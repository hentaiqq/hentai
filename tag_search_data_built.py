import json

tags = {"female":{},"male":{}}

with open("dict.json","r",encoding="utf-8") as f:
    l = json.loads(f.read())

for i in l:
    key = list(i.keys())[0]
    tag = i[key]
    for j in tag:
        j = j.split(":")
        if len(j) < 2:
            continue
        try:
            if not j[1] in tags[j[0]]:
                tags[j[0]][j[1]] = []
        except:
            continue
        tags[j[0]][j[1]].append(key)

with open("tags.json","w",encoding="utf-8") as f:
    f.write(json.dumps(tags,ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':')))
