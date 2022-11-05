import json
import requests

def get_stats(id):
    url = "https://api.spotify.com/v1/audio-analysis/{}".format(id)
    headers = {"Authorization": "Bearer BQBrHZRjpTkfb1jUbXhDht3KsZHIzkeGo6e5ZARQjXBF46Cx70ytq7PsB3g3KrrzHdxUDZ9beQicube7Ym3M2wBG-zre_rALP-RpZ-gNhm7rFDiqY5PxZbzUBlva9-Nt7XqxtAaS-FvRDBm0o99dCKtY41jCLJcHE23eJt9goQw3nXSoBLFZQfRKfFPmOTxzQTfb37M4ez4"}
    response = requests.request("GET", url, headers=headers)
    return response.json()

# Opening JSON file
f = open("/Users/egorg/Documents/GitHub/reaktor-api/spotify_songs/spotify_50_songs.json")
  
# returns JSON object as 
# a dictionary
data = json.load(f)

parsed = []
for item in data["items"]:
    parsed.append({
        "played_at": item["played_at"],
        "name": item["track"]["name"],
        "id": item["track"]["id"]
    })


for p in parsed:
    stat = get_stats(p["id"])
    p["track_statistic"] = stat["track"]


# Serializing json
json_object = json.dumps(parsed, indent=4)
 
# Writing to sample.json
with open("parsed.json", "w") as outfile:
    outfile.write(json_object)

# curl --request GET \
#   --url https://api.spotify.com/v1/audio-analysis/id \
#   --header 'Authorization: ' \
#   --header 'Content-Type: application/json'