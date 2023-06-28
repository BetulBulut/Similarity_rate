import sys
import time

import concurrent.futures
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from AnasayfaUI import *
import pandas as pd
import threading

from TextUI import *

app2=QtWidgets.QApplication(sys.argv)
pencere2=QtWidgets.QWidget()
text_ui=Ui_text()
text_ui.setupUi(pencere2)
pencere2.show()


app=QtWidgets.QApplication(sys.argv)
pencere=QtWidgets.QWidget()
anasayfa_ui=Ui_Form()
anasayfa_ui.setupUi(pencere)
pencere.show()





def BenzerBul(x,benzer,oran,filt):
    t1_start = time.perf_counter()

    first = x["{}".format(benzer)].lower().split()
    list=[x]
    for i in range(len(filt)):
        sayac = 0
        y=filt.iloc[i,:]
        second = y["{}".format(benzer)].lower().split()
        if(len(second)>=len(first)):
            for a in range(len(first)):
                if(first[a] in second):
                    sayac+=1
        else:
            for a in range(len(second)):
                if(second[a] in first):
                    sayac+=1

        formul = (sayac / max(len(first), len(second))) * 100
        if (formul >= int(oran)):
            list.append(int(formul))
            list.append(y)
    if(len(list)>1):
        t2_start = time.perf_counter()
        list.append("{} : {} ".format(threading.get_native_id(),t2_start-t1_start))
        return list
    else:

        return ""

