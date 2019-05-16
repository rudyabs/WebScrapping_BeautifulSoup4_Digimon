from bs4 import BeautifulSoup
import requests
import csv
import mysql.connector

# mendirikan koneksi ke mysql
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'rudyabs',
    passwd = 'Kecapi48',
    database = 'digimon_db',
)

# content yang akan di web scraping
url = 'https://wikimon.net/Visual_List_of_Digimon'
get_url = requests.get(url)
content = BeautifulSoup(get_url.content, 'html.parser')

# cek isi html digimon
# print(content.prettify())

# list nama dan gambar digimon
nama = []
gambar = []

# ambil data nama dan gambar dari tag <alt> di dalam tag <img>
for i in content.find_all('img'):
    nama.append(i.get('alt'))
    gambar.append('https://wikimon.net'+i.get('src')) # tambah domain url gambar

# menghilangkan data yang tidak relevan
nama.pop()
gambar.pop()
nama.pop()
gambar.pop()

# buat csv file
with open('digimon.csv', 'w', newline='', encoding='utf-8') as digimondb:
    writer = csv.writer(digimondb)
    writer.writerows(zip(nama, gambar))
digimondb.close()

# membuat cursor mysql
mycursor = mydb.cursor()

# insert data ke table
for i in range(len(nama)):
    header_nama = nama[i]
    header_gambar = gambar[i]
    mycursor.execute('insert into digimon (nama, gambar) values (%s, %s)', (header_nama, header_gambar))
    mydb.commit()

# tutup mysql
mydb.close()