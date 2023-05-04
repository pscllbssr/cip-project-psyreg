import time
import requests
import string
import os

# path where to store data
PATH = 'data/psyreg/'

# make sure data path exits
if not os.path.exists(PATH):
   os.makedirs(PATH)

# set timeout in seconds
TIMEOUT = 1

# following constants obtained via chrome plugin
URL = "https://www.psyreg.admin.ch/api/psyreg/public/person/search"
HEADERS = {"Sec-GPC": "1", "X-Requested-With": "XMLHttpRequest", "X-Time-Zone-Iana": "Europe/Zurich",
           "api-key": "AB929BB6-8FAC-4298-BC47-74509E45A10B"}
COOKIES = {"cookiesession1": "678A3EAAFAAB3802FE6B02809165DA7D", "_pk_id.198.50b9": "91606401f87aba27.1679493328.",
           "_pk_ses.198.50b9": "1", "_pk_id.29.ad74": "d58fcd628ef6ec6e.1679988073.", "_pk_ses.29.ad74": "1"}

# manually copied from html-code (browser inspector)
GENDER_IDS = [12000, 12001]

# get all letters
alphabet = list(string.ascii_lowercase)

# request session for performance reasons
s = requests.session()

# scrape per letter and gender
for letter in alphabet:
    for gender_id in GENDER_IDS:
        # prepare payload
        payload = {
            "name": "{}".format(letter),
            "genderId": gender_id}

        # do request
        response = s.post(URL,
                          json=payload,
                          headers=HEADERS,
                          cookies=COOKIES)

        # write every request to file for later processing
        with open(os.path.join(PATH, "response_{}_{}.txt".format(letter, gender_id)), "w") as f:
            f.write(response.text)

        # timeout to no impact server performance
        time.sleep(TIMEOUT)