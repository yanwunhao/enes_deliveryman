import requests

r = requests.get('http://www3.muroran-it.ac.jp/enes/~mxdong/publications.html')

print(r.text)
