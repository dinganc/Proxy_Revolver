from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import sqlite3
import datetime

ua = UserAgent() # From here we generate a random user agent

def main():
  conn=sqlite3.connect('Proxies.db')
  cur=conn.cursor()
  proxies_req = Request('https://www.sslproxies.org/')
  proxies_req.add_header('User-Agent', ua.random)
  proxies_doc = urlopen(proxies_req).read().decode('utf8')

  soup = BeautifulSoup(proxies_doc, 'html.parser')
  proxies_table = soup.find(id='proxylisttable')

  for j in range(len(proxies_table.tbody.find_all('tr'))):
    row=proxies_table.tbody.find_all('tr')[j]
    cur.execute("INSERT OR REPLACE INTO Sum VALUES(?,?,?,?)",(str(datetime.datetime.utcnow().timestamp())+'Numba'+str(j),0,row.find_all('td')[0].string, row.find_all('td')[1].string))
    conn.commit()
  cur.close()
  conn.close()

def test_proxy():
  conn=sqlite3.connect('Proxies.db')
  cur=conn.cursor()

  for i in cur.execute("SELECT * FROM Sum ORDER BY UNIX_Checked ASC").fetchall():
    req = Request('http://icanhazip.com')
    req.set_proxy(i[2] + ':' + i[3], 'http')
    try:
      my_ip = urlopen(req,timeout=5).read().decode('utf8')
      print(my_ip+" OK")
      cur.execute("UPDATE Sum SET UNIX_Checked=? WHERE UNIX_Added =?",(datetime.datetime.utcnow().timestamp(),i[0]))
      conn.commit()
    except:
      print(i[2]+' Failed')
      cur.execute("DELETE FROM Sum WHERE UNIX_Added=?",(i[0],))
      conn.commit()
  cur.close()
  conn.close()

import time

main()