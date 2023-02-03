#Standard Lib
import sys
#import crypt
#Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QFileDialog


# UI files
from CreatePass import Create_Master_Password_UI
from Main_Window import Ui_MainWindow
from Master_Pass import Enter_Master_Pass_UI
from SavePass import Ui_Form

# Own files
from Password_Manager import entry, registry

#LOOKINGTO
#qfiledialgue

class PasswordManager:
    def __init__(self):

        self.fileName = 'MySecretPasswords.txt'

        self.Main_Window = QtWidgets.QMainWindow()
        self.Main_Window_UI = Ui_MainWindow()
        self.Main_Window_UI.setupUi(self.Main_Window)
        self.Create_Master_Pass = Create_Master_Password_UI()
        self.Enter_Master_Pass = Enter_Master_Pass_UI()
        self.data = registry()

        self.Main_Window_UI.SearchButton.clicked.connect(self.searchClicked)
        self.Main_Window_UI.SettingsButton.clicked.connect(self.searchClicked)
        self.Main_Window_UI.AddPassButton.clicked.connect(self.addPassClicked)
        self.Main_Window_UI.AddCategory.clicked.connect(self.addCategotyClicked)
        self.Main_Window_UI.DeleteCategory.clicked.connect(self.deleteCategoryClicked)
        self.Main_Window_UI.CategoriesWidget.itemSelectionChanged.connect(self.clickedCategory)
        self.Main_Window_UI.actionSave.triggered.connect(lambda: self.save())
        self.Main_Window_UI.actionSave_2.triggered.connect(lambda: self.saveAs())
        self.Main_Window_UI.actionOpen_file.triggered.connect(lambda: self.load())

        self.addPass = QtWidgets.QWidget()
        self.addPassUI = Ui_Form()
        self.addPassUI.setupUi(self.addPass)

        self.updateCategoriesList()
        self.Main_Window.show()

    def searchClicked(self):
        pass

    def settingsClicked(self):
        pass

    def addPassClicked(self):
        self.addPassUI.TagBox.clear()
        self.addPassUI.UserBox.clear()
        self.addPassUI.PasswordBox.clear()
        self.addPassUI.UrlBox.clear()
        self.addPass.show()
        self.addPassUI.ShowPassButton.toggled.connect(lambda: self.showPassword())
        self.addPassUI.pushButton.clicked.connect(self.savePassClicked)
        self.addPassUI.GenerateButton.clicked.connect(self.generatePasswordClicked)
        #print(self.data.register)

    def addCategotyClicked(self):
        tag = self.Main_Window_UI.AddCatagoryBox.text()
        if tag == '':
            pass
        else:
            self.data.addCategory(tag)
            self.updateCategoriesList()
    
    def deleteCategoryClicked(self):
        selectedCategory = self.Main_Window_UI.CategoriesWidget.currentRow()
        if selectedCategory > 0:
            self.data.deleteCategory(selectedCategory)
        self.updateCategoriesList()
         
    def updateCategoriesList(self):
        self.Main_Window_UI.CategoriesWidget.clear()
        counter = 0
        for i in self.data.register:
            self.Main_Window_UI.CategoriesWidget.addItem(self.data.register[counter][0])
            counter = counter + 1

    def savePassClicked(self):
        tag = self.addPassUI.TagBox.text()
        url = self.addPassUI.UrlBox.text()
        username = self.addPassUI.UserBox.text()
        password = self.addPassUI.PasswordBox.text()
        account = entry(url, username, password, tag)
        self.data.addToCategory(account)
        self.addPassUI.TagBox.clear()
        self.addPassUI.UserBox.clear()
        self.addPassUI.PasswordBox.clear()
        self.addPassUI.UrlBox.clear()
        self.addPass.close()

        counter = 0
        finalCount = 0
        for i in range(0, len(self.data.register) - 1):
            print(self.data.register[counter][0])
            if entry.tag == self.data.register[counter][0]:
                finalCount = counter
            counter = counter + 1
        
        self.setTreeDisplay(finalCount)

        #print(self.data.register[0])

    def clickedCategory(self):
        selectedCategory = self.Main_Window_UI.CategoriesWidget.currentRow()
        self.setTreeDisplay(selectedCategory)
        
    def showPassword(self):
        if  self.addPassUI.ShowPassButton.isChecked() == True:
            self.addPassUI.PasswordBox.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.addPassUI.PasswordBox.setEchoMode(QtWidgets.QLineEdit.Password)

    def generatePasswordClicked(self):
        password = self.data.generatePassword()
        self.addPassUI.PasswordBox.setText(password)

    def setTreeDisplay(self, val):
        self.Main_Window_UI.PasswordsWidget.clear()
        if val > (len(self.data.register) - 1):
            val = 0
        #print('val = ' + str(val))
        usernames = []
        Urls = []
        passwords = []
        tag = self.data.register[val][0]
        for i in range(1, len(self.data.register[val])):
            usernames.append(self.data.register[val][i].username)
            Urls.append(self.data.register[val][i].url)
            passwords.append(self.data.register[val][i].password)

        for i in range(len(usernames)):
            Item = QTreeWidgetItem(self.Main_Window_UI.PasswordsWidget)
            Item.setText(0, tag)
            Item.setText(1, Urls[i])
            Item.setText(2, usernames[i])
            Item.setText(3, passwords[i])

    # Saving and loading
    def saveAs(self):
        fileName = QFileDialog.getSaveFileName()[0]
        self.data.saveAs(fileName)

    def save(self):
        print('Saving')
        self.data.save()

    def load(self):
        print('Loading') # This is for trouble shooting
        fileName = QFileDialog.getOpenFileName()[0]
        print(fileName)
        self.data.load(fileName)
        self.updateCategoriesList()
        self.data.updateTaglist()
        self.setTreeDisplay(0)

app = QtWidgets.QApplication(sys.argv)
PM = PasswordManager()
sys.exit(app.exec_())