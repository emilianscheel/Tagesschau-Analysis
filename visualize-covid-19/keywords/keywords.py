#
# Verarbeitet die 'keywords.txt' zu einer 'keywords.json'
#

import json

origin_filename = "keywords.txt"
target_filename = "keywords.json"

keywords = []
data = open(origin_filename, "r").read().split("\n")
for line in data:
    if (line.startswith("-")):
        keywords.append(line.split("- ")[1])

f = open(target_filename, "w").write(json.dumps(keywords, indent=4))
