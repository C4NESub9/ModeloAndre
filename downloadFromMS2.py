import json
import requests
import pandas as pd
from datetime import datetime, timedelta

url = "https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/"
headers = {
    "accept": "application/json, text/plain, /",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "x-parse-application-id": "unAFkcaNDeXajurGB7LChj8SgQYS2ptm",
}

request = requests.get(url + "PortalGeral", headers=headers)
content = request.content.decode("utf8")
data = json.loads(content)["results"][0]

csv_file = data["arquivo"]["url"]

#df = pd.read_csv(csv_file, sep=";")
df = pd.read_excel(csv_file)
today_date_str = "".join(str(datetime.now().date()).split("-"))
downloadPath = "./dataRaw/"
df.to_csv(downloadPath+"Brasil_COVID19-" + today_date_str + ".csv", index=False)



