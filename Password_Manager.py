from dataclasses import dataclass
import string
import random
import pickle
import requests


@dataclass
class entry:
    url: str
    username: str
    password: str
    tag: str = 'General'

class registry:

    def __init__(self):
        self.register = []
        self.tagList = []
        self.addCategory('General')
 
    def addCategory(self, tag):
        if tag not in self.tagList:
            category = []
            category.append(tag)
            self.register.append(category)
            self.tagList.append(tag)

    def deleteCategory(self, val):
        if val != 0:
           self.register.pop(val)
           self.tagList.pop(val)

    def updateTaglist(self):
        tagList = []
        for i in range (len(self.register)):
            tagList.append(self.register[i][0])

    def addToCategory(self, entry):
        for i in range(0, len(self.register)):
            if self.register[i][0] == entry.tag:
                self.register[i].append(entry)
            else:
                pass

    def generatePassword(self):
        list = []
        list += string.ascii_letters
        list += string.punctuation
        list += string.digits
        password = random.choices(list, k = 12)
        passwordStr = ''
        for i in password:
            passwordStr += str(i)
        return passwordStr
            # Saving and loading

    def saveAs(self, fileName):       
        self.fileName = fileName       
        file = open(self.fileName, 'wb')
        data = pickle.dumps(self.register)
        file.write(data)
        file.close()

    def save(self):
        print('Saving') # This is for trouble shooting
        file = open(self.fileName, 'wb')
        data = pickle.dump(self.register)
        file.write(data)
        file.close()

    def load(self, fileName):
        print('Loading') # This is for trouble shooting
        if fileName != '':
            file = open(fileName, 'rb')
            data = pickle.loads(file.read())
            self.register = data
            file.close()

    def loadFromWeb(self, link):
        print('Loading') # This is for trouble shooting
        data = requests.get(link)
        data = data.content
        data = pickle.loads(data)
        self.register = data