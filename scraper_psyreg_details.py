import glob
import os
import time
from torpy.http.requests import TorRequests
import pandas as pd

PATH = 'data/psyreg_details/'

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7); SRF Data data@srf.ch",
           "Sec-GPC": "1", "X-Requested-With": "XMLHttpRequest", "X-Time-Zone-Iana": "Europe/Zurich",
           "api-key": "AB929BB6-8FAC-4298-BC47-74509E45A10B"}
COOKIES = {"_pk_id.198.6ba1": "f5c109f79cd3d9f0.1680250022.", "_pk_ses.198.6ba1": "1",
            "cookiesession1": "678B78A6867542041B1007865A10CB19"}

# make sure data path exits
if not os.path.exists(PATH):
    os.makedirs(PATH)

# set timeout
TIMEOUT = 0.1

# list to scrape
scraper_list = pd.read_csv('data/psyreg.csv')
scraper_list = scraper_list[['id', 'name', 'firstName']]
scraper_list.drop_duplicates(inplace=True)
print("We want to scrape {} entries".format(len(scraper_list)))

while True:

    timestamp = time.localtime()
    print("start (again) at {}. ".format(time.strftime("%H:%M:%S", timestamp)))

    # get already scraped entries
    ignore_list = glob.glob(os.path.join(PATH, "*.txt"))
    ignore_list = [int(path.replace(PATH, '').replace('.txt', '')) for path in ignore_list]
    print("Already saved {} entries".format(len(ignore_list)))

    # subtract already scraped entries
    scraper_list_left = list(set(scraper_list.id) ^ set(ignore_list))
    print("Entries left to scrape: {}".format(len(scraper_list_left)))

    if(len(scraper_list_left) == 0):
        print("finished scraping, exit.")
        break

    # request session for performance reasons
    with TorRequests() as tor_requests:
        with tor_requests.get_session() as s:

            for id in scraper_list_left:

                # prepare url
                url = 'https://www.healthreg-public.admin.ch/api/psyreg/public/person/{}'.format(id)

                # do request
                response = s.get(url,
                                 headers=HEADERS,
                                 cookies=COOKIES)
                try:
                    if ("API calls quota exceeded!" in response.text):
                        raise Exception(response.text)

                    # write every request to file for later processing
                    with open(os.path.join(PATH, "{}.txt".format(id)), "w") as f:
                        f.write(response.text)
                except Exception as e:
                    print(e)
                    break

                # timeout to no impact server performance
                time.sleep(TIMEOUT)

    timestamp = time.localtime()
    print("Timeout at {}. Sleep for 1 minute.".format(time.strftime("%H:%M:%S", timestamp)))
    time.sleep(60)
