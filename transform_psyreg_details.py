import json
import os

from pandas import json_normalize
import glob
from tqdm import tqdm
import pandas as pd
from dateutil.relativedelta import relativedelta

# to know what we are looking for
# (already answers questions)
os.system("grep -rnwl data/psyreg_details/ -e 'licence withdrawn'")


# 2.)   CLEAN DATA

all_results = []

# merge single requests big json
for f in tqdm(glob.glob("data/psyreg_details/*.txt")):
    with open(f, "rb") as infile:
        try:
            data = json.load(infile)
            all_results.append(data)

        except Exception as e:
            print('\nError in {}'.format(infile.name))
            print(e)

print("read {} profiles".format(len(all_results)))

# store as file to meet naming requirements
with open("data/psyreg_details_stage1.json", "w") as outfile:
    json.dump(all_results, outfile)

# delete reference (gc should notice and free memory)
del all_results

# read in formerly stored staging data
with open("data/psyreg_details_stage1.json", "r") as stage_file:
    stage_data = json.load(stage_file)

# function to extract deeply nested attributes for each therapist
def extract_permission_data(x):

    # as json-data is dictionary, we can access with get()
    id = x.get('id')
    titles = x.get('cetTitles',[])

    # list to store permission-data
    perms = []

    # loop over titles
    for title in titles:
        permissions = title.get('permissions', [])
        profession_id = title.get('profession', {}).get('id')
        profession = title.get('profession', {}).get('textEn')

        # loop over permissions in titles
        for permission in permissions:
            dateDecision = permission.get('dateDecision')
            timeLimitationDate = permission.get('timeLimitationDate')

            canton_id = permission.get('canton').get('id')
            canton = permission.get('canton').get('textEn')
            legal_basis = permission.get('legalBasis').get('textEn')
            state_id = permission.get('permissionState').get('id')
            state = permission.get('permissionState').get('textEn')

            addresses = permission.get('addresses',[])

            # append each permission
            perms.append({
                'profession': profession,
                'professionId': profession_id,
                'canton': canton,
                'cantonId': canton_id,
                'legalBasis': legal_basis,
                'state': state,
                'stateId': state_id,
                'date': dateDecision,
                'limited': timeLimitationDate,
                'addresses': addresses
            })
    # return flattened record for every therapist
    return {
        'therapist_id': id,
        'permissions': perms
    }

# flatten input data
flat_stage_data = [extract_permission_data(x) for x in stage_data]

# make dataframe
df_permissions = json_normalize(flat_stage_data, record_path='permissions', meta='therapist_id')

# explode on addresses to later join with address book
df_permissions_addresses = df_permissions.join(df_permissions.addresses.explode().apply(pd.Series)).reset_index(drop=True).drop(['addresses', 0], axis=1)

# some dates have unplausible entries
df_permissions_addresses.date = df_permissions_addresses.date.str.replace('2914-', '2014-')

# apply datetime
df_permissions_addresses.date = pd.to_datetime(df_permissions_addresses.date)
df_permissions_addresses.limited = pd.to_datetime(df_permissions_addresses.limited)

#
# 2.)   ENRICH
#

# as boolean variable
df_permissions_addresses['license_widthdrawn'] = df_permissions_addresses.state.apply(lambda x: "withdrawn" in x)

# license since?
df_permissions_addresses['license_for_x_years'] = df_permissions_addresses.date.apply(lambda x: relativedelta(pd.to_datetime('now', utc=True), x).years)
df_permissions_addresses['license_year_issued'] = df_permissions_addresses.date.dt.year

# save dataframe to csv in order to upload to mariaDB
df_permissions_addresses.to_csv('data/psyreg_details_stage3.csv', index=False)