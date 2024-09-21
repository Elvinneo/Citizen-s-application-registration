from __future__ import print_function
from mailmerge import MailMerge
import sys
import os
from docx2pdf import convert
import sqlite3
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime,date
from dateutil import parser
import winreg
import subprocess
import time
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
day = date.today()
day=day.strftime("%d/%m/%Y")
try:
    file=open("conf.ini","r",encoding="UTF-8")
    li=[]
    for i in file:
        li.append(i)   
    basis_base=li[0][11:].strip()
    reserve_base=li[1][14:].strip()
    certified_path=li[2][11:].strip()
unless:
    print('Failed to read configuration file')
    sys.exit()
path=document_path+"\\Documents"
#################################################################################################################################################################


class Pencere(QWidget):
    def __init__(self):
        super().__init__()
        

        self.setFixedSize(850,700)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        #qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setStyleSheet("background-color:#6c2cc;")
        self.setWindowTitle("Registration of citizens' applications")
        self.veziyyet=''
        self.user=''
        
        
        self.frame0 = QFrame(self)
        self.frame0.resize(850, 70)
        self.frame0.move(70, 0)
        self.yolu="background-image : url(bas1.jpg);"
   
        self.frame0.setStyleSheet("background-image : url(resurslar//bas1.jpg);")

        self.frame1 = QFrame(self)
        self.frame1.resize(850, 35)
        self.frame1.move(0, 70)
        self.frame1.setStyleSheet("background-color :#b0e0e6;")
        
        self.yol=os.getcwd()
        self.bazayol=esas_baza
        self.yazilisay=0
        self.sifahisay=0
        self.elektronsay=0

        
        
        try:
            os.chdir(self.yol)
            yolu1=os.listdir()
            if not "Endirilənlər" in yolu1:           
                os.mkdir("Endirilənlər")
                os.chdir("Endirilənlər")
                os.mkdir("Şifahi")
                os.mkdir("Yazılı")
                os.mkdir("Elektron")
                os.chdir(self.yol)
                QMessageBox.information(self, "Info","Downloads folder recreated !")
        except Exception as e:
            s=str(e)
            print("Pencere_init"+s)
        try:
            os.chdir(self.bazayol)
            self.dir=os.listdir()
            if "baza.db" not in self.dir:
                QMessageBox.information(self, "Info","Database not available !")
                sys.exit()
            else:             
                self.con = sqlite3.connect(self.bazayol+"\\baza.db")
                self.cur = self.con.cursor()
                self.yazilisay1=self.cur.execute("""SELECT * FROM yazili""")
                self.yazilisay2=self.yazilisay1.fetchall()
                self.yazilisay=len(self.yazilisay2)          
                self.sifahisay1=self.cur.execute("""SELECT * FROM sifahi""")
                self.sifahisay2=self.sifahisay1.fetchall()
                self.sifahisay=len(self.sifahisay2)
                self.elektronsay1=self.cur.execute("""SELECT * FROM elektron""")
                self.elektronsay2=self.elektronsay1.fetchall()
                self.elektronsay=len(self.elektronsay2)

                self.baxilmamissay1=self.cur.execute("""SELECT * FROM sifahi where netice= 'Baxılmadı'""")
                self.baxilmamissay2=self.baxilmamissay1.fetchall()

                self.baxilmamissay3=self.cur.execute("""SELECT * FROM yazili where netice= 'Baxılmadı'""")
                self.baxilmamissay4=self.baxilmamissay3.fetchall()

                self.baxilmamissay5=self.cur.execute("""SELECT * FROM elektron where netice= 'Baxılmadı'""")
                self.baxilmamissay6=self.baxilmamissay5.fetchall()

                self.baxilmamissay=len(self.baxilmamissay2+self.baxilmamissay4+self.baxilmamissay6)
                
                self.baxilmissay1=self.cur.execute("""SELECT * FROM sifahi where netice= 'Baxıldı'""")
                self.baxilmissay2=self.baxilmissay1.fetchall()

                self.baxilmissay3=self.cur.execute("""SELECT * FROM yazili where netice= 'Baxıldı'""")
                self.baxilmissay4=self.baxilmissay3.fetchall()

                self.baxilmissay5=self.cur.execute("""SELECT * FROM elektron where netice= 'Baxıldı'""")
                self.baxilmissay6=self.baxilmissay5.fetchall()

                self.baxilmissay=len(self.baxilmissay2+self.baxilmissay4+self.baxilmissay6)

                self.nosay3=self.cur.execute("""SELECT * FROM yazili where nezaret= 'Nəzarətdədir'""")
                self.nosay4=self.nosay3.fetchall()

                self.nosay5=self.cur.execute("""SELECT * FROM elektron where nezaret= 'Nəzarətdədir'""")
                self.nosay6=self.nosay5.fetchall()

                self.nosay=len(self.nosay4+self.nosay6)

                self.ncsay3=self.cur.execute("""SELECT * FROM yazili where nezaret= 'Nəzarətdən çıxarılmışdır'""")
                self.ncsay4=self.ncsay3.fetchall()

                self.ncsay5=self.cur.execute("""SELECT * FROM elektron where nezaret= 'Nəzarətdən çıxarılmışdır'""")
                self.ncsay6=self.ncsay5.fetchall()

                self.ncsay=len(self.ncsay4+self.ncsay6)
                os.chdir(self.yol)
                
        except Exception as e:
            s=str(e)
            print("Pencere_init"+s)
            sys.exit()
        self.frame = QFrame( self)
        self.frame.resize(850, 50)
        self.frame.move(0, 650)
        self.frame.setStyleSheet("background-color: #b0e0e6; border: 0.5px solid black;")
        self.frame1 = QFrame( self)
        self.frame1.resize(850, 2)
        self.frame1.move(0, 70)
        self.frame1.setStyleSheet("background-color: #8b7d7b; border: 0.5px solid black;")

        self.bayraq = QFrame( self)
        self.bayraq.resize(140, 70)
        self.bayraq.move(710, 0)
        self.bayraq.setStyleSheet("background-image : url(resurslar/bayraq.png);")
        
        self.gerb = QFrame( self)
        self.gerb.resize(62, 62)
        self.gerb.move(2, 2)
        self.gerb.setStyleSheet("background-image : url(resurslar/gerb1.png);")

        self.ist_lab = QLabel(self)
        self.ist_lab.move(8, 75)
        self.ist_lab.resize(250,25)
        self.ist_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : red;")
        self.ist_lab.setText("İstifadəçi:")
       
        self.elave =QPushButton(self)
        self.elave.resize(45, 45)
        self.elave.move(2, 654)
        self.elave.setStyleSheet("background-image : url(resurslar/yarat.jpg);")
        self.elave.clicked.connect(self.muraciet)

        self.axtar =QPushButton(self) 
        self.axtar.resize(45, 45)
        self.axtar.move(49, 654)
        self.axtar.setStyleSheet("background-image : url(resurslar/axtar1.jpg);")
        self.axtar.clicked.connect(self.axtari)

        self.giriset =QPushButton(self)
        self.giriset.resize(45, 45)
        self.giriset.move(94, 654)
        self.giriset.setStyleSheet("background-image : url(resurslar/login.png);")
        self.giriset.clicked.connect(self.gir)

        self.sinx =QPushButton(self) 
        self.sinx.resize(45, 45)
        self.sinx.move(141, 654)
        self.sinx.setStyleSheet("background-image : url(resurslar/yenile.jpg);")
        self.sinx.clicked.connect(self.yenile_)

        self.cixis =QPushButton(self)
        self.cixis.resize(100, 30)
        self.cixis.move(745, 660)
        self.cixis.setText("Çıxış")
        self.cixis.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")
        self.cixis.clicked.connect(self.cix)

        self.cercive1=QFrame(self)
        self.cercive1.move(0,102)
        self.cercive1.resize(850,2)
        self.cercive1.setStyleSheet("background-color : black")

        self.cercive2=QFrame(self)
        self.cercive2.move(1,104)
        self.cercive2.resize(849,545)
        self.cercive2.setStyleSheet("background-image : url(resurslar/2.jpg);")

        self.ust=QLineEdit(self)
        self.ust.move(100,120)
        self.ust.resize(651,2)
        self.ust.setStyleSheet("background-color : #ffe413;")

        self.alt=QLineEdit(self)
        self.alt.move(100,330)
        self.alt.resize(651,2)
        self.alt.setStyleSheet("background-color : #ffe413;")        

        self.sag=QLineEdit(self)
        self.sag.move(100,120)
        self.sag.resize(2,210)
        self.sag.setStyleSheet("background-color : #ffe413;")   

        self.sol=QLineEdit(self)
        self.sol.move(750,120)
        self.sol.resize(2,210)
        self.sol.setStyleSheet("background-color : #ffe413;")


        self.sinxron=QLabel(self)
        self.sinxron.move(200, 660)
        self.sinxron.resize(450,25)
        self.sinxron.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : green;")
        self.sinxron.setText("Son sinxronizasiya tarixi :")
        
       
        self.ys=QLabel(self)
        self.ys.move(125, 140)
        self.ys.resize(300,25)
        self.ys.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : #ffe413;")
        self.ys.setText("Yazılı müraciət sayı:".ljust(31," ")+ str(self.yazilisay))

        self.ss=QLabel(self)
        self.ss.move(125, 190)
        self.ss.resize(300,25)
        self.ss.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : #ffe413;")
        self.ss.setText("Şifahi müraciət sayı:".ljust(30," ")+ str(self.sifahisay))

        self.baxilmis=QLabel(self)
        self.baxilmis.move(370, 140)
        self.baxilmis.resize(300,25)
        self.baxilmis.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : #ffe413;")
        self.baxilmis.setText("Baxılmış müraciət sayı:".ljust(34," ")+ str(self.baxilmissay))

        self.baxilmamis=QLabel(self)
        self.baxilmamis.move(370, 190)
        self.baxilmamis.resize(300,25)
        self.baxilmamis.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : #ffe413;")
        self.baxilmamis.setText("Baxılmamış müraciət sayı:".ljust(31," ")+ str(self.baxilmamissay))

        self.es=QLabel(self)
        self.es.move(125, 240)
        self.es.resize(300,25)
        self.es.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : #ffe413;")
        self.es.setText("Elektron müraciət sayı:".ljust(28," ")+ str(self.elektronsay))


        self.no=QLabel(self)
        self.no.move(370, 240)
        self.no.resize(300,25)
        self.no.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : #ffe413;")
        self.no.setText("Nəzarətdə olan:".ljust(40," ")+ str(self.nosay))

        self.nc=QLabel(self)
        self.nc.move(370, 285)
        self.nc.resize(300,25)
        self.nc.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : #ffe413;")
        self.nc.setText("Nəzarətdən çıxarılmış:".ljust(35," ")+ str(self.ncsay))

        self.cem=QLabel(self)
        self.cem.move(125, 285)
        self.cem.resize(300,25)
        self.cem.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : #ffe413;")
        self.cem.setText("Cəm müraciət sayı:".ljust(29," ")+ str(self.sifahisay+self.yazilisay+self.elektronsay))
        
        
    def yenile_(self):
        if self.veziyyet=="giris olunub":
            try:
                os.chdir(esas_baza)
                a=str(datetime.now().strftime("%d-%m-%Y.%H-%M-%S"))
                b=self.user
                self.dir=os.listdir()
                source=os.path.join(esas_baza+'\\baza.db')
                destination=os.path.join(ehtiyyat_baza+'\\'+a+'-'+b+'.db')
                shutil.copy2(source,destination)
                QMessageBox.information(self, "İnfo","Backup database"+a+".db  created\n\nPath to file: "+destination)
                text="Son sinxronizasiya tarixi :" + " "+str(datetime.now().strftime("%m-%d-%Y.%H:%M:%S"))
            except Exception as e:
                s=str(e)
                print("Pencere_yenile"+s)
                os.chdir(self.yol)
            self.sinxron.setText(text)               
            os.chdir(self.yol)
        else:
            QMessageBox.information(self, "Info","Unable to synchronize database without user login ")

        
                

    def axtari(self):
        try:
            if not len(str(self.ist_lab.text()))>11:            
                QMessageBox.information(self, "Info","Unable to search without user login ")
            else:
                axtaris_ekran.yenile()
                self.hide()
                axtaris_ekran.radioclick1()
                axtaris_ekran.show()
        except Exception as e:
            s=str(e)
            print("Pencere_axtari"+s)

            
    def gir(self):
        try:
            qm =QMessageBox
            if len(str(login_ekran.ist.text()))>0 and len(str(login_ekran.parol.text()))>0:
                ret=qm.question(self,'Message', "Do you want to leave the user profile?", qm.Yes | qm.No)
                if ret==qm.Yes:
                    login_ekran.ist.setText("")
                    login_ekran.parol.setText("")
                    self.ist_lab.setText("İstifadəçi: "+login_ekran.ist.text())
                    QMessageBox.information(self, "Info","Logged out   ")
                    self.ist_lab.setText("İstifadəçi:")
                else:
                    pass
                
            else:
                self.hide()
                login_ekran.show()
        except Exception as e:
            s=str(e)
            print("Pencere_gir"+s)

            
    def muraciet(self):
        try:
            if not len(str(self.ist_lab.text()))>11:            
                QMessageBox.information(self, "Info","Unable to enter application without user login ")
            else:
                ana_ekran.hide()
                muraciet_ekran.show()
                muraciet_ekran.legv()
        except Exception as e:
            s=str(e)
            print("Pencere_muraciet"+s)

    def cix(self):
        try:
            qm =QMessageBox
            ret=qm.question(self,'Message', 'You want to exit the program?", qm.Yes | qm.No)
            if ret==qm.Yes:
                sys.exit()
            else:
                pass
        except Exception as e:
            s=str(e)
            print("Pencere_cix"+s)
###############################################################################################################################################################

class Pencere1(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 170)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setStyleSheet("background-image:#6c2cc;")
        self.setWindowTitle("Giriş")
        self.yol=os.getcwd()
        self.bazayol=esas_baza

        try:
            os.chdir(self.bazayol)
            self.dir=os.listdir()
            if "baza.db" not in self.dir:
                QMessageBox.information(self, "Info","Database not available !")
                sys.exit()
            else:             
                self.con = sqlite3.connect(self.bazayol+"\\baza.db")
                self.cur = self.con.cursor()

            self.metn=''
            self.metn=self.cur.execute("SELECT ad FROM istifadeci")
            self.metn1=self.metn.fetchall()
            self.istifad=[]
            os.chdir(self.yol)
            for i in self.metn1:
                self.istifad.append(* i)
               
                
            self.metn2=''
            self.metn2=self.cur.execute("SELECT sifre FROM istifadeci")
            self.metn3=self.metn2.fetchall()
            self.parolu=[]
            for i in self.metn3:
                self.parolu.append(* i)
          
            self.say=0
            self.istifadeci={}
            
            for i in self.istifad:
                self.istifadeci[str(self.istifad[self.say])]=str(self.parolu[self.say])
                self.say+=1

            
        except Exception as e:
            s=str(e)
            print("Pencere1_init"+s)
            sys.exit()

        self.istifadeciler=QCompleter(self.istifadeci)
        self.gir =QPushButton(self)
        self.gir.resize(100, 30)
        self.gir.move(185, 135)
        self.gir.setText("Giriş")
        #self.gir.setStyleSheet("background-image : url(resurslar/yarat.jpg);")
        self.gir.clicked.connect(self.giris)
        self.gir.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")

        self.bagla =QPushButton(self)
        self.bagla.resize(100, 30)
        self.bagla.move(290, 135)
        self.bagla.setText("Bağla")
        #self.bagla.setStyleSheet("background-image : url(resurslar/yarat.jpg);")
        self.bagla.clicked.connect(self.baglama)
        self.bagla.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")

        self.deyiss =QPushButton(self)
        self.deyiss.resize(100, 30)
        self.deyiss.move(80, 135)
        self.deyiss.setText("Şifrə dəyiş")
        #self.bagla.setStyleSheet("background-image : url(resurslar/yarat.jpg);")
        self.deyiss.clicked.connect(self.deyis)
        self.deyiss.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.sss=0
        
        self.ist_ad=QLabel(self)
        self.ist_ad.move(5, 28)
        self.ist_ad.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")
        self.ist_ad.setText("İstifadəçi adı")

        self.ist_sifre=QLabel(self)
        self.ist_sifre.move(5, 62)
        self.ist_sifre.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")
        self.ist_sifre.setText("Şifrə")

        self.ist = QLineEdit(self)
        self.ist.move(130, 20)
        self.ist.resize(250,30)
        self.ist.setCompleter(self.istifadeciler)
        self.ist.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")

        self.parol = QLineEdit(self,echoMode=QLineEdit.EchoMode.Password)
        self.parol.move(130, 60)
        self.parol.resize(250,30)
        self.parol.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")


        self.ist_ysifre=QLabel(self)
        self.ist_ysifre.move(5, 96)
        self.ist_ysifre.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")
        self.ist_ysifre.setText("Yeni şifrə")
        self.ist_ysifre.hide()


        self.isti = QLineEdit(self)
        self.isti.move(130, 100)
        self.isti.resize(250,30)
        self.isti.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.isti.hide()
    def keyPressEvent(self, e):
        if e.key() == 16777220 or e.key() == 16777221 :
            self.giris()

    def deyis(self):
        try:
            if self.ist.text() not in self.istifadeci:
               QMessageBox.critical(self, "Error", "This user does not exist in the database!")
            else:
                
                if self.sss==0:
                    self.gir.hide()                   
                    self.setWindowTitle("Şifrə dəyişmə")
                    self.ist_ysifre.show()
                    self.isti.show()
                    self.parol.setText('')
                    self.isti.setText('')

                    self.setFixedSize(400, 200)
                    self.deyiss.move(175, 160)
                    self.bagla.move(280, 160)
                    self.ist.setEnabled(False)
                    
                    self.sss+=1
                else:
        
                    met=self.cur.execute("""select sifre from istifadeci where ad=?""",(self.ist.text(),))
                    met1=met.fetchall()
                    if not self.parol.text()==str(met1[0]).strip("' '")[2:-3]:

                        QMessageBox.critical(self, "Info","The user password is incorrect")

                    else:
                        if self.isti.text()== str(met1[0]).strip("' '")[2:-3]:
                            QMessageBox.information(self, "Info","The new password is the same as the previous one!")


                        else:
                            self.istifadeci={}
                            self.query="""UPDATE istifadeci set sifre=? where ad=?"""
                            self.values=(self.isti.text(),self.ist.text())
                            self.cur.execute (self.query,self.values)
                            self.con.commit()
                            self.metn2=''
                            self.metn2=self.cur.execute("SELECT sifre FROM istifadeci")
                            self.metn3=self.metn2.fetchall()
                            self.parolu=[]
                            for i in self.metn3:
                                self.parolu.append(* i)
                            self.say=0
                            self.istifadeci={}
            
                            for i in self.istifad:
                                self.istifadeci[str(self.istifad[self.say])]=str(self.parolu[self.say])
                                self.say+=1
                            QMessageBox.information(self, "Info","User password changed")
                            self.sss=0
        
        except Exception as e:
            s=str(e)
            print("Pencere1_deyis"+s)
        
    def giris(self):
        try:
            sifresi=self.istifadeci.get(self.ist.text())               
            if self.ist.text() in self.istifad and sifresi==self.parol.text():
                login_ekran.hide()
                ana_ekran.show()
                ana_ekran.ist_lab.setText("İstifadəçi : "+ login_ekran.ist.text())
                ana_ekran.veziyyet='giris olunub'
                ana_ekran.user=login_ekran.ist.text()
            else:
                QMessageBox.critical(self, "Error", "The username or password is incorrect!")

        except Exception as e:
            s=str(e)
            print("Pencere1_giris"+s)

            
    def baglama(self):
        try:
            self.gir.show()
            self.deyiss.move(80, 135)       
            self.ist.setText("")
            self.parol.setText("")
            self.setWindowTitle("Giriş")
            self.ist_ysifre.hide()
            self.isti.hide()
            self.ist.setEnabled(True)
            self.setFixedSize(400, 170)
            self.bagla.move(290, 135)       
            self.hide()
            ana_ekran.show()
        except Exception as e:
            s=str(e)
            print("Pencere1_baglama"+s)
        
####################################################################################################################################################################
class Pencere2(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(850, 750)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setStyleSheet("background-color: #dcdcdc;")
        self.setWindowTitle("Yeni müraciət")
        self.yol=os.getcwd()
        self.bazayol=esas_baza
        try:
            os.chdir(self.bazayol)
            self.dir=os.listdir()
            if "baza.db" not in self.dir:
                QMessageBox.information(self, "Info","Database not available !")
                sys.exit()
            else:             
                self.con = sqlite3.connect(self.bazayol+"\\baza.db")
                self.cur = self.con.cursor()
                os.chdir(self.yol)

        except Exception as e:
            s=str(e)
            print("Pencere2_init"+s)
            sys.exit()

        self.yoxla()
        self.metn=self.cur.execute("SELECT sıra_no FROM sifahi")
        self.metn1=self.metn.fetchall()
        self.sirasi=[]
        for i in self.metn1:
            self.sirasi.append(* i)
        try:
            self.sifahi_sira_nomre=int(self.sirasi[-1])+1
        except:
            self.sifahi_sira_nomre=1
            
        
        self.metn2=self.cur.execute("SELECT sira_no FROM yazili")
        self.metn3=self.metn2.fetchall()
        self.yazili_sirasi=[]
        for i in self.metn3:
            self.yazili_sirasi.append(* i)
        try:
            self.yazili_sira_nomre=int(self.yazili_sirasi[-1])+1
        except:
            self.yazili_sira_nomre=1

        self.metn4=self.cur.execute("SELECT sira_no FROM elektron")
        self.metn5=self.metn4.fetchall()
        self.elektron_sirasi=[]
        for i in self.metn5:
            self.elektron_sirasi.append(* i)
        try:
            self.elektron_sira_nomre=int(self.elektron_sirasi[-1])+1
        except:
            self.elektron_sira_nomre=1

        self.novu=['Ərizə','Təklif','Şikayət']
        self.xarakte=" .Ailə münasibətləri üzrə mübahisələr.Əmək mübahisələri.Mənzil mübahisələri.Mülkiyyət hüququ ilə əlaqədar mübahisələr.Əqli mülkiyyət hüququ ilə əlaqədar mübahisələr.Torpaq mübahisələri.Müqavilələrin bağlanması.Müqavilələrin ləğv edilməsi.Müqavilələrin məcburi bağlanması,müqavilənin etibarsız hesab edilməsi tələbi üzrə.Müqavilələrdən əmələ gələn öhdəliklər üzrə mübahisələr.Mülki hüquq pozuntularından (deliktlərdən) əmələ gələn öhdəliklər üzrə mübahisələr.Vərəsəlik hüququ üzrə mübahisələr.Hüquqi əhəmiyyəti olan faktların müəyyən edilməsi haqqında.Şəxsin xəbərsiz itkin düşmüş hesab edilməsi haqqında.Şəxsin ölmüş elan edilməsi haqqında.Şəxsin məhdud fəaliyyət qabiliyyətli və ya fəaliyyət qabiliyyəti olmayan hesab edilməsi haqqında.Şəxsin xəbərsiz itkin düşmüş hesab edilməsi və ya şəxsin ölmüş elan edilməsi haqqında.Daşınar əşyanın sahibsiz hesab edilməsi və daşınmaz əşya üzərində dövlət mülkyyəti hüququnun tanınması haqqında.Notariat hərəkətlərindən və ya həmin hərəkətlərin aparılmasından imtinaya dair şikayətlər üzrə icraat.Vətəndaşlıq vəziyyəti aktlarının qeydiyyatının düzgün olmamasının müəyyən edilməsi haqqında.Məişət zorakılığı ilə bağlı müraciətlər.Şərəf və ləyaqətin müdafiəsi üzrə.Müvafiq icra hakimiyyəti orqanlarının və onların vəzifəli şəxslərinin inzibati hüquq pozuntuları ilə bağlı müraciətlər.Müvafiq icra hakimiyyəti və yerli özünüidarə orqanlarının, sair orqan və təşkilatların, onların vəzifəli şəxslərinin qərarlarından və hərəkətlərindən (hərəkətsizliklərindən) olan müraciətlər üzrə.Övladlığa götürmə.Mülki və cinayət işlərinə məhkəmələr tərəfindən vaxtında baxılmaması ilə bağlı müraciətlər.Birinci instansiya məhkəmələri tərəfindən baxılmış işlər üzrə apеllyasiya şikayəti (protеsti).Apеllyasiya qaydasında baxılmış işlər  üzrə kassasiya şikayəti (protеsti).Mülki və cinayət işlərinə, inzibati xətalara dair matеriallara məhkəmələr tərəfindən obyеktiv baxılmaması ilə bağlı müraciətlər.Naxçıvan MR Ali Məhkəməsinin icraatında olan işlərlə bağlı müxtəlif məzmunlu ərizələr.Qətnamələrin və məhkəmə əmrlərinin vaxtında icra olunmaması ilə bağlı ərizələr.Sair məzmunlu ərizələr.Təkrar ərizə və şikayətlər.Etiraz ərizələri"
        self.xarakter=self.xarakte.split(".")
        self.xarakteri=[]
        for i in self.xarakter:
            self.xarakteri.append(i)
        

        self.icraci=["Əsgər Novruzov","İlqar Mirzayev","Əli Allahverdiyev","Yusifəli Qurbanov","Səxavət Novruzov","Səxavət Bəylərli","Sənan Qarayev","Mehman Allahverdiyev","Fərman Abbasov","Vüqar Quliyev","Vera Kuimova","Gülay Qurbanova","Oruc Əliyev","Sahilə Bağırova","Aqil Atakişiyev"]
        self.neticesi=["Baxıldı","Baxılmadı"]
        self.nezareti=["Nəzarətdədir","Nəzarətdən çıxarılmışdır"]
        self.derkenar=["Sədr","Sədr müavini"]
        self.formas=["Məktub","Elektron məktub","Teleqram","Faks"]
        self.yollar=["Poçt","Elektron poçt","Teleqram","Faks","Qəbul zamanı"]
        self.evvelkil=[]
       
        basliq = QLabel(self)
        basliq.move(0, 0)
        basliq.resize(850,79)
        basliq.setStyleSheet("font-family: Arial;font-style:normal ;background-image : url(resurslar/ali.jpg) ;font-size: 16pt;color : black; border: 1px solid black")
        
        self.radiobutton = QRadioButton(self)
        self.radiobutton.setText("Şifahi müraciət")
        self.radiobutton.setChecked(False)
        self.radiobutton.toggled.connect(self.sifahi)
        self.radiobutton.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")
        self.radiobutton.move(130, 90)
        self.radiobutton.toggled.connect(self.yenile)

        self.radiobutton1 = QRadioButton(self)
        self.radiobutton1.setText("Yazılı müraciət")
        self.radiobutton1.setChecked(True)
        self.radiobutton1.toggled.connect(self.yazili)
        self.radiobutton1.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")
        self.radiobutton1.move(350, 90)
        self.radiobutton1.toggled.connect(self.yenile)

        self.radiobutton2 = QRadioButton(self)
        self.radiobutton2.setText("Elektron müraciət")
        self.radiobutton2.setChecked(False)
        self.radiobutton2.toggled.connect(self.elektron)
        self.radiobutton2.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")
        self.radiobutton2.move(570, 90)
        self.radiobutton2.toggled.connect(self.yenile)

        self.sira_no = QLineEdit(self)
        self.sira_no.move(200, 130)
        self.sira_no.resize(100,22)
        self.sira_no.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.sira_no_lab = QLabel(self)
        self.sira_no_lab.move(20, 130)
        self.sira_no_lab.resize(180,25)
        self.sira_no_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.sira_no_lab.setText("Sıra nömrəsi")
        #self.sira_no.setEnabled(False)


        if self.radiobutton.isChecked():
            self.sira_no.setText(str(self.sifahi_sira_nomre))
        elif self.radiobutton1.isChecked():
            self.sira_no.setText(str(self.yazili_sira_nomre))
        elif self.radiobutton2.isChecked():
            self.sira_no.setText(str(self.elektron_sira_nomre))
 
        self.daxil_no = QLineEdit(self)
        self.daxil_no.move(200, 165)
        self.daxil_no.resize(200,22)
        self.daxil_no.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.daxil_no_lab = QLabel(self)
        self.daxil_no_lab.move(20, 165)
        self.daxil_no_lab.resize(180,25)
        self.daxil_no_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.daxil_no_lab.setText("Qeydiyyat nömrəsi")

        self.tarix = QDateEdit(self)
        self.tarix.move(200, 200)
        self.tarix.resize(100,22)
        self.tarix.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.tarix_lab = QLabel(self)
        self.tarix_lab.move(20, 200)
        self.tarix_lab.resize(180,25)
        self.tarix_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.tarix_lab.setText("Qeydiyyat tarixi")
        self.tarix.setDate(QDate.currentDate())
        
        self.vereq= QLineEdit(self)
        self.vereq.move(200, 235)
        self.vereq.resize(100,22)
        self.vereq.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.vereq_lab = QLabel(self)
        self.vereq_lab.move(20, 235)
        self.vereq_lab.resize(180,25)
        self.vereq_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.vereq_lab.setText("Vərəq sayı ")

        self.ad = QTextEdit(self)
        self.ad.move(200, 261)
        self.ad.resize(200,40)
        self.ad.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.ad_lab = QLabel(self)
        self.ad_lab.move(20, 270)
        self.ad_lab.resize(180,25)
        self.ad_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.ad_lab.setText("Ad,soyad,ata adı")

        self.fin = QLineEdit(self)
        self.fin.move(200, 305)
        self.fin.resize(100,22)
        self.fin.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.fin_lab = QLabel(self)
        self.fin_lab.move(20, 305)
        self.fin_lab.resize(180,25)
        self.fin_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.fin_lab.setText("FİN nömrəsi")
        self.fin.returnPressed.connect(self.evvelde)
        
        self.unv = QLineEdit(self)
        self.unv.move(200, 340)
        self.unv.resize(610,22)
        self.unv.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.unv_lab = QLabel(self)
        self.unv_lab.move(20, 340)
        self.unv_lab.resize(180,25)
        self.unv_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.unv_lab.setText("Ünvanı")

        self.tel = QLineEdit(self)
        self.tel.move(200, 375)
        self.tel.resize(100,22)
        self.tel.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.tel_lab = QLabel(self)
        self.tel_lab.move(20, 375)
        self.tel_lab.resize(180,25)
        self.tel_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.tel_lab.setText("Telefon nömrəsi")

        self.nov = QComboBox(self)
        self.nov.move(660, 375)
        self.nov.resize(150,22)
        self.nov.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.nov.addItems(self.novu)
        self.nov_lab = QLabel(self)
        self.nov_lab.move(430, 375)
        self.nov_lab.resize(130,25)
        self.nov_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.nov_lab.setText("Müraciətin növü")

        self.xar = QComboBox(self)
        self.xar.move(200, 410)
        self.xar.resize(610,44)
        self.xar.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.xar.addItems(self.xarakteri)
        self.xar_lab = QLabel(self)
        #self.xar.setWordWrap(True)
        self.xar_lab.move(20, 410)
        self.xar_lab.resize(180,25)
        self.xar_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.xar_lab.setText("Müraciətin xarakteri")       
        self.xarakterler=QCompleter(self.xarakteri)
        self.xar.setCompleter(self.xarakterler)

        self.mezmun = QTextEdit(self)
        self.mezmun.move(200, 465)
        self.mezmun.resize(610,44)
        self.mezmun.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.mezmun_lab = QLabel(self)
        self.mezmun_lab.move(20, 465)
        self.mezmun_lab.resize(180,25)
        self.mezmun_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.mezmun_lab.setText("Müraciətin qısa məzmnu")


        self.icra = QComboBox(self)
        self.icra.move(200, 575)
        self.icra.resize(190,22)
        self.icra.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.icra.addItems(self.icraci)
        self.icra_lab = QLabel(self)
        self.icra_lab.move(20, 575)
        self.icra_lab.resize(180,25)
        self.icra_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.icra_lab.setText("İcraçı")

        self.netice = QComboBox(self)
        self.netice.move(200, 610)
        self.netice.resize(190,22)
        self.netice.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.netice.addItems(self.neticesi)
        self.netice_lab = QLabel(self)
        self.netice_lab.move(20, 610)
        self.netice_lab.resize(150,25)
        self.netice_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.netice_lab.setText("Nəticəsi")

        self.aid = QTextEdit(self)
        self.aid.move(510,645)
        self.aid.resize(300,44)
        self.aid.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.aid_lab = QLabel(self)
        self.aid_lab.move(430, 665)
        self.aid_lab.resize(75,25)
        self.aid_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.aid_lab.setText("Aidiyyət")

        self.nez = QComboBox(self)
        self.nez.move(610, 610)
        self.nez.resize(200,22)
        self.nez.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.nez.addItems(self.nezareti)
        self.nez_lab = QLabel(self)
        self.nez_lab.move(430, 610)
        self.nez_lab.resize(75,25)
        self.nez_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.nez_lab.setText("Nəzarət")

        self.cvb_mzm = QTextEdit(self)
        self.cvb_mzm.move(200, 520)
        self.cvb_mzm.resize(610,44)
        self.cvb_mzm.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.cvb_mzm_lab = QLabel(self)
        self.cvb_mzm_lab.move(20, 520)
        self.cvb_mzm_lab.resize(150,25)
        self.cvb_mzm_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.cvb_mzm_lab.setText("Cavabın məzmunu")
        
        self.cvb_trx = QLineEdit(self)
        self.cvb_trx.move(200, 665)
        self.cvb_trx.resize(190,22)
        self.cvb_trx.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.cvb_trx_lab = QLabel(self)
        self.cvb_trx_lab.move(20, 665)
        self.cvb_trx_lab.resize(150,25)
        self.cvb_trx_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.cvb_trx_lab.setText("Cavabın tarixi")


        self.cvb_ind = QLineEdit(self)
        self.cvb_ind.move(610, 575)
        self.cvb_ind.resize(200,22)
        self.cvb_ind.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.cvb_ind_lab = QLabel(self)
        self.cvb_ind_lab.move(430, 575)
        self.cvb_ind_lab.resize(120,25)
        self.cvb_ind_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.cvb_ind_lab.setText("Cavabın indeksi")

        self.derk = QComboBox(self)
        self.derk.move(660, 130)
        self.derk.resize(150,22)
        self.derk.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.derk.addItems(self.derkenar)
        self.derk_lab = QLabel(self)
        #self.derk.setWordWrap(True)
        self.derk_lab.move(430, 130)
        self.derk_lab.resize(170,25)
        self.derk_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.derk_lab.setText("Dərkənar")


        self.formasi = QComboBox(self)
        self.formasi.move(660, 165)
        self.formasi.resize(150,22)
        self.formasi.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.formasi.addItems(self.formas)
        self.formasi_lab = QLabel(self)
        #self.formasi.setWordWrap(True)
        self.formasi_lab.move(430, 165)
        self.formasi_lab.resize(170,25)
        self.formasi_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.formasi_lab.setText("Müraciətin forması")


        self.yolu = QComboBox(self)
        self.yolu.move(660, 200)
        self.yolu.resize(150,22)
        self.yolu.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.yolu.addItems(self.yollar)
        self.yolu_lab = QLabel(self)
        #self.yolu.setWordWrap(True)
        self.yolu_lab.move(430, 200)
        self.yolu_lab.resize(170,25)
        self.yolu_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.yolu_lab.setText("Müraciətin Qeydiyyat yolu")


        self.sexs = QLineEdit(self)
        self.sexs.move(660, 235)
        self.sexs.resize(150,22)
        self.sexs.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.sexs_lab = QLabel(self)
        self.sexs_lab.move(430, 235)
        self.sexs_lab.resize(170,25)
        self.sexs_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.sexs_lab.setText("Ünvanlandığı şəxs")

        self.evvel = QComboBox(self)
        self.evvel.move(660, 265)
        self.evvel.resize(150,22)
        self.evvel.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.evvel_lab = QLabel(self)
        self.evvel.addItems(self.evvelkil)
        self.evvel_lab.move(430, 265)
        self.evvel_lab.resize(170,25)
        self.evvel_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.evvel_lab.setText("Əvvəlki müraciətlər")

        self.gonderen = QTextEdit(self)
        self.gonderen.move(580, 296)
        self.gonderen.resize(230,40)
        self.gonderen.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.gonderen_lab = QLabel(self)
        self.gonderen_lab.move(430, 300)
        self.gonderen_lab.resize(150,35)
        self.gonderen_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
        self.gonderen_lab.setText("Müşaiyət məktubunu göndərən")
        self.gonderen_lab.setWordWrap(True)

        self.cerci=QFrame(self)
        self.cerci.resize(850,55)
        self.cerci.move(0,695)
        self.cerci.setStyleSheet("background-image : url(resurslar/alt.jpg);")
        
        self.printe=QPushButton(self)
        self.printe.resize(47,47)
        self.printe.move(5,700)
        self.printe.setStyleSheet("background-image : url(resurslar/pr.jpg);")
        self.printe.clicked.connect(self.printet)

        self.pdf=QPushButton(self)
        self.pdf.resize(47,47)
        self.pdf.move(55,700)
        self.pdf.setStyleSheet("background-image : url(resurslar/pd.jpg);")
        self.pdf.clicked.connect(self.sened)

        self.erize_yukle=QPushButton(self)
        self.erize_yukle.resize(47,47)
        self.erize_yukle.move(105,700)
        self.erize_yukle.setStyleSheet("background-image : url(resurslar/yuk.jpg);")
        self.erize_yukle.clicked.connect(self.er_yukle)

        self.cavab_yukle=QPushButton(self)
        self.cavab_yukle.resize(47,47)
        self.cavab_yukle.move(155,700)
        self.cavab_yukle.setStyleSheet("background-image : url(resurslar/me.jpg);")
        self.cavab_yukle.clicked.connect(self.cvb_yukle)

        self.qayittt=QPushButton(self)
        self.qayittt.resize(160,30)
        self.qayittt.move(680,710)
        self.qayittt.setText("Əsas menyuya qayıt")
        self.qayittt.clicked.connect(self.esas)
        self.qayittt.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 11pt;font-weight: bold;color : black;")

        self.qeydet=QPushButton(self)
        self.qeydet.resize(160,30)
        self.qeydet.move(515,710)
        self.qeydet.setText("Müraciəti qeyd et")
        self.qeydet.clicked.connect(self.qeydd)
        self.qeydet.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 11pt;font-weight: bold;color : black;")

        self.legvet=QPushButton(self)
        self.legvet.resize(160,30)
        self.legvet.move(350,710)
        self.legvet.clicked.connect(self.legv)
        self.legvet.setText("Müraciəti ləğv et")
        self.legvet.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 11pt;font-weight: bold;color : black;")

        self.endirilen=QPushButton(self)
        self.endirilen.resize(140,30)
        self.endirilen.move(205,710)
        self.endirilen.clicked.connect(self.endiri)
        self.endirilen.setText("Endirilənlər")
        self.endirilen.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 11pt;font-weight: bold;color : black;")


    def yenile(self):
        try:
            if self.radiobutton.isChecked():
                self.sira_no.setText(str(self.sifahi_sira_nomre))
            elif self.radiobutton1.isChecked():
                self.sira_no.setText(str(self.yazili_sira_nomre))
            elif self.radiobutton2.isChecked():
                self.sira_no.setText(str(self.elektron_sira_nomre))
        except Exception as e:
            s=str(e)
            print("Pencere2_yenile"+s)

    def endiri(self):
        try:
            os.chdir(self.yol+'\\Endirilənlər')
            self.dizin=QFileDialog.getOpenFileName(self, 'Endirilənlər',os.getcwd())
            os.popen(self.dizin[0])
        except Exception as e:
            os.chdir(self.yol)           
            QMessageBox.critical(self, "Error","Downloads folder does not exist !")
            s=str(e)
            print("Pencere2_endiri"+s)
            
    def sifahi(self):
        try:
            self.nez.hide()
            self.nez_lab.hide()
            self.aid.hide()
            self.aid_lab.hide()
            self.cvb_ind.hide()
            self.cvb_ind_lab.hide()
            self.derk.hide()
            self.derk_lab.hide()
            self.formasi.hide()
            self.formasi_lab.hide()
            self.yolu.hide()
            self.yolu_lab.hide()
            self.sexs.hide()
            self.sexs_lab.hide()
            self.evvel.hide()
            self.evvel_lab.hide()
            self.gonderen.hide()
            self.gonderen_lab.hide()
            self.vereq.hide()
            self.vereq_lab.hide()
            self.erize_yukle.hide()
            self.cavab_yukle.hide()
        except Exception as e:
            s=str(e)
            print("Pencere2_sifahi"+s)

            
    def yazili(self):
        try:
            self.nez.show()
            self.nez_lab.show()
            self.aid.show()
            self.aid_lab.show()
            self.cvb_ind.show()
            self.cvb_ind_lab.show()
            self.derk.show()
            self.derk_lab.show()
            self.formasi.show()
            self.formasi_lab.show()
            self.yolu.show()
            self.yolu_lab.show()
            self.sexs.show()
            self.sexs_lab.show()
            self.evvel.show()
            self.evvel_lab.show()
            self.gonderen.show()
            self.gonderen_lab.show()
            self.vereq.show()
            self.vereq_lab.show()
            self.erize_yukle.show()
            self.cavab_yukle.show()
        except Exception as e:
            s=str(e)
            print("Pencere2_yazili"+s)

    def elektron(self):
        try:
            self.nez.show()
            self.nez_lab.show()
            self.aid.show()
            self.aid_lab.show()
            self.cvb_ind.show()
            self.cvb_ind_lab.show()
            self.derk.show()
            self.derk_lab.show()
            self.formasi.show()
            self.formasi_lab.show()
            self.yolu.show()
            self.yolu_lab.show()
            self.sexs.show()
            self.sexs_lab.show()
            self.evvel.show()
            self.evvel_lab.show()
            self.gonderen.show()
            self.gonderen_lab.show()
            self.vereq.show()
            self.vereq_lab.show()
            self.erize_yukle.show()
            self.cavab_yukle.show()
        except Exception as e:
            s=str(e)
            print("Pencere2_elektron"+s)

    def evvelde(self):
        try:

            self.metn=''
            self.evv=[]
            if len(self.fin.text())==7:
                self.metni=self.cur.execute("""select daxil_no from sifahi where fin=(?) """,(self.fin.text(),))        
                self.metni1=self.metni.fetchall()
                for i in self.metni1:
                    self.evv.append(str(i[0]).strip()+"-Şifahi")

                self.metnr=self.cur.execute("""select daxil_no from yazili where fin=(?) """,(self.fin.text(),))
                self.metnr1=self.metnr.fetchall()
                for i in self.metnr1:
                    self.evv.append(str(i[0]).strip()+"-Yazılı")

                self.metno=self.cur.execute("""select daxil_no from elektron where fin=(?) """,(self.fin.text(),))
                self.metno1=self.metno.fetchall()
                for i in self.metno1:
                    self.evv.append(str(i[0]).strip()+"-Elektron")
            self.evvel.addItems(self.evv)
            
        except Exception as e:
            s=str(e)
            print("Pencere2_evvelde"+s)


    def esas(self):
        try:
            muraciet_ekran.hide()
            ana_ekran.show()
        except Exception as e:
            s=str(e)
            print("Pencere2_esas"+s)

    def legv(self):
        try:
            self.sira_no.setText("")
            self.daxil_no.setText("")
            self.ad.setText("")
            self.fin.setText("")
            self.mezmun.setText("")
            self.aid.setText("")
            self.cvb_mzm.setText("")
            self.cvb_trx.setText("")
            self.cvb_ind.setText("")
            self.sexs.setText("")
            self.gonderen.setText("")
            self.unv.setText("")
            self.tel.setText("")
            self.vereq.setText("")
            self.evv=[]
            self.evvel.clear()        
        except Exception as e:
            s=str(e)
            print("Pencere2_legv"+s)

    def er_yukle(self):
        os.chdir(sened_yolu+"\\Sənədlər")
        try:
            self.tr=0
            try:
                self.tr=1
            except ValueError:
                self.tr=0
            if self.daxil_no.text()=="" :
                QMessageBox.information(self, "Information","Registration number cannot be empty!")
            elif str(self.input_no.text()) in self.yazililist:
                QMessageBox.information(self, "Information","Another request has been entered with this Registration number!")
                self.input_no.setText("")
            elif not self.vereq.text().isnumeric():
                QMessageBox.information(self, "Information","The sheet number section cannot contain letters!")
            elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                QMessageBox.information(self, "Information","First name, last name cannot be empty or contain numbers!")
            elif not self.fin.text()=='' and not len(self.fin.text())==7 :
                QMessageBox.information(self, "Information","Enter your FIN number correctly!")
            elif len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                QMessageBox.information(self, "Information","Enter the correct phone number!")
            #elif self.cvb_mzm.toPlainText()== "" :
                #QMessageBox.information(self, "Information","The content of the request response cannot be empty ")
            #elif self.tr==0:
                #QMessageBox.information(self, "Information","Enter reply date in correct format ")
            #elif self.cvb_ind.text()== "" :
                #QMessageBox.information(self, "Information","Reply index section cannot be empty ")                
            #elif self.aid.toPlainText()== "" :
                #QMessageBox.information(self, "Information","Subject cannot be empty ")
            elif self.sexs.text()== "" :
                QMessageBox.information(self, "Information","Enter Recipient Name")                
            #elif self.gonderen.toPlainText()== "" :
                #QMessageBox.information(self, "Məlumat","Müşaiyət məktubunu göndərən şəxsin adını daxil edin ")
            else:
                import shutil
                
                try:
                    path=document_path+"\\Documents"
                    os.chdir(path)
                    direct=os.listdir(os.getcwd())
                unless:
                    QMessageBox.information(self, "Information","Documents folder does not exist")                
                if self.sira_no.text() not in direct:
                    os.mkdir(self.sira_no.text())
                    os.chdir(os.getcwd()+"/"+self.sira_no.text())
                    os.mkdir("Applications")
                    os.mkdir("Answers")
                    os.chdir(self.yol)
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialogfiles, _ = QFileDialog.getOpenFileNames(self,"Upload application file", "","All files (*);;MS WORD files (*.docx)", options=options)                                   
                source = files[0]
                if files[0][-4]=='.':
                    destination = path+'\\'+self.sira_no.text()+"/Applications/"+self.ad.toPlainText()+files[0][-4:]
                otherwise:
                    destination = path+'\\'+self.sira_no.text()+"/Applications/"+self.ad.toPlainText()+files[0][-5:]

                try:
                    shutil.copy(source, destination)
                    QMessageBox.information(self, "Information","Application file uploaded successfully ")         
                except shutil.SameFileError:
                    QMessageBox.information(self, "Information","This document has already been loaded ")
                except PermissionError:
                    QMessageBox.information(self, "Information","You do not have permission for this operation ")
                unless:
                    QMessageBox.information(self, "Information","An error occurred")
        except Exception as e:
            s=str(e)
            print("Pencere2_er_yukle"+s)
        os.chdir(self.yol)
    def cvb_yukle(self):
        os.chdir(sened_yolu+"\\Sənədlər")
        try:
            self.tr=0
            try:

                self.tr=1
            except ValueError:
                self.tr=0

if self.input_no.text()=="" :
                QMessageBox.information(self, "Information","Registration number cannot be empty!")
            elif str(self.input_no.text()) in self.yazililist:
                QMessageBox.information(self, "Information","Another request has been entered with this Registration number!")
                self.input_no.setText("")
            elif not self.vereq.text().isnumeric():
                QMessageBox.information(self, "Information","The sheet number section cannot contain letters!")
            elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                QMessageBox.information(self, "Information","First name, last name cannot be empty or contain numbers!")
            elif not self.fin.text()=='' and not len(self.fin.text())==7 :
                QMessageBox.information(self, "Information","Enter your FIN number correctly!")
            elif len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                QMessageBox.information(self, "Information","Enter the correct phone number!")
            #elif self.cvb_mzm.toPlainText()== "" :
                #QMessageBox.information(self, "Information","The content of the request response cannot be empty ")
            #elif self.tr==0:
                #QMessageBox.information(self, "Information","Enter reply date in correct format ")
            #elif self.cvb_ind.text()== "" :
                #QMessageBox.information(self, "Information","Reply index section cannot be empty ")                
            #elif self.aid.toPlainText()== "" :
                #QMessageBox.information(self, "Information","Subject cannot be empty ")
            elif self.sexs.text()== "" :
                QMessageBox.information(self, "Information","Enter Recipient Name")                
            #elif self.gonderen.toPlainText()== "" :
                #QMessageBox.information(self, "Information","Enter the name of the person sending the cover letter ")
            otherwise:                import shutil
                os.chdir(self.yol)
                try:
                    yolu=sened_yolu+"\\Sənədlər"
                    os.chdir(yolu)
                    direk=os.listdir(os.getcwd())
                except:
                    QMessageBox.information(self, "Information","Documents folder does not exist")                
                if self.sira_no.text() not in direct:
                    os.mkdir(self.sira_no.text())
                    os.chdir(os.getcwd()+"\\"+self.sira_no.text())
                    os.mkdir("Applications")
                    os.mkdir("Answers")
                    os.chdir(self.path)
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                files, _ = QFileDialog.getOpenFileNames(self,"Load answer file", "","All files (*);;MS WORD files (*.docx)", options=options)                                   
                source = files[0]                if files[0][-4]=='.':
                    destination = path+'\\'+self.sira_no.text()+"/Answers/"+self.ad.toPlainText()+files[0][-4:]
                    otherwise:
                    destination = path+'\\'+self.sira_no.text()+"/Answers/"+self.ad.toPlainText()+files[0][-5:]

                try:
                    shutil.copy(source, destination)
                    QMessageBox.information(self, "Information","Response file uploaded successfully ")         
                except shutil.SameFileError:
                    QMessageBox.information(self, "Information","This document has already been loaded ")
                except PermissionError:
                    QMessageBox.information(self, "Information","You do not have permission for this operation ")
                unless:
                    QMessageBox.information(self, "Information","An error occurred")  
        except Exception as e:
            s=str(e)
            print("Pencere2_cava_yukle"+s)
        os.chdir(self.yol)    
    def qeydd(self):
        try:
            self.tr=0
            try:

                self.tr=1
            except ValueError:
                self.tr=0

            self.evvelde()
            if self.radiobutton.isChecked():

                if self.daxil_no.text()=="":
                    QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş ola bilməz !")

                elif str(self.daxil_no.text()) in self.sifahilist:
                    QMessageBox.information(self, "Məlumat","Bu Qeydiyyat nömrəsi ilə başqa müraciət daxil edilib !")
                    self.daxil_no.setText("")

                    
                elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                    QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")

                elif not  self.fin.text()=="" and not len(self.fin.text())==7 :
                    QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")

                elif  len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                    
                    QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")

                elif self.unv.text()=="" :
                    QMessageBox.information(self, "Məlumat","Ünvan bölməsinə yaşayış yerini daxil edin")
                else:
                    try:
                        self.cur.execute ("""INSERT INTO sifahi(sıra_no,daxil_no,tarix,vereq,ad_soyad,fin,tel,unvan,novu,xarakteri,netice,mezmun,icraci,for,cvb_mezmun,cvb_tarix,qeyd_eden,son_deyisdiren)
                                VALUES 
                                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(self.sira_no.text(),self.daxil_no.text(),self.tarix.text(),self.vereq.text(),self.ad.toPlainText(),self.fin.text(),self.tel.text(),self.unv.text(),self.nov.currentText(),self.xar.currentText(),self.netice.currentText(),self.mezmun.toPlainText(),self.icra.currentText(),"Şifahi",self.cvb_mzm.toPlainText(),self.cvb_trx.text(),ana_ekran.user,ana_ekran.user))
                        self.con.commit()
                        QMessageBox.information(self, "Məlumat","Şifahi müraciət qeydə alındı")
                        ana_ekran.ss.setText("Şifahi müraciət sayı:".ljust(27," ")+ str(ana_ekran.sifahisay+1))
                        ana_ekran.baxilmamis.setText("Baxılmamış müraciət sayı:".ljust(27," ")+ str(ana_ekran.baxilmamissay+1))
                        
                    except Exception as e:
                        s = str(e)
                        print(s)
                        QMessageBox.information(self, "Məlumat","Şifahi müraciət qeydə alınmadı !")
                    
            elif self.radiobutton1.isChecked():

             
                if self.daxil_no.text()=="" :
                    QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş ola bilməz !")
            
                elif str(self.daxil_no.text()) in self.yazililist:
                    QMessageBox.information(self, "Məlumat","Bu Qeydiyyat nömrəsi ilə başqa müraciət daxil edilib !")
                    self.daxil_no.setText("")


                elif  not self.vereq.text().isnumeric():
                    QMessageBox.information(self, "Məlumat","Vərəq sayı bölməsi hərflərdən ibarət ola bilməz !")


                elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                    QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")

                elif  not self.fin.text()=="" and  not len(self.fin.text())==7 :
                    QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
               

                elif len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                    QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")

       
                #elif self.cvb_mzm.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müraciətə verilən cavabın məzmunu boş ola bilməz ")

                #elif self.tr==0:
                    #QMessageBox.information(self, "Məlumat","Cavab tarixini düzgün formatda daxil edin ")

                #elif self.cvb_ind.text()== "" :
                    #QMessageBox.information(self, "Məlumat","Cavab indeksi bölməsi boş ola bilməz ")
          
                #elif self.aid.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Aidiyət bölməsi boş ola bilməz ")


                elif self.sexs.text()== "" :
                    QMessageBox.information(self, "Məlumat","Müraciət ünvanlanan şəxsin adını daxil edin")
                    
                #elif self.gonderen.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müşaiyət məktubunu göndərən şəxsin adını daxil edin ")


                else:
                    try:
                        self.cur.execute ("""INSERT INTO yazili(sira_no,daxil_no,tarix,ad_soyad,fin,unvan,tel,vereqsay,nov,forması,yolu,kime,musaiyet,xarakteri,mezmun,derkenar,icraci,cvb_tarix,cvb_mezmun,cvb_indeksi,aidiyyat,nezaret,netice,for,qeyd_eden,son_deyisdiren)
                                VALUES 
                                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(self.sira_no.text(),
                                                                                self.daxil_no.text(),
                                                                                self.tarix.text(),
                                                                                self.ad.toPlainText(),
                                                                                self.fin.text(),
                                                                                self.unv.text(),
                                                                                self.tel.text(),
                                                                                self.vereq.text(),
                                                                                self.nov.currentText(),
                                                                                self.formasi.currentText(),
                                                                                self.yolu.currentText(),
                                                                                self.sexs.text(),
                                                                                self.gonderen.toPlainText(),
                                                                                self.xar.currentText(),
                                                                                self.mezmun.toPlainText(),
                                                                                self.derk.currentText(),
                                                                                self.icra.currentText(),
                                                                                self.cvb_trx.text(),
                                                                                self.cvb_mzm.toPlainText(),
                                                                                self.cvb_ind.text(),
                                                                                self.aid.toPlainText(),
                                                                                self.nez.currentText(),
                                                                                self.netice.currentText(),"Yazılı",ana_ekran.user,ana_ekran.user))
                        self.con.commit()
                        QMessageBox.information(self, "Məlumat","Yazılı müraciət qeydə alındı")
                        ana_ekran.ys.setText("Yazılı müraciət sayı:".ljust(27," ")+ str(ana_ekran.yazilisay+1))
                        ana_ekran.baxilmamis.setText("Baxılmamış müraciət sayı:".ljust(27," ")+ str(ana_ekran.baxilmamissay+1))
     
                    except Exception as e:
                        s=str(e)
                        print("Pencere2_qeydd"+s)
                        QMessageBox.information(self, "Məlumat","Yazılı müraciət qeydə alınmadı !")


            elif  self.radiobutton2.isChecked():
                if self.daxil_no.text()=="" :
                    QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş ola bilməz !")

                elif str(self.daxil_no.text()) in self.elektronlist:
                    QMessageBox.information(self, "Məlumat","Bu Qeydiyyat nömrəsi ilə başqa müraciət daxil edilib !")
                    self.daxil_no.setText("")


                elif  not self.vereq.text().isnumeric():
                    QMessageBox.information(self, "Məlumat","Vərəq sayı bölməsi hərflərdən ibarət ola bilməz !")


                elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                    QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")

                elif  not self.fin.text()=="" and not len(self.fin.text())==7 :
                    QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
               

                elif  len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                    QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")


                #elif self.cvb_mzm.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müraciətə verilən cavabın məzmunu boş ola bilməz ")

                #elif self.tr==0:
                    #QMessageBox.information(self, "Məlumat","Cavab tarixini düzgün formatda daxil edin ")

                #elif self.cvb_ind.text()== "" :
                    #QMessageBox.information(self, "Məlumat","Cavab indeksi bölməsi boş ola bilməz ")
                    
                #elif self.aid.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Aidiyət bölməsi boş ola bilməz ")


                elif self.sexs.text()== "" :
                    QMessageBox.information(self, "Məlumat","Müraciət ünvanlanan şəxsin adını daxil edin")
                    
                #elif self.gonderen.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müşaiyət məktubunu göndərən şəxsin adını daxil edin ")


                else:
                    try:
                        self.cur.execute ("""INSERT INTO elektron(sira_no,daxil_no,tarix,ad_soyad,fin,unvan,tel,vereqsay,nov,forması,yolu,kime,musaiyet,xarakteri,mezmun,derkenar,icraci,cvb_tarix,cvb_mezmun,cvb_indeksi,aidiyyat,nezaret,netice,for,qeyd_eden,son_deyisdiren)
                                VALUES 
                                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(self.sira_no.text(),self.daxil_no.text(),
                                                                                self.tarix.text(),
                                                                                self.ad.toPlainText(),
                                                                                self.fin.text(),
                                                                                self.unv.text(),
                                                                                self.tel.text(),
                                                                                self.vereq.text(),
                                                                                self.nov.currentText(),
                                                                                self.formasi.currentText(),
                                                                                self.yolu.currentText(),
                                                                                self.sexs.text(),
                                                                                self.gonderen.toPlainText(),
                                                                                self.xar.currentText(),
                                                                                self.mezmun.toPlainText(),
                                                                                self.derk.currentText(),
                                                                                self.icra.currentText(),
                                                                                self.cvb_trx.text(),
                                                                                self.cvb_mzm.toPlainText(),
                                                                                self.cvb_ind.text(),
                                                                                self.aid.toPlainText(),
                                                                                self.nez.currentText(),
                                                                                self.netice.currentText(),"Elektron",ana_ekran,ana_ekran))
                        self.con.commit()
                        QMessageBox.information(self, "Məlumat","Elektron müraciət qeydə alındı")
                        ana_ekran.es.setText("Elektron müraciət sayı:".ljust(27," ")+ str(ana_ekran.elektronsay+1))
                        ana_ekran.baxilmamis.setText("Baxılmamış müraciət sayı:".ljust(27," ")+ str(ana_ekran.baxilmamissay+1))

                        
                    except Exception as e:
                        s=str(e)
                        print("Pencere2_qeydd"+s)
                        QMessageBox.information(self, "Məlumat","Elektron müraciət qeydə alınmadı !")


                        
        except Exception as e:
            s=str(e)
            print("Pencere2_qeydd"+s)


    def sened (self):
        try:
            self.tr=0
            try:

                self.tr=1
            except ValueError:
                self.tr=0

            if self.radiobutton.isChecked():

                if self.daxil_no.text()=="" :
                    QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş ola bilməz !")

                elif str(self.daxil_no.text()) in self.sifahilist:
                    QMessageBox.information(self, "Məlumat","Bu Qeydiyyat nömrəsi ilə başqa müraciət daxil edilib !")
                    self.daxil_no.setText("")
                    
                elif  self.vereq.text().isnumeric():
                    QMessageBox.information(self, "Məlumat","Vərəq sayı bölməsi hərflərdən ibarət ola bilməz !")

                elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                    QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")

                elif  self.fin.text()=='' and not len(self.fin.text())==7 :
                    QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
                elif  len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                    QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")

                #elif self.unv.text()=="" :
                    #QMessageBox.information(self, "Məlumat","Ünvan bölməsinə yaşayış yerini daxil edin")

                else:
                    try:
                        self.ev=''
                        for i in self.evv:
                            self.ev= self.ev + i +","
                        self.template = self.yol+"\\resurslar\\sablon.docx"
                        self.document = MailMerge(self.template)
                        self.document.merge(
                            formasi=self.formasi.currentText(),
                            novu=self.nov.currentText(),
                            daxil_no=self.daxil_no.text(),
                            sira_no=self.sira_no.text(),
                            tarixi=gunu,
                            ad_soyad=self.ad.toPlainText(),
                            fin_no=self.fin.text(),
                            unvan=self.unv.text(),
                            telefon=self.tel.text(),
                            yolu=self.yolu.currentText(),
                            vereq=self.vereq.text(),
                            xarakteri=self.xar.currentText(),
                            icraci=self.icra.currentText(),
                            derkenar=self.derk.currentText(),
                            nezaret=self.nez.currentText(),
                            aidiyyat=self.aid.toPlainText(),
                            sexs=self.sexs.text(),
                            evvelki=self.ev,
                            musaiyet=self.gonderen.toPlainText(),
                            neticesi=self.netice.currentText(),
                            cvb_tarixi=self.cvb_trx.text(),
                            cvb_indeksi=self.cvb_ind.text(),
                            mur_mezmun=self.mezmun.toPlainText(),
                            cvb_mezmun=self.cvb_mzm.toPlainText(),
                            rap_tarix=gunu,
                            form="şifahi")
                        self.document.write(self.yol+'/Endirilənlər/Şifahi/'+self.sira_no.text()+'.docx')
                        QMessageBox.information(self, "Məlumat","Şifahi müraciət yükləndi.")
                    except Exception as e:
                        s=str(e)
                        print(s)
                        QMessageBox.information(self, "Məlumat","Şifahi müraciət yüklənmədi")
                    
            elif self.radiobutton1.isChecked():
                
                if self.daxil_no.text()=="":
                    QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş və ya hərflərdən ibarət ola bilməz !")

                elif str(self.daxil_no.text()) in self.yazililist:
                    QMessageBox.information(self, "Məlumat","Bu Qeydiyyat nömrəsi ilə başqa müraciət daxil edilib !")
                    self.daxil_no.setText("")


                elif  not self.vereq.text().isnumeric():
                    QMessageBox.information(self, "Məlumat","Vərəq sayı bölməsi hərflərdən ibarət ola bilməz !")


                elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                    QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")

                elif  not self.fin.text()=="" and not len(self.fin.text())==7 :
                    QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
               

                elif len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                    QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")


                #elif self.cvb_mzm.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müraciətə verilən cavabın məzmunu boş ola bilməz ")

                #elif self.tr==0:
                    #QMessageBox.information(self, "Məlumat","Cavab tarixini düzgün formatda daxil edin ")

                #elif self.cvb_ind.text()== "" :
                    #QMessageBox.information(self, "Məlumat","Cavab indeksi bölməsi boş ola bilməz ")
                    
                #elif self.aid.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Aidiyət bölməsi boş ola bilməz ")


                elif self.sexs.text()== "" :
                    QMessageBox.information(self, "Məlumat","Müraciət ünvanlanan şəxsin adını daxil edin")
                    
                #elif self.gonderen.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müşaiyət məktubunu göndərən şəxsin adını daxil edin ")


                else:
                    try:
                        self.ev=''
                        for i in self.evv:
                            self.ev= self.ev + i +","
                        self.template = self.yol+"\\resurslar\\sablon.docx"
                        self.document = MailMerge(self.template)
                        self.document.merge(
                            formasi=self.formasi.currentText(),
                            novu=self.nov.currentText(),
                            daxil_no=self.daxil_no.text(),
                            sira_no=self.sira_no.text(),
                            tarixi=gunu,
                            ad_soyad=self.ad.toPlainText(),
                            fin_no=self.fin.text(),
                            unvan=self.unv.text(),
                            telefon=self.tel.text(),
                            yolu=self.yolu.currentText(),
                            vereq=self.vereq.text(),
                            xarakteri=self.xar.currentText(),
                            icraci=self.icra.currentText(),
                            derkenar=self.derk.currentText(),
                            nezaret=self.nez.currentText(),
                            aidiyyat=self.aid.toPlainText(),
                            sexs=self.sexs.text(),
                            evvelki=self.ev,
                            musaiyet=self.gonderen.toPlainText(),
                            neticesi=self.netice.currentText(),
                            cvb_tarixi=self.cvb_trx.text(),
                            cvb_indeksi=self.cvb_ind.text(),
                            mur_mezmun=self.mezmun.toPlainText(),
                            cvb_mezmun=self.cvb_mzm.toPlainText(),
                            rap_tarix=gunu,
                            form="yazılı")
                        self.document.write(self.yol+'/Endirilənlər/Yazılı/'+self.sira_no.text()+'.docx')
                        QMessageBox.information(self, "Məlumat","Yazılı müraciət yükləndi.")
                    except Exception as e:
                        s=str(e)
                        print(s)
                        QMessageBox.information(self, "Məlumat","Yazılı müraciət yüklənmədi")


            elif  self.radiobutton2.isChecked():
                if self.daxil_no.text()=="" :
                    QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş ola bilməz !")

                elif str(self.daxil_no.text()) in self.elektronlist:
                    QMessageBox.information(self, "Məlumat","Bu Qeydiyyat nömrəsi ilə başqa müraciət daxil edilib !")
                    self.daxil_no.setText("")


                elif  not self.vereq.text().isnumeric():
                    QMessageBox.information(self, "Məlumat","Vərəq sayı bölməsi hərflərdən ibarət ola bilməz !")


                elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                    QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")

                elif  not self.fin.text()=='' and not len(self.fin.text())==7 :
                    QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
               

                elif  len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                    QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")


                #elif self.cvb_mzm.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müraciətə verilən cavabın məzmunu boş ola bilməz ")

                #elif self.tr==0:
                    #QMessageBox.information(self, "Məlumat","Cavab tarixini düzgün formatda daxil edin ")

                #elif self.cvb_ind.text()== "" :
                    #QMessageBox.information(self, "Məlumat","Cavab indeksi bölməsi boş ola bilməz ")
                    
                #elif self.aid.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Aidiyət bölməsi boş ola bilməz ")


                elif self.sexs.text()== "" :
                    QMessageBox.information(self, "Məlumat","Müraciət ünvanlanan şəxsin adını daxil edin")
                    
                #elif self.gonderen.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müşaiyət məktubunu göndərən şəxsin adını daxil edin ")


                else:
                    try:
                        self.ev=''
                        for i in self.evv:
                            self.ev= self.ev + i +","
                        self.template = self.yol+"\\resurslar\\sablon.docx"
                        self.document = MailMerge(self.template)
                        self.document.merge(
                            formasi=self.formasi.currentText(),
                            novu=self.nov.currentText(),
                            daxil_no=self.daxil_no.text(),
                            sira_no=self.sira_no.text(),
                            tarixi=gunu,
                            ad_soyad=self.ad.toPlainText(),
                            fin_no=self.fin.text(),
                            unvan=self.unv.text(),
                            telefon=self.tel.text(),
                            yolu=self.yolu.currentText(),
                            vereq=self.vereq.text(),
                            xarakteri=self.xar.currentText(),
                            icraci=self.icra.currentText(),
                            derkenar=self.derk.currentText(),
                            nezaret=self.nez.currentText(),
                            aidiyyat=self.aid.toPlainText(),
                            sexs=self.sexs.text(),
                            evvelki=self.ev,
                            musaiyet=self.gonderen.toPlainText(),
                            neticesi=self.netice.currentText(),
                            cvb_tarixi=self.cvb_trx.text(),
                            cvb_indeksi=self.cvb_ind.text(),
                            mur_mezmun=self.mezmun.toPlainText(),
                            cvb_mezmun=self.cvb_mzm.toPlainText(),
                            rap_tarix=gunu,
                            form="elektron")
                        self.document.write(self.yol+'/Endirilənlər/Elektron/'+self.sira_no.text()+'.docx')
                        QMessageBox.information(self, "Məlumat","Elektron müraciət yükləndi.")
                    except:
                        QMessageBox.information(self, "Məlumat","Elektron müraciət yüklənmədi")
        except Exception as e:
            s=str(e)
            print("Pencere2_sened"+s)


    def yoxla(self):
        try:
            self.sifahilist=[]
            self.yazililist=[]
            self.elektronlist=[]
            
            self.yoxs=self.cur.execute("""select daxil_no from sifahi""")        
            self.yoxs1=self.yoxs.fetchall()
            for i in self.yoxs1:
                self.sifahilist.append(str(i[0]).strip())

            self.yoxy=self.cur.execute("""select daxil_no from yazili""")        
            self.yoxy1=self.yoxy.fetchall()
            for i in self.yoxy1:
                self.yazililist.append(str(i[0]).strip())
            
            self.yoxe=self.cur.execute("""select daxil_no from elektron""")        
            self.yoxe1=self.yoxe.fetchall()
            for i in self.yoxe1:
                self.elektronlist.append(str(i[0]).strip())
        except Exception as e:
            s=str(e)
            print("Pencere2_yoxla"+s)

    def printet(self):
        if  self.radiobutton.isChecked():
            os.chdir(self.yol+"/Endirilənlər/Şifahi")
        elif  self.radiobutton1.isChecked():
            os.chdir(self.yol+"/Endirilənlər/Yazılı")       
        elif  self.radiobutton2.isChecked():
            os.chdir(self.yol+"/Endirilənlər/Elektron")   
        print(os.getcwd())
        senedler=os.listdir()
        if not self.daxil_no.text()+".docx" in senedler:
            self.sened()


        try:
            convert(self.daxil_no.text()+'.docx', self.daxil_no.text()+'.pdf')
            def get_adobe_executable():
                with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as conn:
                    with winreg.OpenKey(conn, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\AcroRd32.exe', 0, winreg.KEY_READ) as hkey:
                        value = winreg.QueryValue(hkey, None)
                        if value:
                            value = '"{}"'.format(value)
                            return value.strip()
                return None

            def print_pdf_file(file, printer_name=None, secs=5):
                cmd = get_adobe_executable()
                if cmd is None:
                    return False
                if printer_name:
                    cmd = '{} /h /t "{}" "{}"'.format(cmd, file, printer_name)
                else:
                    cmd = '{} /p /h "{}"'.format(cmd, file)
                proc = subprocess.Popen(cmd)
                time.sleep(secs)
                proc.kill()
                print_pdf_file(self.daxil_no.text()+'.pdf')
        except Exception as e:
            s=str(e)
            print("Pencere2_printet"+s)

###################################################################################################################################################################

class Pencere3(QWidget):
    def __init__(self):
        try:
            super().__init__()
            self.setFixedSize(850,700)
            qtRectangle = self.frameGeometry()
            centerPoint = QDesktopWidget().availableGeometry().center()
            qtRectangle.moveCenter(centerPoint)
            self.move(qtRectangle.topLeft())
            self.setStyleSheet("background-color:#6c2cc;")
            self.setWindowTitle("Müraciət sorğusu")
            self.formas=""

            self.adi=""
            self.finn=""
            self.unv=""
            self.tell=""
            self.vereq=""
            self.novun=""
            self.formasi=""
            self.yolu=""
            self.sexs=""
            self.gonderen=""
            self.xar=""
            self.mezmun=''
            self.derk=''
            self.cvb_trx=''
            self.cvb_mzm=''
            self.cvb_ind=''
            self.aid=''
            self.nez=''
            self.netice=''       
            self.yol=os.getcwd()
            self.bazayol=esas_baza
            self.senedi=[]
            try:
                self.con = sqlite3.connect(self.bazayol+"\\baza.db")
                self.cur = self.con.cursor()
                os.chdir(self.yol)
            except:
                QMessageBox.information(self, "Məlumat","Verilənlər bazası mövcud deyil !")
                sys.exit()

            self.ad = QTextEdit(self)
            self.ad.move(110, 20)
            self.ad.resize(150,23)
            self.ad.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.ad_lab = QLabel(self)
            self.ad_lab.move(10, 20)
            self.ad_lab.resize(75,25)
            self.ad_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.ad_lab.setText("Ad,soyad")
            self.ad.setEnabled(True)

            self.radiobutton = QRadioButton(self)
            self.radiobutton.setText("Şifahi müraciətlər")
            self.radiobutton.setChecked(False)
            self.radiobutton.setStyleSheet("font-family: Arial;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.radiobutton.move(30, 190)
            self.radiobutton.toggled.connect(self.radioclick)

            self.radiobutton1 = QRadioButton(self)
            self.radiobutton1.setText("Yazılı müraciətlər")
            self.radiobutton1.setChecked(True)
            self.radiobutton1.setStyleSheet("font-family: Arial;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.radiobutton1.move(240, 190)
            self.radiobutton1.toggled.connect(self.radioclick1)

            self.radiobutton2 = QRadioButton(self)
            self.radiobutton2.setText("Elektron müraciətlər")
            self.radiobutton2.setChecked(False)
            self.radiobutton2.setStyleSheet("font-family: Arial;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.radiobutton2.move(450, 190)
            self.radiobutton2.toggled.connect(self.radioclick2)


            self.tarix1 = QDateEdit(self)
            self.tarix1.move(110, 60)
            self.tarix1.resize(110,23)
            self.tarix1.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.tarix1_lab = QLabel(self)
            self.tarix1_lab.move(10, 60)
            self.tarix1_lab.resize(100,25)
            self.tarix1_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.tarix1_lab.setText("Başlanğıc tarix")
            self.tarix1.setDate(QDate.currentDate())
     
            self.tarix2= QDateEdit(self)
            self.tarix2.move(440, 60)
            self.tarix2.resize(110,23)
            self.tarix2.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.tarix2_lab = QLabel(self)
            self.tarix2_lab.move(290, 60)
            self.tarix2_lab.resize(110,25)
            self.tarix2_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.tarix2_lab.setText("Son tarix")
            self.tarix2.setDate(QDate.currentDate())
     

            self.xar = QComboBox(self)
            self.xar.move(160, 105)
            self.xar.resize(680,28)
            self.xar.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.xar.addItems(muraciet_ekran.xarakteri)
            self.xar_lab = QLabel(self)
            self.xar_lab.move(10, 105)
            self.xar_lab.resize(140,30)
            self.xar_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.xar_lab.setText("Müraciətin xarakteri")

            
            self.fin = QLineEdit(self)
            self.fin.move(700, 22)
            self.fin.resize(110,23)
            self.fin.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.fin_lab = QLabel(self)
            self.fin_lab.move(610, 22)
            self.fin_lab.resize(120,25)
            self.fin_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.fin_lab.setText("FİN nömrəsi")        

            self.daxil_no = QLineEdit(self)
            self.daxil_no.move(440, 22)
            self.daxil_no.resize(110,23)
            self.daxil_no.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.daxil_no_lab = QLabel(self)
            self.daxil_no_lab.move(290, 22)
            self.daxil_no_lab.resize(120,25)
            self.daxil_no_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 10pt;font-weight: bold;color : black;")
            self.daxil_no_lab.setText("Qeydiyyat nömrəsi")

            self.axtar=QPushButton(self)
            self.axtar.resize(200,25)
            self.axtar.move(10,150)
            self.axtar.clicked.connect(self.axtar_duyme)
            self.axtar.setText("Verilənlərə görə axtar")
            self.axtar.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 10pt;font-weight: bold;color : black;")

          
            self.qayittt=QPushButton(self)
            self.qayittt.resize(200,25)
            self.qayittt.move(220,150)
            self.qayittt.setText("Əsas menyuya qayıt")
            self.qayittt.clicked.connect(self.evvelki)
            self.qayittt.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 10pt;font-weight: bold;color : black;")

            self.bos=QPushButton(self)
            self.bos.resize(200,25)
            self.bos.move(430,150)
            self.bos.setText("Sənədlər qovluğu")          
            self.bos.clicked.connect(self.senedler)
            self.bos.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 10pt;font-weight: bold;color : black;")


            self.tra=QPushButton(self)
            self.tra.resize(200,25)
            self.tra.move(610,60)
            self.tra.setText("Tarixə görə axtar")          
            self.tra.clicked.connect(self.traa)
            self.tra.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 10pt;font-weight: bold;color : black;")


            self.cercive1=QFrame(self)
            self.cercive1.move(0,50)
            self.cercive1.resize(850,1)
            self.cercive1.setStyleSheet("background-color : blue")
            
            self.cercive1=QFrame(self)
            self.cercive1.move(0,95)
            self.cercive1.resize(850,1)
            self.cercive1.setStyleSheet("background-color : blue")

            self.cercive1=QFrame(self)
            self.cercive1.move(0,140)
            self.cercive1.resize(850,1)
            self.cercive1.setStyleSheet("background-color : blue")

            self.cercive1=QFrame(self)
            self.cercive1.move(0,185)
            self.cercive1.resize(850,1)
            self.cercive1.setStyleSheet("background-color : blue")

            
            self.tableWidget = QTableWidget(self)
            self.tableWidget.move(1,220)
            self.tableWidget.resize(848,510)
            self.tableWidget.resizeColumnsToContents() 
            self.tableWidget.setColumnCount(8)
            self.columns = ['Sıra no','Qeydiyyat no','Tarixi','Ad,soyad','FİN','İcraçısı','Telefon','Müraciət forması']
            self.radiobutton.toggled.connect(self.radioclick)
            self.radiobutton1.toggled.connect(self.radioclick1)
            self.radiobutton2.toggled.connect(self.radioclick2)

            self.tableWidget.setHorizontalHeaderLabels(self.columns)
        except Exception as e:
            s=str(e)
            print("Pencere3_init"+s)

    def yenile(self):
        try:
            for i in range(5000):
                for j in range(8):
                    self.tableWidget.setItem(i,j, QTableWidgetItem(""))
        except Exception as e:
            s=str(e)
            print("Pencere3_yenile"+s)                

    def senedler(self):
        try:
            os.chdir(sened_yolu+'\\Sənədlər')
            self.dizin=QFileDialog.getOpenFileName(self, 'sənədlər dizinində olan qovluqlar',os.getcwd())
            os.popen(self.dizin[0])
        except Exception as e:
            os.chdir(self.yol)           
            QMessageBox.critical(self, "Səhv","Sənədlər qovluğu mövcud deyil !")
            s=str(e)
            print("Pencere3_yenile"+s)    

    def radioclick(self):
        self.yenile()

        self.umumi=[] 
        self.metn=''
        self.form=''
        self.form="Şifahi"
        self.metn=self.cur.execute ("""SELECT sıra_no,daxil_no,tarix,ad_soyad,fin,icraci,tel ,for from sifahi """)
        self.metn1=self.metn.fetchall()                    
        for i in self.metn1:
            self.umumi.append(i)
        self.setir=len(self.umumi)+1
        self.tableWidget.setRowCount(self.setir)

        try:
            self.say1=0        
            for i in self.umumi:
                self.say2=0
                for j in i: 
                    self.tableWidget.setItem(self.say1,self.say2, QTableWidgetItem(str(j)))                
                    self.tableWidget.setColumnWidth(5, 100)
                    self.say2+=1
                self.say1+=1

            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)              
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.tableWidget.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch)
            self.tableWidget.setSortingEnabled(True)
            afont = QFont()
            afont.setFamily("Times New Roman")
            afont.setPointSize(9)
            self.tableWidget.horizontalHeaderItem(0).setFont(afont)
            self.tableWidget.horizontalHeaderItem(1).setFont(afont)
            self.tableWidget.horizontalHeaderItem(2).setFont(afont)
            self.tableWidget.horizontalHeaderItem(3).setFont(afont)
            self.tableWidget.horizontalHeaderItem(4).setFont(afont)
            self.tableWidget.horizontalHeaderItem(5).setFont(afont)
            self.tableWidget.horizontalHeaderItem(6).setFont(afont)
            self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))
            self.tableWidget.horizontalHeader().sectionResized.connect(self.tableWidget.resizeRowsToContents)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableWidget.doubleClicked.connect(self.klik)
        except Exception as e:
            s=str(e)
            print("Pencere3_radioclick"+s)

    def radioclick1(self):
        self.yenile()

        self.umumi=[] 
        self.metn=''
        self.form=''
        self.form="Yazılı"
        self.metn=self.cur.execute ("""SELECT sira_no,daxil_no,tarix,ad_soyad,fin,icraci,tel ,for from yazili  """)
        self.metn1=self.metn.fetchall()             
        for i in self.metn1:
            self.umumi.append(i)
        self.setir=len(self.umumi)+1
        self.tableWidget.setRowCount(self.setir)
        try:
            self.say1=0        
            for i in self.umumi:
                self.say2=0
                for j in i: 
                    self.tableWidget.setItem(self.say1,self.say2, QTableWidgetItem(str(j)))                
                    self.tableWidget.setColumnWidth(5, 100)
                    self.say2+=1
                self.say1+=1

            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)              
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.tableWidget.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch)
            self.tableWidget.setSortingEnabled(True)
            afont = QFont()
            afont.setFamily("Times New Roman")
            afont.setPointSize(9)
            self.tableWidget.horizontalHeaderItem(0).setFont(afont)
            self.tableWidget.horizontalHeaderItem(1).setFont(afont)
            self.tableWidget.horizontalHeaderItem(2).setFont(afont)
            self.tableWidget.horizontalHeaderItem(3).setFont(afont)
            self.tableWidget.horizontalHeaderItem(4).setFont(afont)
            self.tableWidget.horizontalHeaderItem(5).setFont(afont)
            self.tableWidget.horizontalHeaderItem(6).setFont(afont)
            self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))
            self.tableWidget.horizontalHeader().sectionResized.connect(self.tableWidget.resizeRowsToContents)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableWidget.doubleClicked.connect(self.klik)
        except Exception as e:
            s=str(e)
            print("Pencere3_radioclik1"+s)

    def radioclick2(self):
        self.yenile()


        self.umumi=[] 
        self.metn=''
        self.form=''

        self.form="Elektron"
        self.metn=self.cur.execute ("""SELECT sira_no,daxil_no,tarix,ad_soyad,fin,icraci,tel ,for from elektron""")
        self.metn1=self.metn.fetchall()             
        for i in self.metn1:
            self.umumi.append(i)
        self.setir=len(self.umumi)+1
        self.tableWidget.setRowCount(self.setir)
        try:
            self.say1=0        
            for i in self.umumi:
                self.say2=0
                for j in i: 
                    self.tableWidget.setItem(self.say1,self.say2, QTableWidgetItem(str(j)))                
                    self.tableWidget.setColumnWidth(5, 100)
                    self.say2+=1
                self.say1+=1

            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)              
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.tableWidget.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch)
            self.tableWidget.setSortingEnabled(True)
            afont = QFont()
            afont.setFamily("Times New Roman")
            afont.setPointSize(9)
            self.tableWidget.horizontalHeaderItem(0).setFont(afont)
            self.tableWidget.horizontalHeaderItem(1).setFont(afont)
            self.tableWidget.horizontalHeaderItem(2).setFont(afont)
            self.tableWidget.horizontalHeaderItem(3).setFont(afont)
            self.tableWidget.horizontalHeaderItem(4).setFont(afont)
            self.tableWidget.horizontalHeaderItem(5).setFont(afont)
            self.tableWidget.horizontalHeaderItem(6).setFont(afont)
            self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))
            self.tableWidget.horizontalHeader().sectionResized.connect(self.tableWidget.resizeRowsToContents)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableWidget.doubleClicked.connect(self.klik)
        except Exception as e:
            s=str(e)
            print("Pencere3_radioclick2"+s)


    def traa(self):

        try:
            self.umumi=[] 
            if  self.tarix1.text()<self.tarix2.text():
              
 
                self.umumi=[] 
                self.metn=''
                self.metn=self.cur.execute("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel,for from sifahi where tarix between  ? and ? """,(self.tarix1.text(),self.tarix2.text()))
                self.metn1=self.metn.fetchall()
                for i in self.metn1:
                    self.umumi.append(i)            

                self.metn2=self.cur.execute("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel ,for from yazili where tarix between  ? and ? """,(self.tarix1.text(),self.tarix2.text()))
                self.metn3=self.metn2.fetchall()
                for i in self.metn3:
                    self.umumi.append(i)

                self.metn4=self.cur.execute ("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel ,for from elektron where tarix between  ? and ? """,(self.tarix1.text(),self.tarix2.text()))
                self.metn5=self.metn4.fetchall()
                for i in self.metn5:
                    self.umumi.append(i)
                self.setir=len(self.umumi)      
                self.tableWidget.setRowCount(self.setir)

                self.say1=0        
                for i in self.umumi:
                    self.say2=0
                    for j in i: 
                        self.tableWidget.setItem(self.say1,self.say2, QTableWidgetItem(str(j)))                
                        self.tableWidget.setColumnWidth(5, 100)
                        self.say2+=1
                    self.say1+=1

                self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)              
                self.tableWidget.horizontalHeader().setStretchLastSection(True)
                self.tableWidget.horizontalHeader().setSectionResizeMode(
                    QHeaderView.Stretch)
                self.tableWidget.setSortingEnabled(True)
                afont = QFont()
                afont.setFamily("Times New Roman")
                afont.setPointSize(10)
                self.tableWidget.horizontalHeaderItem(0).setFont(afont)
                self.tableWidget.horizontalHeaderItem(1).setFont(afont)
                self.tableWidget.horizontalHeaderItem(2).setFont(afont)
                self.tableWidget.horizontalHeaderItem(3).setFont(afont)
                self.tableWidget.horizontalHeaderItem(4).setFont(afont)
                self.tableWidget.horizontalHeaderItem(5).setFont(afont)
                self.tableWidget.horizontalHeaderItem(6).setFont(afont)
                self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))
                self.tableWidget.horizontalHeader().sectionResized.connect(self.tableWidget.resizeRowsToContents)
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.tableWidget.doubleClicked.connect(self.klik)
            else:
                QMessageBox.information(self, "Xəbərdarlıq","Tarix aralığını düzgün daxil seçin !")
                

        except Exception as e:
            s=str(e)
            print("Pencere3_traa"+s)       

    def klik(self):
        

        try:
            self.row=self.tableWidget.currentRow()
            self.qeydi = (self.tableWidget.item(self.row, 1).text())
            self.formas=(self.tableWidget.item(self.row, 7).text())
            if self.formas=="Şifahi":

                self.senedi=[]
                for i in range(15):
                    metn=self.cur.execute("""select GROUP_CONCAT(sıra_no),GROUP_CONCAT(daxil_no),GROUP_CONCAT(tarix),GROUP_CONCAT(vereq),GROUP_CONCAT(ad_soyad),GROUP_CONCAT(novu),GROUP_CONCAT(fin),GROUP_CONCAT(unvan),GROUP_CONCAT(tel),GROUP_CONCAT(netice),GROUP_CONCAT(mezmun),GROUP_CONCAT(icraci),GROUP_CONCAT(for),GROUP_CONCAT(cvb_mezmun),GROUP_CONCAT(cvb_tarix) from sifahi where daxil_no=(?) """,(self.qeydi,))
                    metni=metn.fetchall()
                    columns=[x[i] for x in metni]
                    self.senedi.append(columns[0])
   
                self.xarmes=self.cur.execute("""select xarakteri from sifahi where daxil_no=(?) """,(self.qeydi,))
                self.xarme=self.xarmes.fetchall()
                self.yox=self.cur.execute("""select qeyd_eden from  sifahi where daxil_no=(?)""",(self.qeydi,))
                self.yox1=self.yox.fetchall()
                self.user1=self.yox1[0][0]

                
            elif self.formas=="Yazılı":
                self.senedi=[]                
 
                for i in range(23):
                    metn=self.cur.execute("""select GROUP_CONCAT(sira_no),GROUP_CONCAT(daxil_no),GROUP_CONCAT(tarix),GROUP_CONCAT(ad_soyad),GROUP_CONCAT(vereqsay),GROUP_CONCAT(nov),GROUP_CONCAT(forması),GROUP_CONCAT(yolu),GROUP_CONCAT(kime),GROUP_CONCAT(evvelki),GROUP_CONCAT(musaiyet),GROUP_CONCAT(mezmun),GROUP_CONCAT(derkenar),GROUP_CONCAT(icraci),GROUP_CONCAT(cvb_tarix),GROUP_CONCAT(cvb_mezmun),GROUP_CONCAT(cvb_indeksi),GROUP_CONCAT(aidiyyat),GROUP_CONCAT(nezaret),GROUP_CONCAT(fin),GROUP_CONCAT(unvan),GROUP_CONCAT(tel),GROUP_CONCAT(netice),GROUP_CONCAT(for) from yazili where daxil_no=(?) """,(self.qeydi,))
                    metni=metn.fetchall()
                    columns=[x[i] for x in metni]
                    self.senedi.append(columns[0])
               

                self.xarmey=self.cur.execute("""select xarakteri from yazili where daxil_no=(?) """,(self.qeydi,))
                self.xarme=self.xarmey.fetchall()
                self.yox=self.cur.execute("""select qeyd_eden from  yazili where daxil_no=(?)""",(self.qeydi,))
                self.yox1=self.yox.fetchall()
                self.user1=self.yox1[0][0]
                
            elif self.formas=="Elektron":
                self.senedi=[]                
 
                for i in range(23):
                    metn=self.cur.execute("""select GROUP_CONCAT(sira_no),GROUP_CONCAT(daxil_no),GROUP_CONCAT(tarix),GROUP_CONCAT(ad_soyad),GROUP_CONCAT(vereqsay),GROUP_CONCAT(nov),GROUP_CONCAT(forması),GROUP_CONCAT(yolu),GROUP_CONCAT(kime),GROUP_CONCAT(evvelki),GROUP_CONCAT(musaiyet),GROUP_CONCAT(mezmun),GROUP_CONCAT(derkenar),GROUP_CONCAT(icraci),GROUP_CONCAT(cvb_tarix),GROUP_CONCAT(cvb_mezmun),GROUP_CONCAT(cvb_indeksi),GROUP_CONCAT(aidiyyat),GROUP_CONCAT(nezaret),GROUP_CONCAT(fin),GROUP_CONCAT(unvan),GROUP_CONCAT(tel),GROUP_CONCAT(netice),GROUP_CONCAT(for) from elektron where daxil_no=(?) """,(self.qeydi,))
                    metni=metn.fetchall()
                    columns=[x[i] for x in metni]
                    self.senedi.append(columns[0])
  
                self.xarmey=self.cur.execute("""select xarakteri from elektron where daxil_no=(?) """,(self.qeydi,))
                self.xarme=self.xarmey.fetchall()
                self.yox=self.cur.execute("""select qeyd_eden from  elektron where daxil_no=(?)""",(self.qeydi,))
                self.yox1=self.yox.fetchall()
                self.user1=self.yox1[0][0]
        
            if self.senedi[-3].strip("' '")=="Şifahi":
                duzelis_ekran.radiobutton.setChecked(True)
                duzelis_ekran.sira_no.setText(self.senedi[0])
                duzelis_ekran.daxil_no.setText(self.senedi[1].strip("' '"))
                duzelis_ekran.tarix.setText(self.senedi[2].strip("' '"))
                duzelis_ekran.vereq.setText(self.senedi[3].strip("' '"))
                duzelis_ekran.ad.setText(self.senedi[4].strip("' '"))
                duzelis_ekran.fin.setText(self.senedi[6].strip("' '"))
                duzelis_ekran.tel.setText (self.senedi[8].strip("' '"))
                duzelis_ekran.unv.setText(self.senedi[7].strip("' '"))                
                duzelis_ekran.nov.setCurrentIndex(duzelis_ekran.novu.index(self.senedi[5].strip("' '")))
                duzelis_ekran.netice.setCurrentIndex(duzelis_ekran.neticesi.index(self.senedi[9].strip("' '")))
                duzelis_ekran.mezmun.setText(self.senedi[10].strip("' '"))
                duzelis_ekran.icra.setCurrentIndex(duzelis_ekran.icraci.index(self.senedi[11].strip("' '")))
                duzelis_ekran.cvb_mzm.setText(self.senedi[13].strip("' '"))
                duzelis_ekran.cvb_trx.setText(self.senedi[14].strip("' '"))
                duzelis_ekran.xar.setCurrentIndex(duzelis_ekran.xarakteri.index(self.xarme[0][0]))

                pdfac.radiobutton.setChecked(True)
                pdfac.sira_no.setText(self.senedi[0])
                pdfac.daxil_no.setText(self.senedi[1].strip("' '"))
                pdfac.tarix.setText(self.senedi[2].strip("' '"))
                pdfac.vereq.setText(self.senedi[3].strip("' '"))
                pdfac.ad.setText(self.senedi[4].strip("' '"))
                pdfac.fin.setText(self.senedi[6].strip("' '"))
                pdfac.tel.setText (self.senedi[8].strip("' '"))
                pdfac.unv.setText(self.senedi[7].strip("' '"))                
                pdfac.nov.setText(duzelis_ekran.nov.currentText())
                pdfac.netice.setText(duzelis_ekran.netice.currentText())
                pdfac.mezmun.setText(self.senedi[10].strip("' '"))
                pdfac.icra.setText(duzelis_ekran.icra.currentText())
                pdfac.cvb_mzm.setText(self.senedi[13].strip("' '"))
                pdfac.cvb_trx.setText(self.senedi[14].strip("' '"))
                pdfac.xar.setText(self.xarme[0][0])



            else:
                duzelis_ekran.sira_no.setText(self.senedi[0])
                duzelis_ekran.daxil_no.setText(self.senedi[1].strip("' '"))
                duzelis_ekran.tarix.setText(self.senedi[2].strip("' '"))
                duzelis_ekran.ad.setText(self.senedi[3].strip("' '"))
                duzelis_ekran.vereq.setText(self.senedi[4].strip("' '"))
                duzelis_ekran.nov.setCurrentIndex(duzelis_ekran.novu.index(self.senedi[5].strip("' '")))
                duzelis_ekran.formasi.setCurrentIndex(duzelis_ekran.formas.index(self.senedi[6].strip("' '")))
                duzelis_ekran.yolu.setCurrentIndex(duzelis_ekran.yollar.index(self.senedi[7].strip("' '")))
                duzelis_ekran.sexs.setText(self.senedi[8].strip("' '"))
                try:
                    duzelis_ekran.evvel.setCurrentIndex(duzelis_ekran.evvelkil.index(self.senedi[9].strip("' '")))
                except:
                    pass
                duzelis_ekran.gonderen.setText(self.senedi[10].strip("' '"))                
                duzelis_ekran.xar.setCurrentIndex(duzelis_ekran.xarakteri.index(self.xarme[0][0]))
                duzelis_ekran.mezmun.setText(self.senedi[11].strip("' '"))
                duzelis_ekran.derk.setCurrentIndex(duzelis_ekran.derkenar.index(self.senedi[12].strip("' '")))             
                duzelis_ekran.icra.setCurrentIndex(duzelis_ekran.icraci.index(self.senedi[13].strip("' '")))
                duzelis_ekran.cvb_trx.setText(self.senedi[14].strip("' '"))
                duzelis_ekran.cvb_mzm.setText(self.senedi[15].strip("' '"))
                duzelis_ekran.cvb_ind.setText(self.senedi[16].strip("' '"))
                duzelis_ekran.aid.setText(self.senedi[17].strip("' '"))
                duzelis_ekran.nez.setCurrentIndex(duzelis_ekran.nezareti.index(self.senedi[18].strip("' '")))
                duzelis_ekran.fin.setText(self.senedi[19].strip("' '"))
                duzelis_ekran.unv.setText(self.senedi[20].strip("' '"))
                duzelis_ekran.tel.setText (self.senedi[21].strip("' '"))
                duzelis_ekran.netice.setCurrentIndex(duzelis_ekran.neticesi.index(self.senedi[22].strip("' '")))
                if self.formas=="Yazılı" :
                    duzelis_ekran.radiobutton1.setChecked(True)
                elif self.formas=="Elektron":
                    duzelis_ekran.radiobutton2.setChecked(True)

                pdfac.sira_no.setText(self.senedi[0])
                pdfac.daxil_no.setText(self.senedi[1].strip("' '"))
                pdfac.tarix.setText(self.senedi[2].strip("' '"))
                pdfac.ad.setText(self.senedi[3].strip("' '"))
                pdfac.vereq.setText(self.senedi[4].strip("' '"))
                pdfac.nov.setText(duzelis_ekran.nov.currentText())
                pdfac.formasi.setText(duzelis_ekran.formasi.currentText())
                pdfac.yolu.setText(duzelis_ekran.yolu.currentText())
                pdfac.sexs.setText(self.senedi[8].strip("' '"))
                try:
                    pdfac.evvel.setText(duzelis_ekran.evvel.currentText())
                except:
                    pass
                pdfac.gonderen.setText(self.senedi[10].strip("' '"))                
                pdfac.xar.setText(self.xarme[0][0])
                pdfac.mezmun.setText(self.senedi[11].strip("' '"))
                pdfac.derk.setText(duzelis_ekran.derk.currentText())             
                pdfac.icra.setText(duzelis_ekran.icra.currentText())
                pdfac.cvb_trx.setText(self.senedi[14].strip("' '"))
                pdfac.cvb_mzm.setText(self.senedi[15].strip("' '"))
                pdfac.cvb_ind.setText(self.senedi[16].strip("' '"))
                pdfac.aid.setText(self.senedi[17].strip("' '"))
                pdfac.nez.setText(duzelis_ekran.nez.currentText())
                pdfac.fin.setText(self.senedi[19].strip("' '"))
                pdfac.unv.setText(self.senedi[20].strip("' '"))
                pdfac.tel.setText (self.senedi[21].strip("' '"))
                pdfac.netice.setText(duzelis_ekran.netice.currentText())
                if self.formas=="Yazılı" :
                    pdfac.radiobutton1.setChecked(True)
                elif self.formas=="Elektron":
                    pdfac.radiobutton2.setChecked(True)
            
            self.hide()        
            pdfac.show()
        except Exception as e:
            s=str(e)
            print("Pencere3_klik"+s)       


    def evvelki(self):
        try:
            self.hide()
            ana_ekran.show()
        except Exception as e:
            s=str(e)
            print("Pencere3_evvelki"+s)

    def axtar_duyme(self):
        try:
            self.umumi=[]
            self.setir=len(self.umumi)      
            self.tableWidget.setRowCount(self.setir)
        
            if not self.daxil_no.text()==("") and not self.daxil_no.text().isnumeric():
                QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi hərflərdən ibarət ola bilməz !")
            elif not self.ad.toPlainText()==("") and self.ad.toPlainText().isnumeric():
                QMessageBox.information(self, "Məlumat","Ad , soyad rəqəmlərdən ibarət ola bilməz !")
            elif  not self.fin.text()==("") and not len(self.fin.text())==7 :
                QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
            else:
                fin=self.fin.text()
                xar=self.xar.currentText()
                qeyd=self.daxil_no.text()
                ad=self.ad.toPlainText()

                if not qeyd=="":
                    self.umumi=[] 
                    self.metn=''
                    self.metn=self.cur.execute("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel,for from sifahi where daxil_no =? """,(qeyd,))
                    self.metn1=self.metn.fetchall()
                    for i in self.metn1:
                        self.umumi.append(i)            

                    self.metn2=self.cur.execute("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel ,for from yazili where daxil_no =? """,(qeyd,))
                    self.metn3=self.metn2.fetchall()
                    for i in self.metn3:
                        self.umumi.append(i)

                    self.metn4=self.cur.execute ("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel ,for from elektron where daxil_no =? """,(qeyd,))
                    self.metn5=self.metn4.fetchall()
                    for i in self.metn5:
                        self.umumi.append(i)
                    self.setir=len(self.umumi)      
                    self.tableWidget.setRowCount(self.setir)

                    self.say1=0        
                    for i in self.umumi:
                        self.say2=0
                        for j in i:
                            
                            self.tableWidget.setItem(self.say1,self.say2, QTableWidgetItem(str(j)))                
                            self.tableWidget.setColumnWidth(5, 100)
                            self.say2+=1
                        self.say1+=1

                    self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)              
                    self.tableWidget.horizontalHeader().setStretchLastSection(True)
                    self.tableWidget.horizontalHeader().setSectionResizeMode(
                        QHeaderView.Stretch)
                    self.tableWidget.setSortingEnabled(True)
                    afont = QFont()
                    afont.setFamily("Times New Roman")
                    afont.setPointSize(9)
                    self.tableWidget.horizontalHeaderItem(0).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(1).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(2).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(3).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(4).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(5).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(6).setFont(afont)
                    self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))
                    self.tableWidget.horizontalHeader().sectionResized.connect(self.tableWidget.resizeRowsToContents)
                    self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                    self.tableWidget.doubleClicked.connect(self.klik)
                    
                    self.cercive2=QFrame(self)
                    self.cercive2.move(0,60)
                    self.cercive2.resize(710,1)
                    self.cercive2.setStyleSheet("background-color : black")
                    
                    self.cercive3=QFrame(self)
                    self.cercive3.move(0,30)
                    self.cercive3.resize(710,1)
                    self.cercive3.setStyleSheet("background-color : black")

                elif  qeyd=="" and not fin=='':
                
                    self.umumi=[] 
                    self.metn=''
                    self.metn=self.cur.execute("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel,for from sifahi where fin =? """,(fin,))
                    self.metn1=self.metn.fetchall()
                    for i in self.metn1:
                        self.umumi.append(i)            

                    self.metn2=self.cur.execute("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel ,for from yazili where fin =? """,(fin,))
                    self.metn3=self.metn2.fetchall()
                    for i in self.metn3:
                        self.umumi.append(i)

                    self.metn4=self.cur.execute ("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel ,for from elektron where fin =? """,(fin,))
                    self.metn5=self.metn4.fetchall()
                    for i in self.metn5:
                        self.umumi.append(i)
                    self.setir=len(self.umumi)      
                    self.tableWidget.setRowCount(self.setir)

                    self.say1=0        
                    for i in self.umumi:
                        self.say2=0
                        for j in i: 
                            self.tableWidget.setItem(self.say1,self.say2, QTableWidgetItem(str(j)))                
                            self.tableWidget.setColumnWidth(5, 100)
                            self.say2+=1
                        self.say1+=1

                    self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)              
                    self.tableWidget.horizontalHeader().setStretchLastSection(True)
                    self.tableWidget.horizontalHeader().setSectionResizeMode(
                        QHeaderView.Stretch)
                    self.tableWidget.setSortingEnabled(True)
                    afont = QFont()
                    afont.setFamily("Times New Roman")
                    afont.setPointSize(9)
                    self.tableWidget.horizontalHeaderItem(0).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(1).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(2).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(3).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(4).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(5).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(6).setFont(afont)
                    self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))
                    self.tableWidget.horizontalHeader().sectionResized.connect(self.tableWidget.resizeRowsToContents)
                    self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                    self.tableWidget.doubleClicked.connect(self.klik)


                    self.cercive2=QFrame(self)
                    self.cercive2.move(0,60)
                    self.cercive2.resize(710,1)
                    self.cercive2.setStyleSheet("background-color : black")
                    
                    self.cercive3=QFrame(self)
                    self.cercive3.move(0,30)
                    self.cercive3.resize(710,1)
                    self.cercive3.setStyleSheet("background-color : black")


                elif  qeyd=="" and not ad=='':
                
                    self.umumi=[] 
                    self.metn=''
                    self.metn=self.cur.execute("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel,for from sifahi where ad_soyad =? """,(ad,))
                    self.metn1=self.metn.fetchall()
                    for i in self.metn1:
                        self.umumi.append(i)            

                    self.metn2=self.cur.execute("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel ,for from yazili where ad_soyad =? """,(ad,))
                    self.metn3=self.metn2.fetchall()
                    for i in self.metn3:
                        self.umumi.append(i)

                    self.metn4=self.cur.execute ("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel ,for from elektron where ad_soyad =? """,(ad,))
                    self.metn5=self.metn4.fetchall()
                    for i in self.metn5:
                        self.umumi.append(i)
                    self.setir=len(self.umumi)      
                    self.tableWidget.setRowCount(self.setir)

                    self.say1=0        
                    for i in self.umumi:
                        self.say2=0
                        for j in i: 
                            self.tableWidget.setItem(self.say1,self.say2, QTableWidgetItem(str(j)))                
                            self.tableWidget.setColumnWidth(5, 100)
                            self.say2+=1
                        self.say1+=1

                    self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)              
                    self.tableWidget.horizontalHeader().setStretchLastSection(True)
                    self.tableWidget.horizontalHeader().setSectionResizeMode(
                        QHeaderView.Stretch)
                    self.tableWidget.setSortingEnabled(True)
                    afont = QFont()
                    afont.setFamily("Times New Roman")
                    afont.setPointSize(9)
                    self.tableWidget.horizontalHeaderItem(0).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(1).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(2).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(3).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(4).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(5).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(6).setFont(afont)
                    self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))
                    self.tableWidget.horizontalHeader().sectionResized.connect(self.tableWidget.resizeRowsToContents)
                    self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                    self.tableWidget.doubleClicked.connect(self.klik)


                    self.cercive2=QFrame(self)
                    self.cercive2.move(0,60)
                    self.cercive2.resize(850,1)
                    self.cercive2.setStyleSheet("background-color : black")
                    
                    self.cercive3=QFrame(self)
                    self.cercive3.move(0,30)
                    self.cercive3.resize(850,1)
                    self.cercive3.setStyleSheet("background-color : black")

                elif  qeyd=="" and not xar=='':
                
                    self.umumi=[] 
                    self.metn=''
                    self.metn=self.cur.execute("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel,for from sifahi where xarakteri =? """,(xar,))
                    self.metn1=self.metn.fetchall()
                    for i in self.metn1:
                        self.umumi.append(i)            

                    self.metn2=self.cur.execute("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel ,for from yazili where xarakteri =? """,(xar,))
                    self.metn3=self.metn2.fetchall()
                    for i in self.metn3:
                        self.umumi.append(i)

                    self.metn4=self.cur.execute ("""SELECT daxil_no,tarix,ad_soyad,fin,icraci,tel ,for from elektron where xarakteri  =? """,(xar,))
                    self.metn5=self.metn4.fetchall()
                    for i in self.metn5:
                        self.umumi.append(i)
                    self.setir=len(self.umumi)      
                    self.tableWidget.setRowCount(self.setir)

                    self.say1=0        
                    for i in self.umumi:
                        self.say2=0
                        for j in i: 
                            self.tableWidget.setItem(self.say1,self.say2, QTableWidgetItem(str(j)))                
                            self.tableWidget.setColumnWidth(5, 100)
                            self.say2+=1
                        self.say1+=1

                    self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)              
                    self.tableWidget.horizontalHeader().setStretchLastSection(True)
                    self.tableWidget.horizontalHeader().setSectionResizeMode(
                        QHeaderView.Stretch)
                    self.tableWidget.setSortingEnabled(True)
                    afont = QFont()
                    afont.setFamily("Times New Roman")
                    afont.setPointSize(9)
                    self.tableWidget.horizontalHeaderItem(0).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(1).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(2).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(3).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(4).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(5).setFont(afont)
                    self.tableWidget.horizontalHeaderItem(6).setFont(afont)
                    self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter | Qt.Alignment(Qt.TextWordWrap))
                    self.tableWidget.horizontalHeader().sectionResized.connect(self.tableWidget.resizeRowsToContents)
                    self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                    self.tableWidget.doubleClicked.connect(self.klik)


                    self.cercive2=QFrame(self)
                    self.cercive2.move(0,60)
                    self.cercive2.resize(850,1)
                    self.cercive2.setStyleSheet("background-color : black")
                    
                    self.cercive3=QFrame(self)
                    self.cercive3.move(0,30)
                    self.cercive3.resize(850,1)
                    self.cercive3.setStyleSheet("background-color : black")



                    
        except Exception as e:
            s=str(e)
            print("Pencere3_axtar_duyme"+s)
