import requests

url="http://data.taipei/opendata/datalist/datasetMeta/download;jsessionid=7AC088E2FA3C6BE7F3C8ECC95391E0CC?id=0d1cee1e-4963-41b5-bf9d-93dd5e413cea&rid=7713e7f4-76c6-4f3d-98c4-9ef714c24824"
url="http://data.coa.gov.tw/Service/OpenData/TransService.aspx?UnitId=QcbUEzN6E6DL&FOTT=CSV"
html=requests.get(url)
#html.encoding="cp950"
html.encoding="utf-8"
print(html)

#print(html.text)
a=html.text.split("\r\n")

for b in a:
    print(b)
#print(a)