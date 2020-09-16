import requests
import pandas as pd

header = {"Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJNYXJrb3YiLCJhdXRoIjoiUk9MRV9QUkVNSVVNLFJPTEVfVVNFUiIsImV4cCI6MTU5OTc3NjI0MX0.e0u1ZMOHB00MtGLtWCEIpftr4-LSO9Bs6xn1TD5OAMWawEho1F3JFxEZ8gx3s0XcnMWAkF_Fnnz4amcekUNy7w"}

squaddf = pd.DataFrame(requests.get("https://finalwhistle.org/en/api/player", headers = header).json())

squaddf = pd.concat([squaddf, squaddf.outfielderSkills.apply(pd.Series)], axis=1).drop(["outfielderSkills"], axis=1)

squaddf = pd.concat([squaddf, squaddf.goalKeeperSkills.apply(pd.Series)], axis=1).drop(["goalKeeperSkills"], axis=1)

outfielders = squaddf[squaddf["scoring"].notnull()]
pd.concat([outfielders.offensivePositioning + outfielders.ballControl, outfielders.tackling + outfielders.defensivePositioning], axis=1).rename(columns={0:"OPBC", 1:"TADP"}).min(axis=1)

outfielders.set_index("id", inplace=True)




#### Add ratings for each position to the outfielders dataset
putheader = {"Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJNYXJrb3YiLCJhdXRoIjoiUk9MRV9QUkVNSVVNLFJPTEVfVVNFUiIsImV4cCI6MTU5OTc3NjI0MX0.e0u1ZMOHB00MtGLtWCEIpftr4-LSO9Bs6xn1TD5OAMWawEho1F3JFxEZ8gx3s0XcnMWAkF_Fnnz4amcekUNy7w", "content-length": "17", "content-type": "application/json"}

ratings = []
players = []
for playerid in outfielders.index:
    print(f"getting player {playerid}")
    url = f"https://finalwhistle.org/en/api/player/{playerid}/rating"
    ratings_dict = {}
    for pos in ["CB", "RB", "RWB", "DM", "CM", "OM", "FW"]: 
        pay = {"position":pos}
        RD = requests.put(url, json.dumps(pay), headers=putheader)
        ratings_dict[pos] = (RD.json()["currentRating"], RD.json()["potentialRating"])
    time.sleep(1)
    ratings.append({f"{l}": f"{x1}/{x2}" for (l,(x1,x2)) in ratings_dict.items()})
    players.append(playerid)

ratings = pd.DataFrame(ratings, index=players)

outfielders.join(ratings).to_excel("squad_with_ratings.xlsx")