##################################################################################################################################################################

class Pencere4(QWidget):
    def __init__(self):
        try:
            super().__init__()
            self.setFixedSize(850, 750)
            qtRectangle = self.frameGeometry()
            centerPoint = QDesktopWidget().availableGeometry().center()
            qtRectangle.moveCenter(centerPoint)
            self.move(qtRectangle.topLeft())
            self.setStyleSheet("background-color: #dcdcdc;")
            self.setWindowTitle("Müraciətə Düzəliş")
            self.yol=os.getcwd()
            self.bazayol=esas_baza
            self.yoxlama=''


            try:
                os.chdir(self.bazayol)
                self.dir=os.listdir()
                if "baza.db" not in self.dir:
                    QMessageBox.information(self, "Məlumat","Verilənlər bazası mövcud deyil !")
                    sys.exit()
                else:             
                    self.con = sqlite3.connect(self.bazayol+"\\baza.db")
                    self.cur = self.con.cursor()
                    os.chdir(self.yol)
            except:
                sys.exit()

            self.yoxla()
            self.metn=self.cur.execute("SELECT sıra_no FROM sifahi")
            self.metn1=self.metn.fetchall()
            self.sirasi=[]
            for i in self.metn1:
                self.sirasi.append(* i)
            try:
                self.sifahi_sira_nomre=int(self.sirasi[-1])+1
            except:
                self.sifahi_sira_nomre=1
                
            
            self.metn2=self.cur.execute("SELECT sira_no FROM yazili")
            self.metn3=self.metn2.fetchall()
            self.yazili_sirasi=[]
            for i in self.metn3:
                self.yazili_sirasi.append(* i)
            try:
                self.yazili_sira_nomre=int(self.yazili_sirasi[-1])+1
            except:
                self.yazili_sira_nomre=1

            self.metn4=self.cur.execute("SELECT sira_no FROM elektron")
            self.metn5=self.metn4.fetchall()
            self.elektron_sirasi=[]
            for i in self.metn5:
                self.elektron_sirasi.append(* i)
            try:
                self.elektron_sira_nomre=int(self.elektron_sirasi[-1])+1
            except:
                self.elektron_sira_nomre=1

            self.novu=['Ərizə','Təklif','Şikayət']
            self.xarakte="Ailə münasibətləri üzrə mübahisələr.Əmək mübahisələri.Mənzil mübahisələri.Mülkiyyət hüququ ilə əlaqədar mübahisələr.Əqli mülkiyyət hüququ ilə əlaqədar mübahisələr.Torpaq mübahisələri.Müqavilələrin bağlanması.Müqavilələrin ləğv edilməsi.Müqavilələrin məcburi bağlanması,müqavilənin etibarsız hesab edilməsi tələbi üzrə.Müqavilələrdən əmələ gələn öhdəliklər üzrə mübahisələr.Mülki hüquq pozuntularından (deliktlərdən) əmələ gələn öhdəliklər üzrə mübahisələr.Vərəsəlik hüququ üzrə mübahisələr.Hüquqi əhəmiyyəti olan faktların müəyyən edilməsi haqqında.Şəxsin xəbərsiz itkin düşmüş hesab edilməsi haqqında.Şəxsin ölmüş elan edilməsi haqqında.Şəxsin məhdud fəaliyyət qabiliyyətli və ya fəaliyyət qabiliyyəti olmayan hesab edilməsi haqqında.Şəxsin xəbərsiz itkin düşmüş hesab edilməsi və ya şəxsin ölmüş elan edilməsi haqqında.Daşınar əşyanın sahibsiz hesab edilməsi və daşınmaz əşya üzərində dövlət mülkyyəti hüququnun tanınması haqqında.Notariat hərəkətlərindən və ya həmin hərəkətlərin aparılmasından imtinaya dair şikayətlər üzrə icraat.Vətəndaşlıq vəziyyəti aktlarının qeydiyyatının düzgün olmamasının müəyyən edilməsi haqqında.Məişət zorakılığı ilə bağlı müraciətlər.Şərəf və ləyaqətin müdafiəsi üzrə.Müvafiq icra hakimiyyəti orqanlarının və onların vəzifəli şəxslərinin inzibati hüquq pozuntuları ilə bağlı müraciətlər.Müvafiq icra hakimiyyəti və yerli özünüidarə orqanlarının, sair orqan və təşkilatların, onların vəzifəli şəxslərinin qərarlarından və hərəkətlərindən (hərəkətsizliklərindən) olan müraciətlər üzrə.Övladlığa götürmə.Mülki və cinayət işlərinə məhkəmələr tərəfindən vaxtında baxılmaması ilə bağlı müraciətlər.Birinci instansiya məhkəmələri tərəfindən baxılmış işlər üzrə apеllyasiya şikayəti (protеsti).Apеllyasiya qaydasında baxılmış işlər  üzrə kassasiya şikayəti (protеsti).Mülki və cinayət işlərinə, inzibati xətalara dair matеriallara məhkəmələr tərəfindən obyеktiv baxılmaması ilə bağlı müraciətlər.Naxçıvan MR Ali Məhkəməsinin icraatında olan işlərlə bağlı müxtəlif məzmunlu ərizələr.Qətnamələrin və məhkəmə əmrlərinin vaxtında icra olunmaması ilə bağlı ərizələr.Sair məzmunlu ərizələr.Təkrar ərizə və şikayətlər.Etiraz ərizələri"
            self.xarakter=self.xarakte.split(".")
            self.xarakteri=[]
            for i in self.xarakter:
                self.xarakteri.append(i)
            self.icraci=["Əsgər Novruzov","İlqar Mirzayev","Əli Allahverdiyev","Yusifəli Qurbanov","Səxavət Novruzov","Səxavət Bəylərli","Sənan Qarayev","Mehman Allahverdiyev","Fərman Abbasov","Vüqar Quliyev","Vera Kuimova","Gülay Qurbanova","Oruc Əliyev","Sahilə Bağırova","Aqil Atakişiyev"]
            self.neticesi=["Baxıldı","Baxılmadı"]
            self.nezareti=["Nəzarətdədir","Nəzarətdən çıxarılmışdır"]
            self.derkenar=["Sədr","Sədr müavini"]
            self.formas=["Məktub","Elektron məktub","Teleqram","Faks"]
            self.yollar=["Poçt","Elektron poçt","Teleqram","Faks","Qəbul zamanı"]
            self.evvelkil=[]
           
            basliq = QLabel(self)
            basliq.move(0, 0)
            basliq.resize(850,79)
            basliq.setStyleSheet("font-family: Arial;font-style:normal ;background-image : url(resurslar/duzelis.jpg) ;font-size: 16pt;color : black; border: 1px solid black")
            
            self.radiobutton = QRadioButton(self)
            self.radiobutton.setText("Şifahi müraciət")
            self.radiobutton.setChecked(False)
            self.radiobutton.toggled.connect(self.sifahi)
            self.radiobutton.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")
            self.radiobutton.move(130, 90)
            #self.radiobutton.toggled.connect(self.yenile)

            self.radiobutton1 = QRadioButton(self)
            self.radiobutton1.setText("Yazılı müraciət")
            self.radiobutton1.setChecked(True)
            self.radiobutton1.toggled.connect(self.yazili)
            self.radiobutton1.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")
            self.radiobutton1.move(350, 90)
            #self.radiobutton1.toggled.connect(self.yenile)

            self.radiobutton2 = QRadioButton(self)
            self.radiobutton2.setText("Elektron müraciət")
            self.radiobutton2.setChecked(False)
            self.radiobutton2.toggled.connect(self.elektron)
            self.radiobutton2.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")
            self.radiobutton2.move(570, 90)
            #self.radiobutton2.toggled.connect(self.yenile)

            self.sira_no = QLineEdit(self)
            self.sira_no.move(200, 130)
            self.sira_no.resize(100,22)
            self.sira_no.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.sira_no_lab = QLabel(self)
            self.sira_no_lab.move(20, 130)
            self.sira_no_lab.resize(180,25)
            self.sira_no_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.sira_no_lab.setText("Sıra nömrəsi")
            self.sira_no.setEnabled=(True)

            self.derk = QComboBox(self)
            self.derk.move(660, 130)
            self.derk.resize(150,22)
            self.derk.addItems(self.derkenar)
            self.derk.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.derk_lab = QLabel(self)
            #self.derk.setWordWrap(True)
            self.derk_lab.move(430, 130)
            self.derk_lab.resize(170,25)
            self.derk_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.derk_lab.setText("Dərkənar")


            if self.radiobutton.isChecked():
                self.sira_no.setText(str(self.sifahi_sira_nomre))
            elif self.radiobutton1.isChecked():
                self.sira_no.setText(str(self.yazili_sira_nomre))
            elif self.radiobutton2.isChecked():
                self.sira_no.setText(str(self.elektron_sira_nomre))
     
            self.daxil_no = QLineEdit(self)
            self.daxil_no.move(200, 165)
            self.daxil_no.resize(200,22)
            self.daxil_no.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.daxil_no_lab = QLabel(self)
            self.daxil_no_lab.move(20, 165)
            self.daxil_no_lab.resize(180,25)
            self.daxil_no_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.daxil_no_lab.setText("Qeydiyyat nömrəsi")

            self.tarix = QLineEdit(self)
            self.tarix.move(200, 200)
            self.tarix.resize(100,22)
            self.tarix.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.tarix_lab = QLabel(self)
            self.tarix_lab.move(20, 200)
            self.tarix_lab.resize(180,25)
            self.tarix_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.tarix_lab.setText("Qeydiyyat tarixi")
            #self.tarix.setDate(QDate.currentDate())
            
            self.vereq= QLineEdit(self)
            self.vereq.move(200, 235)
            self.vereq.resize(100,22)
            self.vereq.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.vereq_lab = QLabel(self)
            self.vereq_lab.move(20, 235)
            self.vereq_lab.resize(180,25)
            self.vereq_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.vereq_lab.setText("Vərəq sayı ")

            self.ad = QTextEdit(self)
            self.ad.move(200, 261)
            self.ad.resize(200,40)
            self.ad.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.ad_lab = QLabel(self)
            self.ad_lab.move(20, 270)
            self.ad_lab.resize(180,25)
            self.ad_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.ad_lab.setText("Ad,soyad,ata adı")

            self.fin = QLineEdit(self)
            self.fin.move(200, 305)
            self.fin.resize(100,22)
            self.fin.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.fin_lab = QLabel(self)
            self.fin_lab.move(20, 305)
            self.fin_lab.resize(180,25)
            self.fin_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.fin_lab.setText("FİN nömrəsi")
            self.fin.returnPressed.connect(self.evvelde)
            
            self.unv = QLineEdit(self)
            self.unv.move(200, 340)
            self.unv.resize(610,22)
            self.unv.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.unv_lab = QLabel(self)
            self.unv_lab.move(20, 340)
            self.unv_lab.resize(180,25)
            self.unv_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.unv_lab.setText("Ünvanı")

            self.tel = QLineEdit(self)
            self.tel.move(200, 375)
            self.tel.resize(100,22)
            self.tel.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.tel_lab = QLabel(self)
            self.tel_lab.move(20, 375)
            self.tel_lab.resize(180,25)
            self.tel_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.tel_lab.setText("Telefon nömrəsi")

            self.nov = QComboBox(self)
            self.nov.move(660, 375)
            self.nov.resize(150,22)
            self.nov.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.nov.addItems(self.novu)
            self.nov_lab = QLabel(self)
            self.nov_lab.move(430, 375)
            self.nov_lab.resize(130,25)
            self.nov_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.nov_lab.setText("Müraciətin növü")

            self.xar = QComboBox(self)
            self.xar.move(200, 410)
            self.xar.resize(610,44)
            self.xar.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.xar.addItems(self.xarakteri)
            self.xar_lab = QLabel(self)
            self.xar_lab.move(20, 410)
            self.xar_lab.resize(180,25)
            self.xar_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.xar_lab.setText("Müraciətin xarakteri")
            self.xarakterler=QCompleter(self.xarakteri)
            self.xar.setCompleter(self.xarakterler)


            self.mezmun = QTextEdit(self)
            self.mezmun.move(200, 465)
            self.mezmun.resize(610,44)
            self.mezmun.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.mezmun_lab = QLabel(self)
            self.mezmun_lab.move(20, 465)
            self.mezmun_lab.resize(180,25)
            self.mezmun_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.mezmun_lab.setText("Müraciətin qısa məzmnu")


            self.icra = QComboBox(self)
            self.icra.move(200, 575)
            self.icra.resize(190,22)
            self.icra.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.icra.addItems(self.icraci)
            self.icra_lab = QLabel(self)
            self.icra_lab.move(20, 575)
            self.icra_lab.resize(180,25)
            self.icra_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.icra_lab.setText("İcraçı")

            self.netice = QComboBox(self)
            self.netice.move(200, 610)
            self.netice.resize(190,22)
            self.netice.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.netice.addItems(self.neticesi)
            self.netice_lab = QLabel(self)
            self.netice_lab.move(20, 610)
            self.netice_lab.resize(150,25)
            self.netice_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.netice_lab.setText("Nəticəsi")

            self.aid = QTextEdit(self)
            self.aid.move(510,645)
            self.aid.resize(300,44)
            self.aid.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.aid_lab = QLabel(self)
            self.aid_lab.move(430, 665)
            self.aid_lab.resize(75,25)
            self.aid_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.aid_lab.setText("Aidiyyət")

            self.nez = QComboBox(self)
            self.nez.move(610, 610)
            self.nez.resize(200,22)
            self.nez.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.nez.addItems(self.nezareti)
            self.nez_lab = QLabel(self)
            self.nez_lab.move(430, 610)
            self.nez_lab.resize(75,25)
            self.nez_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.nez_lab.setText("Nəzarət")

            self.cvb_mzm = QTextEdit(self)
            self.cvb_mzm.move(200, 520)
            self.cvb_mzm.resize(610,44)
            self.cvb_mzm.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.cvb_mzm_lab = QLabel(self)
            self.cvb_mzm_lab.move(20, 520)
            self.cvb_mzm_lab.resize(150,25)
            self.cvb_mzm_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.cvb_mzm_lab.setText("Cavabın məzmunu")
            
            self.cvb_trx = QLineEdit(self)
            self.cvb_trx.move(200, 665)
            self.cvb_trx.resize(190,22)
            self.cvb_trx.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.cvb_trx_lab = QLabel(self)
            self.cvb_trx_lab.move(20, 665)
            self.cvb_trx_lab.resize(150,25)
            self.cvb_trx_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.cvb_trx_lab.setText("Cavabın tarixi")


            self.cvb_ind = QLineEdit(self)
            self.cvb_ind.move(610, 575)
            self.cvb_ind.resize(200,22)
            self.cvb_ind.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.cvb_ind_lab = QLabel(self)
            self.cvb_ind_lab.move(430, 575)
            self.cvb_ind_lab.resize(120,25)
            self.cvb_ind_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.cvb_ind_lab.setText("Cavabın indeksi")

            self.formasi = QComboBox(self)
            self.formasi.move(660, 165)
            self.formasi.resize(150,22)
            self.formasi.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.formasi.addItems(self.formas)
            self.formasi_lab = QLabel(self)
            #self.formasi.setWordWrap(True)
            self.formasi_lab.move(430, 165)
            self.formasi_lab.resize(170,25)
            self.formasi_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.formasi_lab.setText("Müraciətin forması")


            self.yolu = QComboBox(self)
            self.yolu.move(660, 200)
            self.yolu.resize(150,22)
            self.yolu.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.yolu.addItems(self.yollar)
            self.yolu_lab = QLabel(self)
            #self.yolu.setWordWrap(True)
            self.yolu_lab.move(430, 200)
            self.yolu_lab.resize(170,25)
            self.yolu_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.yolu_lab.setText("Müraciətin Qeydiyyat yolu")


            self.sexs = QLineEdit(self)
            self.sexs.move(660, 235)
            self.sexs.resize(150,22)
            self.sexs.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.sexs_lab = QLabel(self)
            self.sexs_lab.move(430, 235)
            self.sexs_lab.resize(170,25)
            self.sexs_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.sexs_lab.setText("Ünvanlandığı şəxs")

            self.evvel = QComboBox(self)
            self.evvel.move(660, 270)
            self.evvel.resize(150,22)
            self.evvel.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.evvel_lab = QLabel(self)
            self.evvel.addItems(self.evvelkil)
            self.evvel_lab.move(430, 270)
            self.evvel_lab.resize(170,25)
            self.evvel_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.evvel_lab.setText("Əvvəlki müraciətlər")

            self.gonderen = QTextEdit(self)
            self.gonderen.move(580, 296)
            self.gonderen.resize(230,40)
            self.gonderen.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 9pt;font-weight: bold;color : black;")
            self.gonderen_lab = QLabel(self)
            self.gonderen_lab.move(430, 300)
            self.gonderen_lab.resize(150,35)
            self.gonderen_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.gonderen_lab.setText("Müşaiyət məktubunu göndərən")
            self.gonderen_lab.setWordWrap(True)

            self.cerci=QFrame(self)
            self.cerci.resize(850,55)
            self.cerci.move(0,695)
            self.cerci.setStyleSheet("background-image : url(resurslar/alt.jpg);")
                
 
            self.printe=QPushButton(self)
            self.printe.resize(47,47)
            self.printe.move(5,700)
            self.printe.setStyleSheet("background-image : url(resurslar/pr.jpg);")
            self.printe.clicked.connect(self.printet)

            self.pdf=QPushButton(self)
            self.pdf.resize(47,47)
            self.pdf.move(55,700)
            self.pdf.setStyleSheet("background-image : url(resurslar/pd.jpg);")
            self.pdf.clicked.connect(self.sened)

            self.erize_yukle=QPushButton(self)
            self.erize_yukle.resize(47,47)
            self.erize_yukle.move(105,700)
            self.erize_yukle.setStyleSheet("background-image : url(resurslar/yuk.jpg);")
            self.erize_yukle.clicked.connect(self.er_yukle)

            self.cavab_yukle=QPushButton(self)
            self.cavab_yukle.resize(47,47)
            self.cavab_yukle.move(155,700)
            self.cavab_yukle.setStyleSheet("background-image : url(resurslar/me.jpg);")
            self.cavab_yukle.clicked.connect(self.cvb_yukle)

            self.qayittt=QPushButton(self)
            self.qayittt.resize(160,30)
            self.qayittt.move(680,710)
            self.qayittt.setText("Əsas menyuya qayıt")
            self.qayittt.clicked.connect(self.esas)
            self.qayittt.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 11pt;font-weight: bold;color : black;")

            self.qeydet=QPushButton(self)
            self.qeydet.resize(160,30)
            self.qeydet.move(515,710)
            self.qeydet.setText("Yadda saxla")
            self.qeydet.clicked.connect(self.qeydd)
            self.qeydet.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 11pt;font-weight: bold;color : black;")

            self.legvet=QPushButton(self)
            self.legvet.resize(160,30)
            self.legvet.move(350,710)
            self.legvet.clicked.connect(self.sil)
            self.legvet.setText("Müraciəti sil")
            self.legvet.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 11pt;font-weight: bold;color : black;")

            self.endirilen=QPushButton(self)
            self.endirilen.resize(140,30)
            self.endirilen.move(205,710)
            self.endirilen.clicked.connect(self.endiri)
            self.endirilen.setText("Endirilənlər")
            self.endirilen.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 11pt;font-weight: bold;color : black;")

            self.evveli=self.daxil_no.text()
            
            self.sira_no.setText('')
            self.daxil_no.setText('')
            self.ad.setText('')
            self.fin.setText('')
            self.unv.setText('')
            self.tel.setText ('')
            self.vereq.setText('')
            self.nov.text=('')
            self.formasi.text=('')
            self.yolu.text=('')
            self.sexs.setText('')
            self.evvel.text=('')
            self.gonderen.setText('')
            self.xar.text=('')
            self.mezmun.setText('')
            self.derk.text=('')
            self.icra.text=('')
            self.cvb_trx.setText('')
            self.cvb_mzm.setText('')
            self.cvb_ind.setText('')
            self.aid.setText('')
            self.nez.text=('')
            self.netice.text=('')
        except Exception as e:
            s=str(e)
            print("Pencere4_init"+s)




    def endiri(self):
        try:
            os.chdir(self.yol+'\\Endirilənlər')
            self.dizin=QFileDialog.getOpenFileName(self, 'Endirilənlər',os.getcwd())
            os.popen(self.dizin[0])
        except Exception as e:
            os.chdir(self.yol)           
            QMessageBox.critical(self, "Səhv","Endirilənlər qovluğu mövcud deyil !")
            s=str(e)
            print("Pencere2_endiri"+s)


    def direktori(self):
        try:
            os.chdir(sened_yolu+'\\Sənədlər')
            dire=os.listdir()
            if not self.daxil_no.text() in dire:
                QMessageBox.information(self, "Məlumat","Bu müraciətə aid sənəd tapılmadı")
            else:
                os.chdir(self.daxil_no.text())
                self.dizin=QFileDialog.getOpenFileName(self, 'sənədlər dizinində olan qovluqlar',os.getcwd())
                os.popen(self.dizin[0])
        except Exception as e:
            s=str(e)
            print(s)
            QMessageBox.critical(self, "Xəta","Xəta baş verdi ")        

    def sifahi(self):
        try:
            self.nez.hide()
            self.nez_lab.hide()
            self.aid.hide()
            self.aid_lab.hide()
            self.cvb_ind.hide()
            self.cvb_ind_lab.hide()
            self.derk.hide()
            self.derk_lab.hide()
            self.formasi.hide()
            self.formasi_lab.hide()
            self.yolu.hide()
            self.yolu_lab.hide()
            self.sexs.hide()
            self.sexs_lab.hide()
            self.evvel.hide()
            self.evvel_lab.hide()
            self.gonderen.hide()
            self.gonderen_lab.hide()
            self.vereq.hide()
            self.vereq_lab.hide()
            self.erize_yukle.hide()
            self.cavab_yukle.hide()
        except Exception as e:
            s=str(e)
            print("Pencere4_sifahi"+s)

            
    def yazili(self):
        try:
            self.nez.show()
            self.nez_lab.show()
            self.aid.show()
            self.aid_lab.show()
            self.cvb_ind.show()
            self.cvb_ind_lab.show()
            self.derk.show()
            self.derk_lab.show()
            self.formasi.show()
            self.formasi_lab.show()
            self.yolu.show()
            self.yolu_lab.show()
            self.sexs.show()
            self.sexs_lab.show()
            self.evvel.show()
            self.evvel_lab.show()
            self.gonderen.show()
            self.gonderen_lab.show()
            self.vereq.show()
            self.vereq_lab.show()
            self.erize_yukle.show()
            self.cavab_yukle.show()
        except Exception as e:
            s=str(e)
            print("Pencere4_yazili"+s)

            
    def elektron(self):
        try:
            self.nez.show()
            self.nez_lab.show()
            self.aid.show()
            self.aid_lab.show()
            self.cvb_ind.show()
            self.cvb_ind_lab.show()
            self.derk.show()
            self.derk_lab.show()
            self.formasi.show()
            self.formasi_lab.show()
            self.yolu.show()
            self.yolu_lab.show()
            self.sexs.show()
            self.sexs_lab.show()
            self.evvel.show()
            self.evvel_lab.show()
            self.gonderen.show()
            self.gonderen_lab.show()
            self.vereq.show()
            self.vereq_lab.show()
            self.erize_yukle.show()
            self.cavab_yukle.show()
        except Exception as e:
            s=str(e)
            print("Pencere4_elektron"+s)
    def evvelde(self):
        self.evv=[]
        self.evvel.clear()
        try:
            self.metn=''
            
            if not self.fin.text()=='':


                self.metni=self.cur.execute("""select daxil_no from sifahi where fin=(?) """,(self.fin.text(),))        
                self.metni1=self.metni.fetchall()
                for i in self.metni1:
                    self.evv.append(str(i[0]).strip()+"-Şifahi")


                self.metnr=self.cur.execute("""select daxil_no from yazili where fin=(?) """,(self.fin.text(),))
                self.metnr1=self.metnr.fetchall()
                for i in self.metnr1:
                    self.evv.append(str(i[0]).strip()+"-Yazılı")


                self.metno=self.cur.execute("""select daxil_no from elektron where fin=(?) """,(self.fin.text(),))
                self.metno1=self.metno.fetchall()
                for i in self.metno1:
                    self.evv.append(str(i[0]).strip()+"-Elektron")



                self.evvel.addItems(self.evv)
            

        except Exception as e:
            s=str(e)
            print("Pencere4_evvelde"+s)

    def esas(self):
        try:
            duzelis_ekran.hide()
            axtaris_ekran.radioclick1()
            axtaris_ekran.show()
        except Exception as e:
            s=str(e)
            print("Pencere4_esas"+s)
    def sil(self):
        try:
            self.sira_no.setText("")
            self.ad.setText("")
            self.fin.setText("")
            self.mezmun.setText("")
            self.aid.setText("")
            self.cvb_mzm.setText("")
            self.cvb_trx.setText("")
            self.cvb_ind.setText("")
            self.sexs.setText("")
            self.gonderen.setText("")
            self.unv.setText("")
            self.tel.setText("")
            self.vereq.setText("")
            
            if self.radiobutton.isChecked():
                qm =QMessageBox
                ret=qm.question(self,'Mesaj', "Seçilmiş müraciəti silmək istəyirsiniz ?", qm.Yes | qm.No)
                if ret==qm.Yes:

                    self.cur.execute("""delete from sifahi where daxil_no=(?) """,(self.daxil_no.text(),)).fetchall()
                    self.con.commit()
                    QMessageBox.information(self, "Məlumat","Seçilmiş müraciət verilənlər bazasından silindi ")
                else:
                    pass
                    
            elif self.radiobutton1.isChecked():
                qm =QMessageBox
                ret=qm.question(self,'Mesaj', "Seçilmiş müraciəti silmək istəyirsiniz ?", qm.Yes | qm.No)
                if ret==qm.Yes:
                    self.cur.execute("""delete from yazili where daxil_no= (?) """,(self.daxil_no.text(),)).fetchall()
                    self.con.commit()
                    QMessageBox.information(self, "Məlumat","Seçilmiş müraciət verilənlər bazasından silindi ")
                else:
                    pass

            elif self.radiobutton2.isChecked():
                qm =QMessageBox
                ret=qm.question(self,'Mesaj', "Seçilmiş müraciəti silmək istəyirsiniz ?", qm.Yes | qm.No)
                if ret==qm.Yes:
                    self.cur.execute("""delete from elektron where daxil_no= (?) """,(self.daxil_no.text(),)).fetchall()
                    self.con.commit()
                    QMessageBox.information(self, "Məlumat","Seçilmiş müraciət verilənlər bazasından silindi ")
                else:
                    pass               
        except Exception as e:
            s=str(e)
            print("Pencere4_sil"+s)
        self.hide()
        axtaris_ekran.radioclick2()   
        axtaris_ekran.show()

    def qeydd(self):
        self.evveli=pdfac.daxil_no.text()


        
        try:
        
            self.tr=0
            try:

                self.tr=1
            except ValueError:
                self.tr=0

            self.evvelde()
            if self.radiobutton.isChecked():               

                if self.daxil_no.text()=="" :
                    QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş və ya hərflərdən ibarət ola bilməz !")

                    
                elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                    QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")

                elif  not self.fin.text()=="" and not len(self.fin.text())==7 :
                    QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
                elif  len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                    QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")

                elif self.unv.text()=="" :
                    QMessageBox.information(self, "Məlumat","Ünvan bölməsinə yaşayış yerini daxil edin")
                else:
                    try:
                        if axtaris_ekran.formas=="Şifahi":
                            self.query="""UPDATE sifahi set sıra_no=?,daxil_no=?,tarix=?,ad_soyad=?,fin=?,tel=?,unvan=?,novu=?,xarakteri=?,netice=?,mezmun=?,icraci=?,cvb_mezmun=?,cvb_tarix=? ,for=?,son_deyisdiren=? ,sonduztar=? where daxil_no=?"""
                            self.values=(self.sira_no.text(),self.daxil_no.text(),self.tarix.text(),self.ad.toPlainText(),self.fin.text(),self.tel.text(),self.unv.text(),self.nov.currentText(),self.xar.currentText(),self.netice.currentText(),self.mezmun.toPlainText(),self.icra.currentText(),self.cvb_mzm.toPlainText(),self.cvb_trx.text(),"Şifahi",ana_ekran.user,str(datetime.now().strftime("%m-%d-%Y.%H:%M:%S")),self.daxil_no.text())
                            self.cur.execute (self.query,self.values)
                            self.con.commit()
                            QMessageBox.information(self, "Məlumat","Şifahi müraciətə düzəliş edildi")

                        elif axtaris_ekran.formas=="Yazılı":
                            self.cur.execute ("""Delete from yazili where  daxil_no=?""",(self.daxil_no.text(),))
                            self.con.commit()
                            self.cur.execute ("""INSERT INTO sifahi(sıra_no,daxil_no,tarix,vereq,ad_soyad,fin,tel,unvan,novu,xarakteri,netice,mezmun,icraci,for,cvb_mezmun,cvb_tarix,qeyd_eden,son_deyisdiren)
                                    VALUES 
                                    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(self.sira_no.text(),self.daxil_no.text(),self.tarix.text(),self.vereq.text(),self.ad.toPlainText(),self.fin.text(),self.tel.text(),self.unv.text(),self.nov.currentText(),self.xar.currentText(),self.netice.currentText(),self.mezmun.toPlainText(),self.icra.currentText(),"Şifahi",self.cvb_mzm.toPlainText(),self.cvb_trx.text(),ana_ekran.user,ana_ekran.user))
                            self.con.commit()
                            QMessageBox.information(self, "Məlumat","Yazılı müraciət 'şifahi' olaraq dəyişdirildi")

                        elif axtaris_ekran.formas=="Elektron":
                            self.cur.execute ("""Delete from elektron where  daxil_no=?""",(self.evveli,))
                            self.con.commit()
                            self.cur.execute ("""INSERT INTO sifahi(sıra_no,daxil_no,tarix,vereq,ad_soyad,fin,tel,unvan,novu,xarakteri,netice,mezmun,icraci,for,cvb_mezmun,cvb_tarix,qeyd_eden,son_deyisdiren)
                                    VALUES 
                                    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(self.sira_no.text(),self.daxil_no.text(),self.tarix.text(),self.vereq.text(),self.ad.toPlainText(),self.fin.text(),self.tel.text(),self.unv.text(),self.nov.currentText(),self.xar.currentText(),self.netice.currentText(),self.mezmun.toPlainText(),self.icra.currentText(),"Şifahi",self.cvb_mzm.toPlainText(),self.cvb_trx.text(),ana_ekran.user,ana_ekran.user))
                            self.con.commit()
                            QMessageBox.information(self, "Məlumat","Elektron müraciət 'şifahi' olaraq dəyişdirildi")

                    except Exception as e:
                        s = str(e)
                        print(s)
                        QMessageBox.information(self, "Məlumat","Şifahi müraciətə düzəliş edilmədi !")
                    
            elif self.radiobutton1.isChecked():
                if self.daxil_no.text()=="" :
                    QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş ola bilməz !")


                elif  not self.vereq.text().isnumeric():
                    QMessageBox.information(self, "Məlumat","Vərəq sayı bölməsi hərflərdən ibarət ola bilməz !")


                elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                    QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")

                elif  not self.fin.text()=="" and not len(self.fin.text())==7 :
                    QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
               

                elif  len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                    QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")


                #elif self.cvb_mzm.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müraciətə verilən cavabın məzmunu boş ola bilməz ")

                #elif self.tr==0:
                    #QMessageBox.information(self, "Məlumat","Cavab tarixini düzgün formatda daxil edin ")

                #elif self.cvb_ind.text()== "" :
                    #QMessageBox.information(self, "Məlumat","Cavab indeksi bölməsi boş ola bilməz ")

                #elif self.aid.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Aidiyət bölməsi boş ola bilməz ")


                elif self.sexs.text()== "" :
                    QMessageBox.information(self, "Məlumat","Müraciət ünvanlanan şəxsin adını daxil edin")
                    
                #elif self.gonderen.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müşaiyət məktubunu göndərən şəxsin adını daxil edin ")

                else:
                    try:
                        if axtaris_ekran.formas=="Yazılı":
                            self.query="""UPDATE yazili set sira_no=?,daxil_no=?,tarix=?,ad_soyad=?,fin=?,unvan=?,tel=?,vereqsay=?,nov=?,forması=?,yolu=?,kime=?,musaiyet=?,xarakteri=?,mezmun=?,derkenar=?,icraci=?,cvb_tarix=?,cvb_mezmun=?,cvb_indeksi=?,aidiyyat=?,nezaret=?,netice=?,for=? ,son_deyisdiren=? ,sonduztar=? where daxil_no=?"""
                            self.values=(self.sira_no.text(),self.daxil_no.text(),self.tarix.text(),self.ad.toPlainText(),self.fin.text(),self.unv.text(),self.tel.text(),self.vereq.text(),self.nov.currentText(),self.formasi.currentText(),self.yolu.currentText(),self.sexs.text(),self.gonderen.toPlainText(),self.xar.currentText(),self.mezmun.toPlainText(),self.derk.currentText(),self.icra.currentText(),self.cvb_trx.text(),self.cvb_mzm.toPlainText(),self.cvb_ind.text(),self.aid.toPlainText(),self.nez.currentText(),self.netice.currentText(),"Yazılı",ana_ekran.user,str(datetime.now().strftime("%m-%d-%Y.%H:%M:%S")),self.evveli)                       


                            self.cur.execute (self.query,self.values)
                            self.con.commit()
                            QMessageBox.information(self, "Məlumat","Yazılı müraciətə düzəliş edildi")

                        elif axtaris_ekran.formas=="Elektron": 
                            self.cur.execute ("""Delete from elektron where  daxil_no=?""",(self.evveli,))
                            self.con.commit()
                            self.cur.execute ("""INSERT INTO yazili(sira_no,daxil_no,tarix,ad_soyad,fin,unvan,tel,vereqsay,nov,forması,yolu,kime,musaiyet,xarakteri,mezmun,derkenar,icraci,cvb_tarix,cvb_mezmun,cvb_indeksi,aidiyyat,nezaret,netice,for,qeyd_eden,son_deyisdiren)
                                    VALUES :
                            
                                    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(self.sira_no.text(),
                                                                                    self.daxil_no.text(),
                                                                                    self.tarix.text(),
                                                                                    self.ad.toPlainText(),
                                                                                    self.fin.text(),
                                                                                    self.unv.text(),
                                                                                    self.tel.text(),
                                                                                    self.vereq.text(),
                                                                                    self.nov.currentText(),
                                                                                    self.formasi.currentText(),
                                                                                    self.yolu.currentText(),
                                                                                    self.sexs.text(),
                                                                                    self.gonderen.toPlainText(),
                                                                                    self.xar.currentText(),
                                                                                    self.mezmun.toPlainText(),
                                                                                    self.derk.currentText(),
                                                                                    self.icra.currentText(),
                                                                                    self.cvb_trx.text(),
                                                                                    self.cvb_mzm.toPlainText(),
                                                                                    self.cvb_ind.text(),
                                                                                    self.aid.toPlainText(),
                                                                                    self.nez.currentText(),
                                                                                    self.netice.currentText(),"Yazılı",ana_ekran.user,ana_ekran.user))
                            self.con.commit()
                            QMessageBox.information(self, "Məlumat","Elektron müraciət 'Yazılı' olaraq dəyişdirildi")
                    except Exception as e:
                        s=str(e)
                        print(s)
                        QMessageBox.information(self, "Məlumat","Yazılı müraciətə düzəliş edilmədi!")

            elif  self.radiobutton2.isChecked():
                if self.daxil_no.text()=="":
                    QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş ola bilməz !")

                elif  not self.vereq.text().isnumeric():
                    QMessageBox.information(self, "Məlumat","Vərəq sayı bölməsi hərflərdən ibarət ola bilməz !")


                elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                    QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")

                elif  not self.fin.text()=='' and not len(self.fin.text())==7 :
                    QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
               

                elif  len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                    QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")


                #elif self.cvb_mzm.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müraciətə verilən cavabın məzmunu boş ola bilməz ")

                #elif self.tr==0:
                    #QMessageBox.information(self, "Məlumat","Cavab tarixini düzgün formatda daxil edin ")

                #elif self.cvb_ind.text()== "" :
                    #QMessageBox.information(self, "Məlumat","Cavab indeksi bölməsi boş ola bilməz ")
                    
                #elif self.aid.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Aidiyət bölməsi boş ola bilməz ")


                elif self.sexs.text()== "" :
                    QMessageBox.information(self, "Məlumat"," Elektron müraciət 'yazılı' olaraq dəyişdirildi")
                    
                #elif self.gonderen.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müşaiyət məktubunu göndərən şəxsin adını daxil edin ")


                else:
                    try:
                        if axtaris_ekran.formas=="Elektron":
                            self.query="""UPDATE elektron set sira_no=?, daxil_no=?,tarix=?,ad_soyad=?,fin=?,unvan=?,tel=?,vereqsay=?,nov=?,forması=?,yolu=?,kime=?,musaiyet=?,xarakteri=?,mezmun=?,derkenar=?,icraci=?,cvb_tarix=?,cvb_mezmun=?,cvb_indeksi=?,aidiyyat=?,nezaret=?,netice=?,for=?,son_deyisdiren=?,sonduztar=? where daxil_no=?"""
                            self.values=(self.sira_no.text(),self.tarix.text(),self.ad.toPlainText(),self.fin.text(),self.unv.text(),self.tel.text(),self.vereq.text(),self.nov.currentText(),self.formasi.currentText(),self.yolu.currentText(),self.sexs.text(),self.gonderen.toPlainText(),self.xar.currentText(),self.mezmun.toPlainText(),self.derk.currentText(),self.icra.currentText(),self.cvb_trx.text(),self.cvb_mzm.toPlainText(),self.cvb_ind.text(),self.aid.toPlainText(),self.nez.currentText(),self.netice.currentText(),"Elektron",ana_ekran.user,str(datetime.now().strftime("%m-%d-%Y.%H:%M:%S")),self.daxil_no.text())                        
                            self.cur.execute(self.query,self.values)
                            self.con.commit()

                            QMessageBox.information(self, "Məlumat","Elektron müraciətə düzəliş edildi")

                            
                        elif axtaris_ekran.formas=="Yazılı":
                            self.cur.execute ("""Delete from yazili where daxil_no=?""",(self.daxil_no.text(),))
                            self.con.commit()
                            self.cur.execute ("""INSERT INTO elektron(sira_no,daxil_no,tarix,ad_soyad,fin,unvan,tel,vereqsay,nov,forması,yolu,kime,musaiyet,xarakteri,mezmun,derkenar,icraci,cvb_tarix,cvb_mezmun,cvb_indeksi,aidiyyat,nezaret,netice,for,qeyd_eden,deyisiklik_eden)
                            VALUES 
                            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(self.sira_no.text(),self.daxil_no.text(),
                                                                            self.tarix.text(),
                                                                            self.ad.toPlainText(),
                                                                            self.fin.text(),
                                                                            self.unv.text(),
                                                                            self.tel.text(),
                                                                            self.vereq.text(),
                                                                            self.nov.currentText(),
                                                                            self.formasi.currentText(),
                                                                            self.yolu.currentText(),
                                                                            self.sexs.text(),
                                                                            self.gonderen.toPlainText(),
                                                                            self.xar.currentText(),
                                                                            self.mezmun.toPlainText(),
                                                                            self.derk.currentText(),
                                                                            self.icra.currentText(),
                                                                            self.cvb_trx.text(),
                                                                            self.cvb_mzm.toPlainText(),
                                                                            self.cvb_ind.text(),
                                                                            self.aid.toPlainText(),
                                                                            self.nez.currentText(),
                                                                            self.netice.currentText(),"Elektron",ana_ekran.user,ana_ekran.user))

                            self.con.commit()
                            QMessageBox.information(self, "Məlumat","Yazılı müraciət 'elektron' olaraq dəyişdirildi")
                    except Exception as e:
                        s=str(e)
                        print(s)
                        QMessageBox.information(self, "Məlumat","Elektron müraciətə düzəliş edilmədi")

        except Exception as e:
            s=str(e)
            print("Pencere4_qeydd"+s)


        self.hide()
        axtaris_ekran.show()
            
    def er_yukle(self):
        os.chdir(sened_yolu+"\\Sənədlər")
        try:
            self.tr=0
            try:
                self.tr=1
            except ValueError:
                self.tr=0
            if self.daxil_no.text()=="":
                QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş ola bilməz !")
            elif  not self.vereq.text().isnumeric():
                QMessageBox.information(self, "Məlumat","Vərəq sayı bölməsi hərflərdən ibarət ola bilməz !")
            elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")
            elif  not self.fin.text()=="" and not len(self.fin.text())==7 :
                QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
            elif  len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")
            elif self.sexs.text()== "" :
                QMessageBox.information(self, "Məlumat","Müraciət ünvanlanan şəxsin adını daxil edin")                
            #elif self.gonderen.toPlainText()== "" :
                #QMessageBox.information(self, "Məlumat","Müşaiyət məktubunu göndərən şəxsin adını daxil edin ")
            else:
                import shutil
                os.chdir(self.yol)
                try:
                    yolu=sened_yolu+"\\Sənədlər"
                    os.chdir(yolu)
                    direk=os.listdir(os.getcwd())
                except:
                    QMessageBox.information(self, "Məlumat","Sənədlər qovluğu mövcud deyil")                
                if self.sira_no.text() not in direk:
                    os.mkdir(self.sira_no.text())
                    os.chdir(os.getcwd()+"/"+self.sira_no.text())
                    os.mkdir("Ərizələr")
                    os.mkdir("Cavablar")
                    os.chdir(self.yol)
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                files, _ = QFileDialog.getOpenFileNames(self,"Ərizə faylıni yüklə", "","Bütün fayllar (*);;MS WORD faylları (*.docx)", options=options)                                   
                source = files[0]
                if files[0][-4]=='.':
                    destination = yolu+'\\'+self.sira_no.text()+"/Ərizələr/"+self.ad.toPlainText()+files[0][-4:]
                else:
                    destination = yolu+'\\'+self.sira_no.text()+"/Ərizələr/"+self.ad.toPlainText()+files[0][-5:]
                    

                try:
                    shutil.copy(source, destination)
                    QMessageBox.information(self, "Məlumat","Ərizə faylı uğurla yükləndi ")         
                except shutil.SameFileError:
                    QMessageBox.information(self, "Məlumat","Bu sənəd artıq yüklənmişdir ")
                except PermissionError:
                    QMessageBox.information(self, "Məlumat","Bu əməliyyat üçün icazəniz yoxdur ")
                except:
                    QMessageBox.information(self, "Məlumat","Xəta baş verdi")
        except Exception as e:
            s=str(e)
            print("Pencere4_er_yukle"+s)
        os.chdir(self.yol)
            
    def cvb_yukle(self):
        os.chdir(sened_yolu+"\\Sənədlər")
        try:
            self.tr=0
            try:

                self.tr=1
            except ValueError:
                self.tr=0

            if self.daxil_no.text()=="":
                QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş ola bilməz !")
            elif  not self.vereq.text().isnumeric():
                QMessageBox.information(self, "Məlumat","Vərəq sayı bölməsi hərflərdən ibarət ola bilməz !")
            elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")
            elif  not self.fin.text()==''and not len(self.fin.text())==7 :
                QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
            elif  len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")
            #elif self.aid.toPlainText()== "" :
                #QMessageBox.information(self, "Məlumat","Aidiyət bölməsi boş ola bilməz ")
            elif self.sexs.text()== "" :
                QMessageBox.information(self, "Məlumat","Müraciət ünvanlanan şəxsin adını daxil edin")                
            #elif self.gonderen.toPlainText()== "" :
                #QMessageBox.information(self, "Məlumat","Müşaiyət məktubunu göndərən şəxsin adını daxil edin ")
            else:
                import shutil
                os.chdir(self.yol)
                try:
                    yolu=sened_yolu+"\\Sənədlər"
                    os.chdir(yolu)
                    direk=os.listdir(os.getcwd())
                except:
                    QMessageBox.information(self, "Məlumat","Sənədlər qovluğu mövcud deyil")                
                if self.sira_no.text() not in direk:
                    os.mkdir(self.sira_no.text())
                    os.chdir(os.getcwd()+"/"+self.sira_no.text())
                    os.mkdir("Ərizələr")
                    os.mkdir("Cavablar")
                    os.chdir(self.yol)
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                files, _ = QFileDialog.getOpenFileNames(self,"Cavab sənədini yüklə", "","Bütün fayllar (*);;MS WORD faylları (*.docx)", options=options)
                print(files[0][-4])
                print(files)
                source = files[0]
                if files[0][-4]=='.':
                    
                    destination = yolu+'\\'+self.sira_no.text()+"/Cavablar/"+self.ad.toPlainText()+files[0][-4:]
                else:
                    destination = yolu+'\\'+self.sira_no.text()+"/Cavablar/"+self.ad.toPlainText()+files[0][-5:]

                try:
                    shutil.copy(source, destination)
                    QMessageBox.information(self, "Məlumat","Cavab faylı uğurla yükləndi ")         
                except shutil.SameFileError:
                    QMessageBox.information(self, "Məlumat","Bu sənəd artıq yüklənmişdir ")
                except PermissionError:
                    QMessageBox.critical(self, "Məlumat","Bu əməliyyat üçün icazəniz yoxdur ")
                except:
                    QMessageBox.critical(self, "Məlumat","Xəta baş verdi")       
        except Exception as e:
            s=str(e)
            print("Pencere4_cvb_yukle"+s)       

        os.chdir(self.yol)
    def sened (self):
        os.chdir(self.yol)
        try:
            self.evvelde()
            self.tr=0
            try:

                self.tr=1
            except ValueError:
                self.tr=0

            if self.radiobutton.isChecked():

                if self.daxil_no.text()=="":
                    QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş ola bilməz !")

                elif  self.vereq.text().isnumeric():
                    QMessageBox.information(self, "Məlumat","Vərəq sayı bölməsi hərflərdən ibarət ola bilməz !")


                elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                    QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")

                elif  not self.fin.text()=='' and not len(self.fin.text())==7 :
                    QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
                elif  len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                    QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")

                #elif self.unv.text()=="" :
                    #QMessageBox.information(self, "Məlumat","Ünvan bölməsinə yaşayış yerini daxil edin")
                else:
                    try:
                        self.ev=''
                        for i in self.evv:
                            self.ev= self.ev + i +","
                            self.template = self.yol+"\\resurslar\\sablon.docx"
                            self.document = MailMerge(self.template)
                            self.document.merge(
                            formasi=self.formasi.currentText(),
                            novu=self.nov.currentText(),
                            daxil_no=self.daxil_no.text(),
                            sira_no=self.sira_no.text(),
                            tarixi=gunu,
                            ad_soyad=self.ad.toPlainText(),
                            fin_no=self.fin.text(),
                            unvan=self.unv.text(),
                            telefon=self.tel.text(),
                            yolu=self.yolu.currentText(),
                            vereq=self.vereq.text(),
                            xarakteri=self.xar.currentText(),
                            icraci=self.icra.currentText(),
                            derkenar=self.derk.currentText(),
                            nezaret=self.nez.currentText(),
                            aidiyyat=self.aid.toPlainText(),
                            sexs=self.sexs.text(),
                            evvelki=self.ev,
                            musaiyet=self.gonderen.toPlainText(),
                            neticesi=self.netice.currentText(),
                            cvb_tarixi=self.cvb_trx.text(),
                            cvb_indeksi=self.cvb_ind.text(),
                            mur_mezmun=self.mezmun.toPlainText(),
                            cvb_mezmun=self.cvb_mzm.toPlainText(),
                            rap_tarix=gunu,
                            form="şifahi")
                        self.document.write(self.yol+'/Endirilənlər/Şifahi/'+self.sira_no.text()+'.docx')
                        QMessageBox.information(self, "Məlumat","Şifahi müraciət yükləndi.")
                        self.yoxlama=True
                    except Exception as e:
                        s=str(e)
                        print(s)
                        QMessageBox.information(self, "Məlumat","Şifahi müraciət yüklənmədi")
                    
            elif self.radiobutton1.isChecked():
                
                if self.daxil_no.text()=="" :
                    QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş ola bilməz !")

                elif  not self.vereq.text().isnumeric():
                    QMessageBox.information(self, "Məlumat","Vərəq sayı bölməsi hərflərdən ibarət ola bilməz !")


                elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                    QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")

                elif  not self.fin.text()=='' and not len(self.fin.text())==7 :
                    QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
               

                elif len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                    QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")


                   
                #elif self.aid.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Aidiyət bölməsi boş ola bilməz ")


                elif self.sexs.text()== "" :
                    QMessageBox.information(self, "Məlumat","Müraciət ünvanlanan şəxsin adını daxil edin")
                    
                #elif self.gonderen.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müşaiyət məktubunu göndərən şəxsin adını daxil edin ")

                else:
                    try:
                        self.ev=''
                        for i in self.evv:
                            self.ev= self.ev + i +","
                        self.template = self.yol+"\\resurslar\\sablon.docx"
                        self.document = MailMerge(self.template)
                        self.document.merge(
                            formasi=self.formasi.currentText(),
                            novu=self.nov.currentText(),
                            daxil_no=self.daxil_no.text(),
                            sira_no=self.sira_no.text(),
                            tarixi=gunu,
                            ad_soyad=self.ad.toPlainText(),
                            fin_no=self.fin.text(),
                            unvan=self.unv.text(),
                            telefon=self.tel.text(),
                            yolu=self.yolu.currentText(),
                            vereq=self.vereq.text(),
                            xarakteri=self.xar.currentText(),
                            icraci=self.icra.currentText(),
                            derkenar=self.derk.currentText(),
                            nezaret=self.nez.currentText(),
                            aidiyyat=self.aid.toPlainText(),
                            sexs=self.sexs.text(),
                            evvelki=self.ev,
                            musaiyet=self.gonderen.toPlainText(),
                            neticesi=self.netice.currentText(),
                            cvb_tarixi=self.cvb_trx.text(),
                            cvb_indeksi=self.cvb_ind.text(),
                            mur_mezmun=self.mezmun.toPlainText(),
                            cvb_mezmun=self.cvb_mzm.toPlainText(),
                            rap_tarix=gunu,
                            form="yazılı")
                        self.document.write(self.yol+'/Endirilənlər/Yazılı/'+self.sira_no.text()+'.docx')
                        QMessageBox.information(self, "Məlumat","Yazılı müraciət yükləndi.")
                        self.yoxlama=True
                    except Exception as e:
                        s=str(e)
                        print(s)
                        QMessageBox.information(self, "Məlumat",s+ "Yazılı müraciət yüklənmədi")


            elif  self.radiobutton2.isChecked():
                if self.daxil_no.text()=="" :
                    QMessageBox.information(self, "Məlumat","Qeydiyyat nömrəsi boş ola bilməz !")


                elif  not self.vereq.text().isnumeric():
                    QMessageBox.information(self, "Məlumat","Vərəq sayı bölməsi hərflərdən ibarət ola bilməz !")


                elif self.ad.toPlainText()== "" or self.ad.toPlainText().isnumeric():
                    QMessageBox.information(self, "Məlumat","Ad , soyad boş və ya rəqəmlərdən ibarət ola bilməz !")

                elif  not self.fin.text()=='' and not len(self.fin.text())==7 :
                    QMessageBox.information(self, "Məlumat","FİN nömrəsini düzgün daxil edin!")
               

                elif  len(self.tel.text())>0 and (not len(self.tel.text())==9 or not self.tel.text().isnumeric()):
                    QMessageBox.information(self, "Məlumat","Telefon nömrəsini düzgün daxil edin!")


                #elif self.aid.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Aidiyət bölməsi boş ola bilməz ")


                elif self.sexs.text()== "" :
                    QMessageBox.information(self, "Məlumat","Müraciət ünvanlanan şəxsin adını daxil edin")
                    
                #elif self.gonderen.toPlainText()== "" :
                    #QMessageBox.information(self, "Məlumat","Müşaiyət məktubunu göndərən şəxsin adını daxil edin ")


                else:
                    try:
                        self.ev=''
                        for i in self.evv:
                            self.ev= self.ev + i +","
                        self.template = self.yol+"\\resurslar\\sablon.docx"
                        self.document = MailMerge(self.template)
                        self.document.merge(
                            formasi=self.formasi.currentText(),
                            novu=self.nov.currentText(),
                            daxil_no=self.daxil_no.text(),
                            sira_no=self.sira_no.text(),
                            tarixi=gunu,
                            ad_soyad=self.ad.toPlainText(),
                            fin_no=self.fin.text(),
                            unvan=self.unv.text(),
                            telefon=self.tel.text(),
                            yolu=self.yolu.currentText(),
                            vereq=self.vereq.text(),
                            xarakteri=self.xar.currentText(),
                            icraci=self.icra.currentText(),
                            derkenar=self.derk.currentText(),
                            nezaret=self.nez.currentText(),
                            aidiyyat=self.aid.toPlainText(),
                            sexs=self.sexs.text(),
                            evvelki=self.ev,
                            musaiyet=self.gonderen.toPlainText(),
                            neticesi=self.netice.currentText(),
                            cvb_tarixi=self.cvb_trx.text(),
                            cvb_indeksi=self.cvb_ind.text(),
                            mur_mezmun=self.mezmun.toPlainText(),
                            cvb_mezmun=self.cvb_mzm.toPlainText(),
                            rap_tarix=gunu,
                            form="elektron")
                        self.document.write(self.yol+'/Endirilənlər/Elektron/'+self.sira_no.text()+'.docx')
                        QMessageBox.information(self, "Məlumat","Elektron müraciət yükləndi.")
                        self.yoxlama=True
                    except:
                        QMessageBox.information(self, "Məlumat","Elektron müraciət yüklənmədi")
        except Exception as e:
            s=str(e)
            print("Pencere4_sened"+s)
                        
    def yoxla(self):
        try:
            self.sifahilist=[]
            self.yazililist=[]
            self.elektronlist=[]
            
            self.yoxs=self.cur.execute("""select daxil_no from sifahi""")        
            self.yoxs1=self.yoxs.fetchall()
            for i in self.yoxs1:
                self.sifahilist.append(str(i[0]).strip())

            self.yoxy=self.cur.execute("""select daxil_no from yazili""")        
            self.yoxy1=self.yoxy.fetchall()
            for i in self.yoxy1:
                self.yazililist.append(str(i[0]).strip())
            
            self.yoxe=self.cur.execute("""select daxil_no from elektron""")        
            self.yoxe1=self.yoxe.fetchall()
            for i in self.yoxe1:
                self.elektronlist.append(str(i[0]).strip())
        except Exception as e:
            s=str(e)
            print("Pencere4_yoxla"+s)
    def printet(self):
        try:
            if  self.radiobutton.isChecked():
                os.chdir(self.yol+"/Endirilənlər/Şifahi")
            elif  self.radiobutton1.isChecked():
                os.chdir(self.yol+"/Endirilənlər/Yazılı")       
            elif  self.radiobutton2.isChecked():
                os.chdir(self.yol+"/Endirilənlər/Elektron")   
            
            senedler=os.listdir()
            if not self.daxil_no.text()+".docx" in senedler:
                self.sened()
            if self.yoxlama==True:   
                

                try:

                    convert(self.daxil_no.text()+'.docx', self.daxil_no.text()+'.pdf')
                    def get_adobe_executable():
                        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as conn:
                            
                            with winreg.OpenKey(conn, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\AcroRd32.exe', 0, winreg.KEY_READ) as hkey:
                                value = winreg.QueryValue(hkey, None)
                                if value:
                                    value = '"{}"'.format(value)
                                    return value.strip()
                        return None

                    def print_pdf_file(file, printer_name=None, secs=5):
                        cmd = get_adobe_executable()
                        if cmd is None:
                            return False
                        if printer_name:
                            cmd = '{} /h /t "{}" "{}"'.format(cmd, file, printer_name)
                        else:
                            cmd = '{} /p /h "{}"'.format(cmd, file)
                        proc = subprocess.Popen(cmd)
                        time.sleep(secs)
                        proc.kill()
                        #os.remove(self.daxil_no.text()+'.pdf')

                    print_pdf_file(self.daxil_no.text()+'.pdf')
                    
                except Exception as e:
                    s=str(e)
                    print("Duzelis_ekran.printet"+s)

        except Exception as e:
            s=str(e)
            print("Pencere4_printet"+s)


class Pencere5(QWidget):

    def __init__(self):
       
            super().__init__()
            self.setFixedSize(850, 750)
            qtRectangle = self.frameGeometry()
            centerPoint = QDesktopWidget().availableGeometry().center()
            qtRectangle.moveCenter(centerPoint)
            self.move(qtRectangle.topLeft())
            self.setStyleSheet("background-color: #ce6e2f")
            self.setWindowTitle("Müraciətin tərkibi")
            self.yol=os.getcwd()
            self.sened()
            self.yoxlama=''


            basliq = QLabel(self)
            basliq.move(0, 0)
            basliq.resize(850,30)
            basliq.setStyleSheet("background-color: #bebebe;")


           
            self.radiobutton = QRadioButton(basliq)
            self.radiobutton.setText("Şifahi müraciət")
            self.radiobutton.setChecked(False)
            self.radiobutton.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")
            self.radiobutton.move(30, 5)
            self.radiobutton.toggled.connect(self.sifahi)
            self.radiobutton.setEnabled(False)

            self.radiobutton1 = QRadioButton(basliq)
            self.radiobutton1.setText("Yazılı müraciət")
            self.radiobutton1.setChecked(False)
            self.radiobutton1.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")
            self.radiobutton1.move(250, 5)
            self.radiobutton1.toggled.connect(self.yazili)
            self.radiobutton1.setEnabled(False)

            self.radiobutton2 = QRadioButton(basliq)
            self.radiobutton2.setText("Elektron müraciət")
            self.radiobutton2.setChecked(False)
            self.radiobutton2.setStyleSheet("font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;color : black;")
            self.radiobutton2.move(470, 5)
            self.radiobutton2.toggled.connect(self.elektron)
            self.radiobutton2.setEnabled(False)

            self.sira_no = QLineEdit(self)
            self.sira_no.move(200, 74)
            self.sira_no.resize(100,22)
            self.sira_no.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.sira_no_lab = QLabel(self)
            self.sira_no_lab.move(20, 74)
            self.sira_no_lab.resize(180,25)
            self.sira_no_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.sira_no_lab.setText("Sıra nömrəsi")
            self.sira_no.setEnabled(False)

            self.derk = QLineEdit(self)
            self.derk.move(660, 74)
            self.derk.resize(150,22)
            self.derk.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.derk_lab = QLabel(self)
            #self.derk.setWordWrap(True)
            self.derk_lab.move(430, 74)
            self.derk_lab.resize(170,25)
            self.derk_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.derk_lab.setText("Dərkənar")
            self.derk.setEnabled(False)

     
            self.daxil_no = QLineEdit(self)
            self.daxil_no.move(200, 113)
            self.daxil_no.resize(200,22)
            self.daxil_no.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.daxil_no_lab = QLabel(self)
            self.daxil_no_lab.move(20, 113)
            self.daxil_no_lab.resize(180,25)
            self.daxil_no_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.daxil_no_lab.setText("Qeydiyyat nömrəsi")
            self.daxil_no.setEnabled(False)

            self.formasi = QLineEdit(self)
            self.formasi.move(660, 113)
            self.formasi.resize(150,22)
            self.formasi.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.formasi_lab = QLabel(self)
            #self.formasi.setWordWrap(True)
            self.formasi_lab.move(430, 113)
            self.formasi_lab.resize(170,25)
            self.formasi_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.formasi_lab.setText("Müraciətin forması")
            self.formasi.setEnabled(False)


            self.tarix = QLineEdit(self)
            self.tarix.move(200, 152)
            self.tarix.resize(100,22)
            self.tarix.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.tarix_lab = QLabel(self)
            self.tarix_lab.move(20, 152)
            self.tarix_lab.resize(180,25)
            self.tarix_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.tarix_lab.setText("Qeydiyyat tarixi")
            #self.tarix.setDate(QDate.currentDate())
            self.tarix.setEnabled(False)

            self.yolu = QLineEdit(self)
            self.yolu.move(660, 152)
            self.yolu.resize(150,22)
            self.yolu.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.yolu_lab = QLabel(self)
            #self.yolu.setWordWrap(True)
            self.yolu_lab.move(430, 152)
            self.yolu_lab.resize(170,25)
            self.yolu_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.yolu_lab.setText("Müraciətin Qeydiyyat yolu")
            self.yolu.setEnabled(False)
            
            self.vereq= QLineEdit(self)
            self.vereq.move(200, 191)
            self.vereq.resize(100,22)
            self.vereq.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.vereq_lab = QLabel(self)
            self.vereq_lab.move(20, 191)
            self.vereq_lab.resize(180,25)
            self.vereq_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.vereq_lab.setText("Vərəq sayı ")
            self.vereq.setEnabled(False)

            self.sexs = QLineEdit(self)
            self.sexs.move(660, 191)
            self.sexs.resize(150,22)
            self.sexs.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.sexs_lab = QLabel(self)
            self.sexs_lab.move(430, 191)
            self.sexs_lab.resize(170,25)
            self.sexs_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.sexs_lab.setText("Ünvanlandığı şəxs")
            self.sexs.setEnabled(False)


            self.ad = QTextEdit(self)
            self.ad.move(200, 221)
            self.ad.resize(200,40)
            self.ad.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.ad_lab = QLabel(self)
            self.ad_lab.move(20, 230)
            self.ad_lab.resize(180,25)
            self.ad_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.ad_lab.setText("Ad,soyad,ata adı")
            self.ad.setEnabled(False)

            self.evvel = QLineEdit(self)
            self.evvel.move(660, 230)
            self.evvel.resize(150,22)
            self.evvel.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.evvel_lab = QLabel(self)
            self.evvel_lab.move(430, 230)
            self.evvel_lab.resize(170,25)
            self.evvel_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.evvel_lab.setText("Əvvəlki müraciətlər")
            self.evvel.setEnabled(False)

            self.fin = QLineEdit(self)
            self.fin.move(200, 269)
            self.fin.resize(100,22)
            self.fin.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.fin_lab = QLabel(self)
            self.fin_lab.move(20, 269)
            self.fin_lab.resize(180,25)
            self.fin_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.fin_lab.setText("FİN nömrəsi")
            self.fin.setEnabled(False)

            self.gonderen = QTextEdit(self)
            self.gonderen.move(580, 259)
            self.gonderen.resize(230,40)
            self.gonderen.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 9pt;font-weight: bold;color : black;")
            self.gonderen_lab = QLabel(self)
            self.gonderen_lab.move(430, 259)
            self.gonderen_lab.resize(150,35)
            self.gonderen_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.gonderen_lab.setText("Müşaiyət məktubunu göndərən")
            self.gonderen.setEnabled(False)
            self.gonderen_lab.setWordWrap(True)
            
            self.unv = QLineEdit(self)
            self.unv.move(200, 308)
            self.unv.resize(610,22)
            self.unv.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.unv_lab = QLabel(self)
            self.unv_lab.move(20, 308)
            self.unv_lab.resize(180,25)
            self.unv_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.unv_lab.setText("Ünvanı")
            self.unv.setEnabled(False)

            self.tel = QLineEdit(self)
            self.tel.move(200, 347)
            self.tel.resize(100,22)
            self.tel.setStyleSheet("font-family: Arial;background-color :  #ffffff ;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.tel_lab = QLabel(self)
            self.tel_lab.move(20, 347)
            self.tel_lab.resize(180,25)
            self.tel_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.tel_lab.setText("Telefon nömrəsi")
            self.tel.setEnabled(False)

            self.nov = QLineEdit(self)
            self.nov.move(660, 347)
            self.nov.resize(150,22)
            self.nov.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.nov_lab = QLabel(self)
            self.nov_lab.move(430, 347)
            self.nov_lab.resize(130,25)
            self.nov_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.nov_lab.setText("Müraciətin növü")
            self.nov.setEnabled(False)

            self.xar = QTextEdit(self)
            self.xar.move(200, 386)
            self.xar.resize(610,44)
            self.xar.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.xar_lab = QLabel(self)
            self.xar_lab.move(20, 406)
            self.xar_lab.resize(180,25)
            self.xar_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.xar_lab.setText("Müraciətin xarakteri")
            self.xar.setEnabled(False)


            self.mezmun = QTextEdit(self)
            self.mezmun.move(200, 445)
            self.mezmun.resize(610,44)
            self.mezmun.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.mezmun_lab = QLabel(self)
            self.mezmun_lab.move(20, 465)
            self.mezmun_lab.resize(180,25)
            self.mezmun_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.mezmun_lab.setText("Müraciətin qısa məzmnu")
            self.mezmun.setEnabled(False)

            self.cvb_mzm = QTextEdit(self)
            self.cvb_mzm.move(200, 504)
            self.cvb_mzm.resize(610,44)
            self.cvb_mzm.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.cvb_mzm_lab = QLabel(self)
            self.cvb_mzm_lab.move(20, 524)
            self.cvb_mzm_lab.resize(150,25)
            self.cvb_mzm_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.cvb_mzm_lab.setText("Cavabın məzmunu")
            self.cvb_mzm.setEnabled(False)

       
            self.icra = QLineEdit(self)
            self.icra.move(200, 563)
            self.icra.resize(190,22)
            self.icra.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.icra_lab = QLabel(self)
            self.icra_lab.move(20, 563)
            self.icra_lab.resize(180,25)
            self.icra_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.icra_lab.setText("İcraçı")
            self.icra.setEnabled(False)

            self.cvb_ind = QLineEdit(self)
            self.cvb_ind.move(610, 563)
            self.cvb_ind.resize(200,22)
            self.cvb_ind.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.cvb_ind_lab = QLabel(self)
            self.cvb_ind_lab.move(430, 563)
            self.cvb_ind_lab.resize(120,25)
            self.cvb_ind_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.cvb_ind_lab.setText("Cavabın indeksi")
            self.cvb_ind.setEnabled(False)

            self.netice = QLineEdit(self)
            self.netice.move(200, 602)
            self.netice.resize(190,22)
            self.netice.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.netice_lab = QLabel(self)
            self.netice_lab.move(20, 602)
            self.netice_lab.resize(150,25)
            self.netice_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.netice_lab.setText("Nəticəsi")
            self.netice.setEnabled(False)

            self.nez = QLineEdit(self)
            self.nez.move(610, 602)
            self.nez.resize(200,22)
            self.nez.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.nez_lab = QLabel(self)
            self.nez_lab.move(430, 602)
            self.nez_lab.resize(75,25)
            self.nez_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.nez_lab.setText("Nəzarət")
            self.netice.setEnabled(False)


            self.cvb_trx = QLineEdit(self)
            self.cvb_trx.move(200, 661)
            self.cvb_trx.resize(190,22)
            self.cvb_trx.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.cvb_trx_lab = QLabel(self)
            self.cvb_trx_lab.move(20, 661)
            self.cvb_trx_lab.resize(150,25)
            self.cvb_trx_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.cvb_trx_lab.setText("Cavabın tarixi")
            self.cvb_trx.setEnabled(False)

            self.aid = QTextEdit(self)
            self.aid.move(510,641)
            self.aid.resize(300,44)
            self.aid.setStyleSheet("font-family: Arial;background-color :  #ffffff;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.aid_lab = QLabel(self)
            self.aid_lab.move(430, 661)
            self.aid_lab.resize(75,25)
            self.aid_lab.setStyleSheet("font-family: Arial;font-style: normal;font-size: 11pt;font-weight: bold;color : black;")
            self.aid_lab.setText("Aidiyyət")
            self.aid.setEnabled(False)

            self.cerci=QFrame(self)
            self.cerci.resize(850,40)
            self.cerci.move(0,710)
            self.cerci.setStyleSheet("background-color :  #bebebe;")
                
            self.printe=QPushButton(self)
            self.printe.resize(39,39)
            self.printe.move(5,711)
            self.printe.setStyleSheet("background-image : url(resurslar/pr1.jpg);")
            self.printe.clicked.connect(self.printet)


            self.qayittt=QPushButton(self)
            self.qayittt.resize(160,25)
            self.qayittt.move(680,719)
            self.qayittt.setText("Əsas menyuya qayıt")
            self.qayittt.clicked.connect(self.qayit)
            self.qayittt.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 10pt;font-weight: bold;color : black;")

            self.qeydet=QPushButton(self)
            self.qeydet.resize(160,25)
            self.qeydet.move(515,719)
            self.qeydet.setText("Düzəliş et")
            self.qeydet.clicked.connect(self.duzeli)
            self.qeydet.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 10pt;font-weight: bold;color : black;")

            self.erizeler=QPushButton(self)
            self.erizeler.resize(160,25)
            self.erizeler.move(350,719)
            self.erizeler.setText("Ərizəyə bax")
            self.erizeler.clicked.connect(self.eriz)
            self.erizeler.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 10pt;font-weight: bold;color : black;")

            self.cavablar=QPushButton(self)
            self.cavablar.resize(160,25)
            self.cavablar.move(185,719)
            self.cavablar.setText("Cavaba bax")
            self.cavablar.clicked.connect(self.cvb)
            self.cavablar.setStyleSheet("font-family: Arial;font-style: normal;background-color :  #ffffff;font-size: 10pt;font-weight: bold;color : black;")

    def sifahi(self):
        try:
            self.nez.hide()
            self.nez_lab.hide()
            self.aid.hide()
            self.aid_lab.hide()
            self.cvb_ind.hide()
            self.cvb_ind_lab.hide()
            self.derk.hide()
            self.derk_lab.hide()
            self.formasi.hide()
            self.formasi_lab.hide()
            self.yolu.hide()
            self.yolu_lab.hide()
            self.sexs.hide()
            self.sexs_lab.hide()
            self.evvel.hide()
            self.evvel_lab.hide()
            self.gonderen.hide()
            self.gonderen_lab.hide()
            self.vereq.hide()
            self.vereq_lab.hide()
        except Exception as e:
            s=str(e)
            print("Pencere2_sifahi"+s)

            
    def yazili(self):
        try:
            self.nez.show()
            self.nez_lab.show()
            self.aid.show()
            self.aid_lab.show()
            self.cvb_ind.show()
            self.cvb_ind_lab.show()
            self.derk.show()
            self.derk_lab.show()
            self.formasi.show()
            self.formasi_lab.show()
            self.yolu.show()
            self.yolu_lab.show()
            self.sexs.show()
            self.sexs_lab.show()
            self.evvel.show()
            self.evvel_lab.show()
            self.gonderen.show()
            self.gonderen_lab.show()
            self.vereq.show()
            self.vereq_lab.show()
        except Exception as e:
           s=str(e)
           print("Pencere2_yazili"+s)

    def elektron(self):
        try:
            self.nez.show()
            self.nez_lab.show()
            self.aid.show()
            self.aid_lab.show()
            self.cvb_ind.show()
            self.cvb_ind_lab.show()
            self.derk.show()
            self.derk_lab.show()
            self.formasi.show()
            self.formasi_lab.show()
            self.yolu.show()
            self.yolu_lab.show()
            self.sexs.show()
            self.sexs_lab.show()
            self.evvel.show()
            self.evvel_lab.show()
            self.gonderen.show()
            self.gonderen_lab.show()
            self.vereq.show()
            self.vereq_lab.show()
        except Exception as e:
            s=str(e)
            print("Pencere2_elektron"+s)

    def eriz(self):
        
        try:
            os.chdir(sened_yolu+'\\Sənədlər\\'+self.sira_no.text()+'\\Ərizələr')
            self.dizin=QFileDialog.getOpenFileName(self, 'Müracətə aid ərizələr',os.getcwd())
            os.popen(self.dizin[0])
        except Exception as e:
            os.chdir(self.yol)           
            QMessageBox.critical(self, "Səhv","Bu müraciətə aid sənəd yoxdur !")
            s=str(e)
            print("Pencere5_erize"+s)    


    def cvb(self):
        try:
            os.chdir(sened_yolu+'\\Sənədlər\\'+self.sira_no.text()+'\\Cavablar')
            self.dizin=QFileDialog.getOpenFileName(self, 'Müracətə aid cavab sənədləri',os.getcwd())
            os.popen(self.dizin[0])
        except Exception as e:
            os.chdir(self.yol)           
            QMessageBox.critical(self, "Səhv","Bu müraciətə aid cavab yoxdur !")
            s=str(e)
            print("Pencere5_cavab"+s)         


    def printet(self):
        try:
            if  self.radiobutton.isChecked():
                os.chdir(self.yol+"/Endirilənlər/Şifahi")
            elif  self.radiobutton1.isChecked():
                os.chdir(self.yol+"/Endirilənlər/Yazılı")       
            elif  self.radiobutton2.isChecked():
                os.chdir(self.yol+"/Endirilənlər/Elektron")   
            
            senedler=os.listdir()
            if not self.daxil_no.text()+".docx" in senedler:
                self.sened()
            if self.yoxlama==True:   


                    convert(self.daxil_no.text()+'.docx', self.daxil_no.text()+'.pdf')
                    def get_adobe_executable():
                        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as conn:
                            
                            with winreg.OpenKey(conn, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\AcroRd32.exe', 0, winreg.KEY_READ) as hkey:
                                value = winreg.QueryValue(hkey, None)
                                if value:
                                    value = '"{}"'.format(value)
                                    return value.strip()
                        return None

                    def print_pdf_file(file, printer_name=None, secs=5):
                        cmd = get_adobe_executable()
                        if cmd is None:
                            return False
                        if printer_name:
                            cmd = '{} /h /t "{}" "{}"'.format(cmd, file, printer_name)
                        else:
                            cmd = '{} /p /h "{}"'.format(cmd, file)
                        proc = subprocess.Popen(cmd)
                        time.sleep(secs)
                        proc.kill()
                        #os.remove(self.daxil_no.text()+'.pdf')

                    print_pdf_file(self.daxil_no.text()+'.pdf')
        except Exception as e:
            s=str(e)
            print("Duzelis_ekran.printet"+s)

    def duzeli(self):
        if not ana_ekran.user =="Sahilə Bağırova" and not ana_ekran.user==axtaris_ekran.user1:
            duzelis_ekran.erize_yukle.setEnabled(False)
            duzelis_ekran.cavab_yukle.setEnabled(False)
            duzelis_ekran.qeydet.setEnabled(False)
            duzelis_ekran.legvet.setEnabled(False)
        else:
            duzelis_ekran.erize_yukle.setEnabled(True)
            duzelis_ekran.cavab_yukle.setEnabled(True)
            duzelis_ekran.qeydet.setEnabled(True)
            duzelis_ekran.legvet.setEnabled(True)
        self.hide()
        duzelis_ekran.show()

    def sened (self):
        pass
    def qayit(self):
        self.hide()
        axtaris_ekran.show()
         
if __name__=="__main__":
    app = QApplication(sys.argv)
    ana_ekran=Pencere()
    login_ekran=Pencere1()
    muraciet_ekran=Pencere2()
    axtaris_ekran=Pencere3()
    duzelis_ekran=Pencere4()
    pdfac=Pencere5()
    ana_ekran.show()
    sys.exit(app.exec_())










    
