#
# Verarbeitet die 'topics.txt' zu einer 'topics.json'
#

import json

origin_filename = "topics.txt"
target_filename = "topics.json"

topics = {}
current_short = ""
data = open(origin_filename, "r").read().split("\n")
for line in data:
    if (line.startswith("#")):
        [topic, current_short] = line.split("# ")[1].split(":::")
        topics[current_short] = {
            "name": topic,
            "short": current_short,
            "keywords": []
        }
    if (line.startswith("-")):
        topics[current_short]["keywords"].append(line.split("- ")[1])

f = open(target_filename, "w").write(json.dumps(topics, indent=4))
