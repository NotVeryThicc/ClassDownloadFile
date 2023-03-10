# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Save_Password1.ui'
#
# Created by: PyQt5 UI code generator 5.15.8
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(541, 388)
        Form.setMaximumSize(QtCore.QSize(800, 900))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.UrlBox = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.UrlBox.setFont(font)
        self.UrlBox.setObjectName("UrlBox")
        self.gridLayout.addWidget(self.UrlBox, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.PasswordBox = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PasswordBox.setFont(font)
        self.PasswordBox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordBox.setObjectName("PasswordBox")
        self.gridLayout.addWidget(self.PasswordBox, 3, 1, 1, 1)
        self.UserBox = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.UserBox.setFont(font)
        self.UserBox.setObjectName("UserBox")
        self.gridLayout.addWidget(self.UserBox, 2, 1, 1, 1)
        self.TagBox = QtWidgets.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.TagBox.setFont(font)
        self.TagBox.setText("")
        self.TagBox.setObjectName("TagBox")
        self.gridLayout.addWidget(self.TagBox, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.GenerateButton = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.GenerateButton.setFont(font)
        self.GenerateButton.setObjectName("GenerateButton")
        self.gridLayout.addWidget(self.GenerateButton, 4, 2, 1, 1)
        self.ShowPassButton = QtWidgets.QCheckBox(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ShowPassButton.setFont(font)
        self.ShowPassButton.setObjectName("ShowPassButton")
        self.gridLayout.addWidget(self.ShowPassButton, 3, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 5, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_6.setText(_translate("Form", "Password:"))
        self.UrlBox.setPlaceholderText(_translate("Form", "URL"))
        self.label_4.setText(_translate("Form", "URL:"))
        self.PasswordBox.setPlaceholderText(_translate("Form", "Password"))
        self.UserBox.setPlaceholderText(_translate("Form", "User Name"))
        self.TagBox.setPlaceholderText(_translate("Form", "Tag"))
        self.label_5.setText(_translate("Form", "User Name:"))
        self.GenerateButton.setText(_translate("Form", "Generate Password"))
        self.ShowPassButton.setText(_translate("Form", "Show password"))
        self.label_7.setText(_translate("Form", "Tag:"))
        self.pushButton.setText(_translate("Form", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
