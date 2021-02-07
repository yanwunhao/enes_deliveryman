import requests
from bs4 import BeautifulSoup
import json

name = 'mxdong'

r = requests.get('http://www3.muroran-it.ac.jp/enes/~' +
                 name + '/activities.html')

text = r.text

soup = BeautifulSoup(text, 'html.parser')

output = {
    "catagory": []
}

catagory_object = {
    "name": '',
    "content": []
}

catagory_object["name"] = soup.find('h1').get_text()

item_list = soup.find('ul', id="zhenzhen")

item_list = item_list.find_all('li')

for item in item_list:
    str = item.get_text()
    catagory_object["content"].append(str)

output["catagory"].append(catagory_object)

json_str = json.dumps(output)

with open('activities.json', 'w') as json_file:
    json_file.write(json_str)
    json_file.close()
