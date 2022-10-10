import os, sys
import json
import requests
import codecs
import csv

# Update the serveropcode.json and clientopcode.json according to
# https://github.com/zhyupe/ffxiv-opcode-worker/blob/master/cn-opcodes.csv

OPCODES_URL = "https://raw.githubusercontent.com/zhyupe/ffxiv-opcode-worker/master/cn-opcodes.csv"

OPCODE_NAMES = {
    "HousingWardInfo": "WardLandInfo",
    "MarketBoardItemRequestStart": "MarketBoardItemListingCount",
    "MarketBoardHistory": "MarketBoardItemListingHistory",
    "MarketBoardOfferings": "MarketBoardItemListing",
    "MarketTaxRates": "ResultDialog",
    "CfNotifyPop": "ContentFinderNotifyPop",
    "AirshipTimers": "CompanyAirshipStatus",
    "SubmarineTimers": "CompanySubmersibleStatus"
}

def update_opcode_json(opcode_json, patch_opcode_json):
    for opcode in opcode_json:
        name = OPCODE_NAMES.get(opcode, opcode)
        opcode_json[opcode] = int(patch_opcode_json.get(name, "-0x1"), 16)
    return opcode_json

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 auto-opcode.py {patch_version}")
        exit(1)
    patch_version = sys.argv[1]
    print("Updating the opcodes for patch version: " + patch_version)
    if not os.path.exists("cn-opcodes.csv"):
        with codecs.open("cn-opcodes.csv", "w") as f:
            f.write(requests.get(OPCODES_URL, timeout=10).text)
    patch_opcode = {}
    with codecs.open("cn-opcodes.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                if row[patch_version]:
                    patch_opcode[row["Name"]] = row[patch_version]
        except KeyError:
            print("Invalid patch version: " + patch_version)
            exit(1)

    with codecs.open("UIRes/serveropcode.json", "r") as f:
        server_opcode_json = json.load(f)
    server_opcode_json = update_opcode_json(server_opcode_json, patch_opcode)
    with codecs.open("UIRes/serveropcode.json", "w") as f:
        json.dump(server_opcode_json, f, indent=4)
        print(f"Server Opcodes:\n{json.dumps(server_opcode_json, indent=4)}")

    with codecs.open("UIRes/clientopcode.json", "r") as f:
        client_opcode_json = json.load(f)
    client_opcode_json = update_opcode_json(client_opcode_json, patch_opcode)
    with codecs.open("UIRes/clientopcode.json", "w") as f:
        json.dump(client_opcode_json, f, indent=4)
        print(f"Client Opcodes:\n{json.dumps(client_opcode_json, indent=4)}")