def getir():
    t1=time.perf_counter()

    df=pd.read_csv('son.csv')

    df = df.head(200)

    secici_ozellik=anasayfa_ui.ozellik_combobox.currentText()
    thread_sayısı=anasayfa_ui.therad_sayisi_edit.text()
    deger=anasayfa_ui.deger_edit.text()
    aynı_sutun=anasayfa_ui.sutun1_edit.text()
    benzer_sutun=anasayfa_ui.sutun2_edit.text()
    gosterilecek_ozellik=anasayfa_ui.show_ozellik_edit.text()
    oran=anasayfa_ui.oran_edit.text()



    if (deger !='') & (secici_ozellik !='') & (benzer_sutun !=''):

        if(secici_ozellik== "Complaint ID"):
            filt = df[df["{}".format(secici_ozellik)] == int(deger)]
        else:
            filt = df[df["{}".format(secici_ozellik)] == "{}".format(deger)]

        result=[]

        with concurrent.futures.ThreadPoolExecutor(max_workers= int(thread_sayısı)) as executor:

            for i in range(len(filt)):
                    result.append(executor.submit(BenzerBul, filt.iloc[i, :], benzer_sutun, oran, filt.iloc[i+1:,:]))

            if (gosterilecek_ozellik != ''):
                for f in result:
                    sayac = 0

                    text_ui.plainTextEdit.appendPlainText("****************************************")
                    for i in f.result():
                        if(sayac == len(f.result())-1):
                            text_ui.plainTextEdit.appendPlainText(i)

                        elif (sayac == 0):

                            text_ui.plainTextEdit.appendPlainText("ASIL KAYIT")
                            text_ui.plainTextEdit.appendPlainText(str(i["{}".format(gosterilecek_ozellik)]))
                        elif (sayac % 2 == 0):

                            text_ui.plainTextEdit.appendPlainText("Oranında benziyor: ")
                            text_ui.plainTextEdit.appendPlainText(str(i["{}".format(gosterilecek_ozellik)]))

                        else:

                            text_ui.plainTextEdit.appendPlainText("% {}".format(i))
                            x = 0
                        sayac += 1

            else:
                for f in result:
                    sayac = 0
                    print("**************************")
                    text_ui.plainTextEdit.appendPlainText("****************************************")
                    for i in f.result():
                        if (sayac == len(f.result()) - 1):
                            text_ui.plainTextEdit.appendPlainText(i)

                        elif (sayac == 0):

                            text_ui.plainTextEdit.appendPlainText("ASIL KAYIT")
                            text_ui.plainTextEdit.appendPlainText(str(i))

                        elif (sayac % 2 == 0):

                            text_ui.plainTextEdit.appendPlainText("Oranında benziyor: ")
                            text_ui.plainTextEdit.appendPlainText(str(i))

                        else:
                            text_ui.plainTextEdit.appendPlainText("% {}".format(i))

                            y = 0
                        sayac += 1


    elif aynı_sutun !='' and benzer_sutun !='':

        filt = df.groupby("{}".format(aynı_sutun))
        for key in filt.groups.keys():
            newdf = filt.get_group("{}".format(key))
            result = []


            with concurrent.futures.ThreadPoolExecutor(max_workers=int(thread_sayısı)) as executor:
                for i in range(len(newdf)):
                    result.append(executor.submit(BenzerBul, newdf.iloc[i, :], benzer_sutun, oran, newdf.iloc[i+1:,:]))

                if(gosterilecek_ozellik != ''):
                    for f in result:
                        sayac = 0

                        text_ui.plainTextEdit.appendPlainText("****************************************")
                        for i in f.result():

                            if (sayac == len(f.result()) - 1):
                                text_ui.plainTextEdit.appendPlainText(i)

                            elif (sayac == 0):

                                text_ui.plainTextEdit.appendPlainText("ASIL KAYIT")
                                text_ui.plainTextEdit.appendPlainText(str(i["{}".format(gosterilecek_ozellik)]))
                            elif (sayac % 2 == 0):

                                text_ui.plainTextEdit.appendPlainText("Oranında benziyor: ")
                                text_ui.plainTextEdit.appendPlainText(str(i["{}".format(gosterilecek_ozellik)]))

                            else:

                                text_ui.plainTextEdit.appendPlainText("% {}".format(i))
                                x = 0
                            sayac += 1

                else:
                    for f in result:
                        sayac = 0
                        print("**************************")
                        text_ui.plainTextEdit.appendPlainText("****************************************")
                        for i in f.result():
                            if (sayac == len(f.result()) - 1):
                                text_ui.plainTextEdit.appendPlainText(i)

                            elif (sayac == 0):

                                text_ui.plainTextEdit.appendPlainText("ASIL KAYIT")
                                text_ui.plainTextEdit.appendPlainText(str(i))

                            elif (sayac % 2 == 0):

                                text_ui.plainTextEdit.appendPlainText("Oranında benziyor: ")
                                text_ui.plainTextEdit.appendPlainText(str(i))

                            else:
                                text_ui.plainTextEdit.appendPlainText("% {}".format(i))

                                y = 0
                            sayac += 1


    elif benzer_sutun != '':
            filt=df

            result = []


            with concurrent.futures.ThreadPoolExecutor(max_workers=int(thread_sayısı)) as executor:

                for i in range(len(filt)):
                    result.append(executor.submit(BenzerBul, filt.iloc[i, :], benzer_sutun, oran, filt.iloc[i+1:,:]))

                if (gosterilecek_ozellik != ''):
                    for f in result:
                        sayac = 0

                        text_ui.plainTextEdit.appendPlainText("****************************************")
                        for i in f.result():

                            if (sayac == len(f.result()) - 1):
                                text_ui.plainTextEdit.appendPlainText(i)

                            elif (sayac == 0):

                                text_ui.plainTextEdit.appendPlainText("ASIL KAYIT")
                                text_ui.plainTextEdit.appendPlainText(str(i["{}".format(gosterilecek_ozellik)]))
                            elif (sayac % 2 == 0):

                                text_ui.plainTextEdit.appendPlainText("Oranında benziyor: ")
                                text_ui.plainTextEdit.appendPlainText(str(i["{}".format(gosterilecek_ozellik)]))

                            else:

                                text_ui.plainTextEdit.appendPlainText("% {}".format(i))
                                x = 0
                            sayac += 1

                else:
                    for f in result:
                        sayac = 0
                        print("**************************")
                        text_ui.plainTextEdit.appendPlainText("****************************************")
                        for i in f.result():
                            if (sayac == len(f.result()) - 1):
                                text_ui.plainTextEdit.appendPlainText(i)

                            elif (sayac == 0):

                                text_ui.plainTextEdit.appendPlainText("ASIL KAYIT")
                                text_ui.plainTextEdit.appendPlainText(str(i))

                            elif (sayac % 2 == 0):

                                text_ui.plainTextEdit.appendPlainText("Oranında benziyor: ")
                                text_ui.plainTextEdit.appendPlainText(str(i))

                            else:
                                text_ui.plainTextEdit.appendPlainText("% {}".format(i))

                                y = 0
                            sayac += 1





    else:
        print("eksik değer girdiniz!")

    t2 = time.perf_counter()

    text_ui.plainTextEdit.appendPlainText("TOPLAM SÜRE:")
    text_ui.plainTextEdit.appendPlainText(str(t2-t1))
    # burada süre arayüzüne bastırılacak toplam süre


anasayfa_ui.Getir.clicked.connect(getir)

sys.exit(app.exec())












