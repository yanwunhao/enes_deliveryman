import requests
from bs4 import BeautifulSoup
import json

name = 'mxdong'

r = requests.get('http://www3.muroran-it.ac.jp/enes/~' +
                 name + '/awards.html')

r.encoding = 'utf-8'

text = r.text

soup = BeautifulSoup(text, 'html.parser')

output = {
    "catagory": []
}

awards_obj = {
    "name": "",
    "content": []
}

awards_ul = soup.find(id=name+'_awards')
awards_list = awards_ul.find_all('li')

for item in awards_list:
    parameters = item.get_text().split(',')
    res = {}
    if len(parameters) > 2:
        res["name"] = parameters[0].strip()
        res["org"] = parameters[1].strip()
        res["year"] = parameters[2].strip()
    else:
        res["name"] = parameters[0].strip()
        res["year"] = parameters[1].strip()
    awards_obj["content"].append(res)

awards_obj_as_supervisor = {
    "name": "As supervisor",
    "content": []
}

awards_ul_as_supervisor = soup.find(id=name+'_awards'+'_as'+'_supervisor')
awards_list_as_supervisor = awards_ul_as_supervisor.find_all('li')

for item in awards_list_as_supervisor:
    parameters = item.get_text().split(',')
    res = {}
    if len(parameters) > 2:
        res["name"] = parameters[0].strip()
        res["org"] = parameters[1].strip()
        res["year"] = parameters[2].strip()
    else:
        res["name"] = parameters[0].strip()
        res["year"] = parameters[1].strip()
    awards_obj_as_supervisor["content"].append(res)

output["catagory"].append(awards_obj)
output["catagory"].append(awards_obj_as_supervisor)

json_str = json.dumps(output)

with open('awards.json', 'w') as json_file:
    json_file.write(json_str)
    json_file.close()
