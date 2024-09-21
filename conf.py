file=open("conf.ini","r",encoding="UTF-8")
li=[]
for i in file:
    li.append(i)   
lokal_baza=li[0][11:]
uzaq_baza=li[1][10:]
