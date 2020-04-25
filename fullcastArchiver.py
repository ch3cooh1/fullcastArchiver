#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import json
import xml.etree.ElementTree as ET
import pandas as pd
import glob
from datetime import datetime
url = 'https://feeds.megaphone.fm/fullcast'

data = requests.get(url)

tree = ET.fromstring(data.content)

urllist, desclist, titlelist, filenamelist = [],[],[],[]
for node in tree.iter('enclosure'):
    urllist.append(node.attrib.get('url'))
for node in tree.iter('item'):
    desclist.append(node.findall('description')[0].text)
    titlelist.append(node.findall('title')[0].text)
for i in range(len(urllist)):
    filenamelist.append(urllist[i].split('?')[0].split('/')[-1])

lists = [titlelist, desclist, urllist, filenamelist]
df = pd.concat([pd.Series(x) for x in lists],axis=1)
df.columns = ['Title', 'Description','URL', 'fileName']
print('Enter directory to save:')
saveDir = input()

for i in range(len(df)):
    r = requests.get(df['URL'].iloc[i])
    print(str(r.status_code) + '---' + df['fileName'].iloc[i] + '---' + str(datetime.now()))
    with open(saveDir+'/{}'.format(df['fileName'].iloc[i]), 'wb') as f:
        f.write(r.content)
    print(str(len(df)-(i+1)) + ' files remaining')

