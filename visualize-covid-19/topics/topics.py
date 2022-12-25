#
# Verarbeitet die 'topics.txt' zu einer 'topics.json'
#

import json

origin_filename = "topics.txt"
target_filename = "topics.json"

topics = {}
current = ""
data = open(origin_filename, "r").read().split("\n")
for line in data:
    if (line.startswith("#")):
        current = line.split("# ")[1]
        topics[current] = {
            "keywords": []
        }
    if (line.startswith("-")):
        topics[current]["keywords"].append(line.split("- ")[1])

f = open(target_filename, "w").write(json.dumps(topics, indent=4))
