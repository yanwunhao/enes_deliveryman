import requests
from bs4 import BeautifulSoup
import json

name = 'mxdong'

r = requests.get('http://www3.muroran-it.ac.jp/enes/~' +
                 name + '/teaching.html')

r.encoding = 'utf-8'

text = r.text

soup = BeautifulSoup(text, 'html.parser')

output = {
    "catagory": []
}

for year in range(2020, 2013, -1):
    item = {
        "year": year,
        "list": []
    }
    teaching_in_this_year = soup.find(id=name+'_teach_'+str(year))
    teaching_list = teaching_in_this_year.find_all('li')
    for teaching_item in teaching_list:
        item["list"].append(teaching_item.get_text())
    output["catagory"].append(item)

json_str = json.dumps(output)

with open('teaching.json', 'w') as json_file:
    json_file.write(json_str)
    json_file.close()
