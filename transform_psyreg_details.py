import pandas as pd
import json
import glob
from tqdm import tqdm

all_results = []

for f in tqdm(glob.glob("data/psyreg_details/*.txt")):
    with open(f, "rb") as infile:
        try:
            data = json.load(infile)
            all_results.append(data)

        except Exception as e:
            print('\nError in {}'.format(infile.name))
            print(e)


print("read {} profiles".format(len(all_results)))

# @todo: all the flattening stuff...
