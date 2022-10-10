import json
import hashlib
import codecs

filename = "UIRes/bannedplugin.json"
with codecs.open("asset.json", "r") as f:
    asset_json = json.load(f)

asset_list = []
for asset in asset_json["Assets"]:
    file_path = asset["FileName"]
    try:
        with open(file_path,"rb") as f:
            bs = f.read()
            readable_hash = hashlib.sha1(bs).hexdigest()
            asset["Hash"] = readable_hash.upper()
            # print(json.dumps(asset, indent=2))
    except FileNotFoundError:
        print("File not found: " + file_path)
    asset_list.append(asset)

asset_json["Assets"] = asset_list
print("Hashed Assets: \n" + str(json.dumps(asset_json, indent=2)))

with codecs.open("asset.json", "w") as f:
    json.dump(asset_json, f, indent=4)
