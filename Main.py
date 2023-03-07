import os
import sys
import random
import chardet
from wordBank import Ui_MainWindow
from listWindow import Ui_Dialog
from os import environ
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from wordBank import *

###Convert UI to PyQt5 py file###
os.system("pyuic5 -o wordBank.py wordBank.ui")


environ["QT_DEVICE_PIXEL_RATIO"] = "0"
environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
environ["QT_SCREEN_SCALE_FACTORS"] = "1"
environ["QT_SCALE_FACTOR"] = "1"

class MainWindow(QMainWindow):

    def openWindow(self,rowCount, englishList, turkishList):
        self.window = QtWidgets.QDialog()
        self.dialog_ui = Ui_Dialog()  # create a new instance of Ui_Dialog for the dialog window
        self.dialog_ui.setupUi(self.window,int(rowCount))
        self.window.setWindowTitle("Kelime Listesi")
        self.window.finished.connect(self.window.close)

        for i in range(len(englishList)):
            self.dialog_ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(englishList[i]))

        for j in range(len(turkishList)):
            self.dialog_ui.tableWidget.setItem(j, 1, QtWidgets.QTableWidgetItem(turkishList[j]))    

        self.window.show()
    
    def generateWords(self):
        rowCount = int(self.ui.wordNumberComboBox.currentText())
        englishList = []
        turkishList = []
        pathTr = os.path.join("assets", "turkish.txt")
        pathEn = os.path.join("assets", "english.txt")

        with open(pathTr, "rb") as t:
            t_encoding = chardet.detect(t.read())['encoding']
        with open(pathEn, "rb") as e:
            e_encoding = chardet.detect(e.read())['encoding']

        with open(pathTr, "r", encoding=t_encoding) as t, open(pathEn, "r", encoding=e_encoding) as e:
            
            # Read how many lines we have
            linesTr = t.readlines()
            linesEn = e.readlines()
            num_lines = len(linesTr)

            if(num_lines < rowCount):
                self.show_popup("Congragulations you finihed all the words")

            
            # We get the number of index numbers requested by the user, later will be read from the files.
            indexNumbers = sorted(random.sample(range(num_lines), rowCount))


            for i in range(len(indexNumbers)):
                turkishList.append(linesTr[indexNumbers[i]].strip())
                englishList.append(linesEn[indexNumbers[i]].strip())    
            
                # Deletes the used words from list in reverse order not to disturb the que
            for j in reversed(range(len(indexNumbers))):
                del linesTr[indexNumbers[j]]
                del linesEn[indexNumbers[j]]

        # writes the remaining lines back to the file
        with open(pathTr, "w", encoding="utf-8") as t, open(pathEn, "w", encoding="utf-8") as e:
            t.writelines(linesTr)
            e.writelines(linesEn)

        # Opens the words list
        self.openWindow(rowCount, englishList, turkishList)

    def show_popup(self,text):
        msg = QMessageBox.warning(self, "Error", text)

    def updateLabels(self):
         score = self.getScore() + int(self.ui.wordNumberComboBox.currentText())
         self.setScore(score)
         self.ui.learnedLabel.setText(f"Öğrenilen Kelime Sayısı: {score}")
         self.ui.leftLabel.setText(f"Öğrenilen Kelime Sayısı: {2650 - score}")
    

    def getScore(self):
        if os.path.exists('assets/score.txt'):
            with open('assets/score.txt', 'r') as f:
                self.score = int(f.read())
        else:
            self.score = 0
        return self.score


    def setScore(self,score):
        if os.path.exists('assets/score.txt'):
            with open('assets/score.txt', 'w') as f:
                f.write(str(score))
        else:
             raise RuntimeError


    def resetCounter(self):

        # Assign the paths for original files, later they will be fetched
        pathTr = os.path.join("assets", "originalTurkish.txt")
        pathEn = os.path.join("assets", "originalEnglish.txt")
        newPathTr = os.path.join("assets", "turkish.txt")
        newPathEn = os.path.join("assets", "english.txt")

        # We get the encoding types of the files to read and write flawlesly
        with open(pathTr, "rb") as t:
            t_encoding = chardet.detect(t.read())['encoding']
        with open(pathEn, "rb") as e:
            e_encoding = chardet.detect(e.read())['encoding']

        with open(pathTr, "r", encoding=t_encoding) as t, open(pathEn, "r", encoding=e_encoding) as e:
            contentsTr = t.read()
            contentsEn = e.read()
        with open(newPathTr, "w", encoding=t_encoding) as t, open(newPathEn, "w", encoding=e_encoding) as e:
            t.write(contentsTr)
            e.write(contentsEn)

        # Finally Resets the scoreBoard
        self.setScore(0)
        self.ui.learnedLabel.setText(f"Öğrenilen Kelime Sayısı: {self.getScore()}")
        self.ui.leftLabel.setText(f"Kalan Kelime Sayısı: {2650 - self.getScore()}")   


    def __init__(self, parent=None):
            QMainWindow.__init__(self)
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

            # Başlangıç için gerekli labelları ayarlar
            self.ui.learnedLabel.setText(f"Öğrenilen Kelime Sayısı: {self.getScore()}")
            self.ui.leftLabel.setText(f"Kalan Kelime Sayısı: {2650 - self.getScore()}")
           
            self.ui.resetButton.setIcon(QIcon(os.path.join("assets","reset.jpg")))
            self.ui.resetButton.setIconSize(QSize(50, 50))
            self.ui.resetButton.setToolTip("Sayacı ve Kelimeleri sıfırlar")

            # Buton event sonrası önce labelları günceller seçilen sayıya göre sonra da listeyi açar
            self.ui.generateButton.clicked.connect(lambda: (self.updateLabels(), self.generateWords()))         
            self.ui.resetButton.clicked.connect(lambda: self.resetCounter())
           
                        
            self.ui.learnedWidget.setStyleSheet("background-color: white; border: 2px solid black;",)
            self.ui.leftWidget.setStyleSheet("background-color: white; border: 2px solid black;",)
            self.ui.learnedLabel.setStyleSheet("border: None;")
            self.ui.leftLabel.setStyleSheet("border: None;")
            self.setStyleSheet("QComboBox QAbstractItemView { background-color: white; }")
            self.ui.Frame.setStyleSheet("background: #FA9D06;")


            self.ui.generateButtonWidget.setStyleSheet(            """
            background: white;
            border: 1px solid black;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
                """.format(20)
            )


            self.ui.generateFrame.setStyleSheet(            """
            background: #196FA1;
            border: 1px solid black;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(20)
            )


            self.ui.generateLineWidget.setStyleSheet(            """
            background: white;
            color: black;
            border: none;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(10)
            )


            self.ui.widget.setStyleSheet(            """
            background: white;
            color: black;
            border: none;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(10)
            )


            self.ui.generateButtonWidget.setStyleSheet(            """
            background: white;
            color: black;
            border: none;
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(10)
            )


            self.ui.wordNumberComboBox.setStyleSheet(            """
            background: white;
            border : 1px solid black;
            border-top-left-radius : 5px;
            border-top-right-radius : 5px;
            border-bottom-left-radius:5px;
            border-bottom-right-radius : 5px;
            """
            )
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Dictionary")
    window.setWindowIcon(QIcon(os.path.join("assets","Icon.ico")))
    window.show()
    sys.exit(app.exec_())

