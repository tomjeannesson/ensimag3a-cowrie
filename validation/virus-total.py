import json
from time import sleep

import requests
from domains import domains

apikey1 = ""
apikey2 = ""
try:
    with open("malicious.json", "r") as f:
        malicious = json.load(f)
    with open("checked.json", "r") as f:
        checked = json.load(f)
except FileNotFoundError:
    with open("malicious.json", "w") as f:
        json.dump([], f, indent=4)
        malicious = []
    with open("checked.json", "w") as f:
        json.dump([], f, indent=4)
        checked = []

for domain in domains:
    if domain in checked:
        print(f"Skipping {domain}")
        continue
    print(f"Checking {domain}")
    url = "https://www.virustotal.com/vtapi/v2/domain/report"
    passed = False
    while not passed:
        try:
            params = {
                "apikey": apikey1,
                "domain": domain,
            }
            response = requests.get(url, params=params)
            response_json = json.loads(response.content)
            passed = True
        except json.decoder.JSONDecodeError:
            try:
                params = {
                    "apikey": apikey2,
                    "domain": domain,
                }
                response = requests.get(url, params=params)
                response_json = json.loads(response.content)
                passed = True
            except json.decoder.JSONDecodeError:
                sleep(5)

    with open(f"validation/finds/{domain}.json", "w") as f:
        json.dump(response_json, f, indent=4)
    result = response_json.get("detected_referrer_samples", [])
    d_list = []
    for line in result:
        d_list.append(line["positives"])

    final_result = sum(d_list) if len(d_list) > 0 else -1
    checked.append(domain)

    if final_result == 0:
        print("The Domain Not Malicious! ")
    elif final_result > 0:
        print("The Domain Is Malicious ! ")
        malicious.append(domain)
    with open("malicious.json", "w") as f:
        json.dump(malicious, f, indent=4)
    with open("checked.json", "w") as f:
        json.dump(checked, f, indent=4)
