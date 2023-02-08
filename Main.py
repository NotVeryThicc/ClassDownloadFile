#Standard Lib
import sys
import pickle
import requests
import pyperclip

#Qt
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QFileDialog
from PyQt5.QtCore import Qt

# UI files
from CreatePass import Ui_Main_Pass_UI
from Main_Window import Ui_MainWindow
from MasterPass import Ui_Enter_Master_Pass
from SavePass import Ui_Form
from Download_File import Ui_DownloadFile_UI

# Own files
from Password_Manager import entry, registry

#Encryption
import encryptionU

class PasswordManager:
    def __init__(self):
        self.fileName = ''
        self.data = registry()

        #Setting Up UI
        self.Main_Window = QtWidgets.QMainWindow()
        self.Main_Window_UI = Ui_MainWindow()
        self.Main_Window_UI.setupUi(self.Main_Window)
        self.Create_Master_Pass = Ui_Main_Pass_UI()
        self.Enter_Master_Pass = Ui_Enter_Master_Pass()
        self.DownloadFile = QtWidgets.QMainWindow()
        self.DownloadFile_UI = Ui_DownloadFile_UI()
        self.DownloadFile_UI.setupUi(self.DownloadFile)
        self.addPass = QtWidgets.QWidget()
        self.addPassUI = Ui_Form()
        self.editPassword = QtWidgets.QWidget()
        self.editPasswordUI = Ui_Form()

        #Save Passwords Buttons
        self.addPassUI.setupUi(self.addPass)
        self.addPassUI.ShowPassButton.toggled.connect(lambda: self.showPassword())
        self.addPassUI.AddButton.clicked.connect(self.savePassClicked)
        self.addPassUI.GenerateButton.clicked.connect(self.generatePasswordClicked)
        self.addPassUI.CancelButton.clicked.connect(self.addPassCancelled)

        #Edit Password Buttons
        self.editPasswordUI.setupUi(self.editPassword)
        self.editPasswordUI.ShowPassButton.toggled.connect(lambda: self.showPassword())
        self.editPasswordUI.AddButton.clicked.connect(self.saveEditedPassClicked)
        self.editPasswordUI.GenerateButton.clicked.connect(self.generatePasswordClickedEdit)
        self.editPasswordUI.CancelButton.clicked.connect(self.editPassCancelled)
        
        #Main UI buttons
        self.Main_Window_UI.SearchButton.clicked.connect(self.searchClicked)
        self.Main_Window_UI.SettingsButton.clicked.connect(self.settingsClicked)
        self.Main_Window_UI.AddPassButton.clicked.connect(self.addPassClicked)
        self.Main_Window_UI.AddCategory.clicked.connect(self.addCategotyClicked)
        self.Main_Window_UI.DeleteCategory.clicked.connect(self.deleteCategoryClicked)
        self.Main_Window_UI.DeletePassword.clicked.connect(self.deleteAccountClicked)
        self.Main_Window_UI.SearchButton.clicked.connect(self.searchClicked)
        self.Main_Window_UI.SearchBox.textChanged.connect(self.searchClicked)
        self.Main_Window_UI.CategoriesWidget.itemSelectionChanged.connect(self.clickedCategory)
        self.Main_Window_UI.PasswordsWidget.itemSelectionChanged.connect(self.clickedPassword)

        #Action Buttons
        self.Main_Window_UI.actionSave.triggered.connect(lambda: self.save())
        self.Main_Window_UI.actionSave_2.triggered.connect(lambda: self.saveAs())
        self.Main_Window_UI.actionOpen_file.triggered.connect(lambda: self.load())
        self.Main_Window_UI.actionDownload_File.triggered.connect(lambda: self.loadFromWebClicked())
        
        #Download online Button
        self.DownloadFile_UI.EnterButton.clicked.connect(self.loadFromWeb)

        #Default values
        self.clickedAccPass = ''
        self.clickedAccUrl = ''
        self.clickedAccUser = ''
        self.clickedAccTag = ''
        self.selectedCategory = 0
        self.stay = 1

        self.editPasswordUI.TagBox.setReadOnly(True)
        self.updateCategoriesList()
        self.createContextMenu()
        self.Main_Window.show()

    def createContextMenu(self):
        self.Main_Window_UI.PasswordsWidget.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.copy_Password = QtWidgets.QAction("Copy", self.Main_Window_UI.PasswordsWidget)
        self.Main_Window_UI.PasswordsWidget.addAction(self.copy_Password)
        self.copy_Password.triggered.connect(lambda: self.copyPass())

        self.edit_Password = QtWidgets.QAction("Edit", self.Main_Window_UI.PasswordsWidget)
        self.Main_Window_UI.PasswordsWidget.addAction(self.edit_Password)
        self.edit_Password.triggered.connect(lambda: self.editPassClicked())

    def searchClicked(self):
        searchTerm = self.Main_Window_UI.SearchBox.text()
        self.Main_Window_UI.PasswordsWidget.clear()
        searchResult = []

        # Getting seach results
        for catagory in self.data.register:
            for account in range(1, len(catagory)):
                if searchTerm in catagory[account].url or searchTerm in catagory[account].username or searchTerm in catagory[account].password:
                    searchResult.append(catagory[account])

        #Displaying seach results
        for i in range(len(searchResult)):
            Item = QTreeWidgetItem(self.Main_Window_UI.PasswordsWidget)
            Item.setText(0, searchResult[i].tag)
            Item.setText(1, searchResult[i].url)
            Item.setText(2, searchResult[i].username)
            Item.setText(3, searchResult[i].password)
            

    def settingsClicked(self):
        pass

    def addPassClicked(self):
        self.addPassUI.TagBox.clear()
        self.addPassUI.UserBox.clear()
        self.addPassUI.PasswordBox.clear()
        self.addPassUI.UrlBox.clear()
        self.addPass.show()
        #print(self.data.register)

    def addPassCancelled(self):
        self.addPassUI.TagBox.clear()
        self.addPassUI.UserBox.clear()
        self.addPassUI.PasswordBox.clear()
        self.addPassUI.UrlBox.clear()
        self.addPass.close()

    def editPassClicked(self):
        self.editPasswordUI.TagBox.setText(self.clickedAccTag)
        self.editPasswordUI.UserBox.setText(self.clickedAccUser)
        self.editPasswordUI.PasswordBox.setText(self.clickedAccPass)
        self.editPasswordUI.UrlBox.setText(self.clickedAccUrl)
        self.editPassword.show()

    def editPassCancelled(self):
        self.editPasswordUI.TagBox.clear()
        self.editPasswordUI.UserBox.clear()
        self.editPasswordUI.PasswordBox.clear()
        self.editPasswordUI.UrlBox.clear()
        self.editPasssword.close()

    def saveEditedPassClicked(self):
        tag = self.editPasswordUI.TagBox.text()
        url = self.editPasswordUI.UrlBox.text()
        username = self.editPasswordUI.UserBox.text()
        password = self.editPasswordUI.PasswordBox.text()
        account = entry(url, username, password, tag)
        self.data.editAccount(self.clickedAccTag, self.clickedAccUser, self.clickedAccPass, self.clickedAccUrl, account)
        self.editPasswordUI.TagBox.clear()
        self.editPasswordUI.UserBox.clear()
        self.editPasswordUI.PasswordBox.clear()
        self.editPasswordUI.UrlBox.clear()
        if self.stay == 0:
            self.addPass.close()

        counter = 0
        finalCount = 0
        for i in range(0, len(self.data.register) - 1):
            #print(self.data.register[counter][0])
            if entry.tag == self.data.register[counter][0]:
                finalCount = counter
            counter = counter + 1

        self.setTreeDisplay(finalCount)

    def addCategotyClicked(self):
        tag = self.Main_Window_UI.AddCatagoryBox.text()
        if tag == '':
            self.setStatusBar('Enter a catagory tag!')
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
        if self.stay == 0:
            self.addPass.close()

        counter = 0
        finalCount = 0
        for i in range(0, len(self.data.register) - 1):
            #print(self.data.register[counter][0])
            if entry.tag == self.data.register[counter][0]:
                finalCount = counter
            counter = counter + 1

        self.setTreeDisplay(finalCount)
        #print(self.data.register[0])

    def clickedCategory(self):
        self.selectedCategory = self.Main_Window_UI.CategoriesWidget.currentRow()
        self.setTreeDisplay(self.selectedCategory)
        
    def showPassword(self):
        if  self.addPassUI.ShowPassButton.isChecked() == True:
            self.addPassUI.PasswordBox.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.addPassUI.PasswordBox.setEchoMode(QtWidgets.QLineEdit.Password)
        if  self.editPasswordUI.ShowPassButton.isChecked() == True:
            self.editPasswordUI.PasswordBox.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.editPasswordUI.PasswordBox.setEchoMode(QtWidgets.QLineEdit.Password)        

    def stayOnform(self):
        if self.addPassUI.StayOnForm.isChecked() == True:
            self.stay = 1
        else:
            self.stay = 0

    def generatePasswordClicked(self):
        password = self.data.generatePassword()
        self.addPassUI.PasswordBox.setText(password)

    def generatePasswordClickedEdit(self):
        password = self.data.generatePassword()
        self.editPassword.PasswordBox.setText(password)

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

    def clickedPassword(self):
        self.clickedAccTag = self.Main_Window_UI.PasswordsWidget.currentItem().text(0)
        self.clickedAccUrl = self.Main_Window_UI.PasswordsWidget.currentItem().text(1)
        self.clickedAccUser = self.Main_Window_UI.PasswordsWidget.currentItem().text(2)
        self.clickedAccPass = self.Main_Window_UI.PasswordsWidget.currentItem().text(3)
        #print(self.clickedAccUrl)

    def deleteAccountClicked(self): 
        self.data.delFromCategory(self.selectedCategory, self.clickedAccUrl, self.clickedAccUser, self.clickedAccPass)
        self.setTreeDisplay(self.selectedCategory)

    def copyPass(self):
        print("clicked copy")
        self.setStatusBar("Copied Password")
        clickedPass = self.clickedAccPass
        pyperclip.copy(clickedPass)

    # Saving and loading
    #######################################################################################################################
    def saveAs(self):
        print('Saving')
        self.setStatusBar('Saving')

        fileName = QFileDialog.getSaveFileName()[0]
        if fileName != '':
            self.data.fileName = fileName
            file = open(fileName, "wb")
            data = pickle.dumps(self.data)
            #Encrypt


            #Write
            file.write(data)
            file.close
        else:
            self.setStatusBar("Please Choose a file")

    def save(self):
        print('Saving')
        self.setStatusBar('Saving')
        if self.fileName == '':
            self.saveAs()
            pass

        file = open(self.fileName, "wb")
        data = data = pickle.dumps(self.data)
        #Encrypt

        #Write
        file.write(data)
        file.close

    def load(self):
        print('Loading') # This is for trouble shooting
        self.setStatusBar('Loading')

        fileName = QFileDialog.getOpenFileName()[0]
        if fileName != '':
            file = open(fileName, 'rb')
            data = pickle.loads(file.read())
            #Decrypt

            self.data = data
            
            file.close()

            self.fileName = fileName
            self.updateCategoriesList()
            self.data.updateTaglist()
            self.setTreeDisplay(0)
            self.selectedCategory = 0
        else:
            self.setStatusBar("Please Chose a file")

    def loadFromWebClicked(self):
        #https://www.dropbox.com/s/qfh5tajh9d55ab5/Secret.txt?dl=1
        self.setStatusBar('Loading from Web')
        self.DownloadFile.show()
        
    def loadFromWeb(self):
        link = self.DownloadFile_UI.LinkBox.text()
        if link == '':
            self.setStatusBar('Error Loading File!')
            return 0
        data = requests.get(link)
        data = data.content
        self.DownloadFile.close()
        #Decrypt

        data = pickle.loads(data)
        self.data = data
        self.updateCategoriesList()
        self.data.updateTaglist()
        self.setTreeDisplay(0)
        self.selectedCategory = 0

    def encrypt(self, data):
        #f = Fernet(self.data.MasterPassword + self.salt)
        pass

    def decrypt(self, encryptedData):
        pass

    def setStatusBar(self, text):
        self.Main_Window_UI.StatusBarLabel.setText(text)
        #QtTest.QTest.qWait(2000)
        #self.Main_Window_UI.StatusBarLabel.clear()

    def getMasterPassword(self):
        #get pass from UI form
        #if first login ask to create one instead
        #self.data.MasterPassword = password
        pass

app = QtWidgets.QApplication(sys.argv)
PM = PasswordManager()
sys.exit(app.exec_())