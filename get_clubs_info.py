import pandas
import requests
import feather
import time

TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJNYXJrb3YiLCJhdXRoIjoiUk9MRV9QUkVNSVVNLFJPTEVfVVNFUiIsImV4cCI6MTYwMDE5NTE2Nn0.f147QjUtu0mng62S6byzwQ_95qczsdez2hZ3T_HrLCv7sLptuDsEtB8lq4PVpjnQY0z-1z3kPMpzEa8dUmHcRA"

headers = {"Authorization": f"Bearer {TOKEN}"}

nations_json = requests.get(
    "https://finalwhistle.org/en/api/nations", headers=headers).json()
nations = [n['code'] for n in nations_json]

clubs = {}
for country_code in nations:
    nation_teams_json = requests.get(f"https://finalwhistle.org/en/api/nations/country?code={country_code}", headers=headers).json()
    for team in nation_teams_json:
        print(f"ClubId:{team['clubId']} from {country_code}")
        clubstats = requests.get(f"https://finalwhistle.org/en/api/club/{team['clubId']}", headers=headers).json()
        clubs[str(team["clubId"])] = {
            "name": clubstats["club"]["name"],
            "country": clubstats["club"]["countryName"],
            "series": clubstats["club"]["series"],
            "group": clubstats["club"]["group"],
            "position": clubstats["club"]["position"],
            "YA": clubstats["academyLevel"],
            "SN": clubstats["scoutNetwork"]
        }
    time.sleep(1)
df = pandas.DataFrame.from_dict(clubs, orient = "index")
#### to excel ..####
