#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
import json


# In[5]:


data = requests.post("https://app.rextie.com/api/v1/fxrates/rate/?origin=template-original&commit=false", headers={
"Host": "app.rextie.com",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
"Accept": "application/json, text/plain, */*",
"Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
"Accept-Encoding": "gzip, deflate, br",
"Referer": "https://www.rextie.com/",
"Content-Type": "application/json; charset=UTF-8",
"Content-Length": "75",
"Origin": "https://www.rextie.com",
"Connection": "keep-alive",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-site",},json={"source_currency":"PEN","target_currency":"USD","source_amount":"1.00"})


# In[12]:





# In[ ]:


with open('finanzas.json', 'w') as json_file:
    json.dump(data.json(), json_file)

