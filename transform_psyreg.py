import pandas as pd
import json
import glob

all_results = []

for f in glob.glob("data/psyreg/*.txt"):
    with open(f, "rb") as infile:
        res = json.load(infile)
        data = res.get('entries')

        all_results = [*all_results, *data]

# deduplicate
print(len(all_results))
dedup_results = pd.DataFrame(all_results).drop_duplicates(subset='id')
print(len(dedup_results))

# save again as json
dedup_results.to_json('data/psyreg_index.json', orient='records')
