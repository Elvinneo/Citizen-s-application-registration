import sys
import os
import sqlite3

con = sqlite3.connect("N:/Baza/baza.db")
cur = con.cursor()
sutunlar=[]
for i in range(15):
    metn=cur.execute("""select GROUP_CONCAT(sıra_no),GROUP_CONCAT(daxil_no),GROUP_CONCAT(tarix),GROUP_CONCAT(vereq),GROUP_CONCAT(ad_soyad),GROUP_CONCAT(novu),GROUP_CONCAT(fin),GROUP_CONCAT(unvan),GROUP_CONCAT(tel),GROUP_CONCAT(netice),GROUP_CONCAT(mezmun),GROUP_CONCAT(icraci),GROUP_CONCAT(for),GROUP_CONCAT(cvb_mezmun),GROUP_CONCAT(cvb_tarix) from sifahi where daxil_no=(?) """,(499,))
    metni=metn.fetchall()
    columns=[x[i] for x in metni]
    sutunlar.append(columns[0])

