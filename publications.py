import requests
from bs4 import BeautifulSoup
import json

name = 'mxdong'

r = requests.get('http://www3.muroran-it.ac.jp/enes/~' +
                 name + '/publications.html')

r.encoding = 'utf-8'

text = r.text

soup = BeautifulSoup(text, 'html.parser')

output = {
    "catagory": []
}

book_object = {
    "name": "Book Chapters",
    "content": []
}

book_ol = soup.find(id='book_ol')
book_item_list = book_ol.find_all('li')
for book_item in book_item_list:
    item = {}
    str = book_item.get_text()

    arr = str.split('"')
    item["author"] = arr[0].strip()
    item["title"] = arr[1]

    em = book_item.find('em')
    item["medium"] = em.get_text().strip()

    a = book_item.find('a')
    item["link"] = '' if a["href"] is None else a["href"]

    raw_html = book_item.prettify()
    arr2 = raw_html.split('</em>')
    tobehandled = arr2[-1]
    s_index = tobehandled.find('pp')
    if s_index != -1:
        tobehandled = tobehandled[s_index:]
    item["remark"] = tobehandled.replace('\n</li>\n', '').strip()

    book_object["content"].append(item)

output["catagory"].append(book_object)

journal_object = {
    "name": "Journal Papers",
    "content": []
}

journal_ol = soup.find(id='journal_ol')
journal_item_list = journal_ol.find_all('li')
for journal_item in journal_item_list:
    item = {}
    str = journal_item.get_text()

    arr = str.split('"')
    item["author"] = arr[0].strip()
    item["title"] = arr[1]

    em = journal_item.find('em')
    item["medium"] = em.get_text().strip()

    a = journal_item.find('a')
    item["link"] = '' if a["href"] is None else a["href"]

    raw_html = journal_item.prettify()
    arr2 = raw_html.split('</em>')
    tobehandled = arr2[-1]

    index_of_inpress = tobehandled.find('In')
    index_of_vol = tobehandled.find('vol')
    s_index = index_of_inpress \
        if index_of_inpress > index_of_vol \
        else index_of_vol
    if s_index != -1:
        tobehandled = tobehandled[s_index:]

    index_of_font = tobehandled.find('<font')
    if index_of_font != -1:
        tobehandled = tobehandled[:index_of_font]

    item["remark"] = tobehandled.replace('\n</li>\n', '').strip()

    font = journal_item.find('font')
    if font is not None:
        item["award"] = font.get_text().strip()

    journal_object["content"].append(item)

output["catagory"].append(journal_object)

conference_object = {
    "name": "Conference Papers",
    "content": []
}

conference_ol = soup.find(id='conference_ol')
conference_item_list = conference_ol.find_all('li')
for conference_item in conference_item_list:
    item = {}
    str = conference_item.get_text()

    arr = str.split('"')
    item["author"] = arr[0].strip()
    item["title"] = arr[1]

    em = book_item.find('em')
    item["medium"] = em.get_text().strip()

    a = book_item.find('a')
    item["link"] = '' if a["href"] is None else a["href"]

    tobehandled = arr[2]
    index_of_bracket = tobehandled.find('(')
    if index_of_bracket != -1:
        tobehandled = tobehandled[:index_of_bracket]
        item["remark"] = tobehandled.strip()
    else:
        item["remark"] = tobehandled.replace('\n</li>\n', '').strip()

    font = conference_item.find('font')
    if font is not None:
        item["award"] = font.get_text().strip()

    conference_object["content"].append(item)

output["catagory"].append(conference_object)


json_str = json.dumps(output)

with open('publications.json', 'w') as json_file:
    json_file.write(json_str)
    json_file.close()
