from PyQt5 import uic
if __name__ == '__main__':
    with open ('AnasayfaUI.py','w',encoding="utf-8") as fout:
        uic.compileUi('arayuz.ui',fout)