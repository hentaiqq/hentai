import matplotlib.pyplot as plt
import json
from collections import Counter
import wordcloud as wc
import matplotlib as mpl

# Set the font size for all text elements to 14
mpl.rcParams['font.size'] = 6

include_tag = ['female','male','other','mixed']
tag_count = Counter()
for i in json.load(open('dict.json',encoding="utf-8")):
    v = list(i.values())[0]
    for j in v:
        for k in include_tag:
            if j.find(k) != -1:
                tag_count[j.split(":")[-1].replace(" ","_")] += 1
                break

tags = []
count = []
for tag in tag_count.most_common(20):
    tags.append(tag[0])
    count.append(tag[1])

plt.bar(range(len(count)), count,tick_label=tags)
plt.show()

wordcloud = wc.WordCloud(max_font_size=60,background_color='white',width=640,height=640).fit_words(tag_count)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
