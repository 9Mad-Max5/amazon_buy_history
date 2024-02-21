# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_interface_new.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(474, 568)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(60, 100, 351, 311))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.HeadlineInputField = QLabel(self.verticalLayoutWidget)
        self.HeadlineInputField.setObjectName(u"HeadlineInputField")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(12)
        font.setBold(True)
        self.HeadlineInputField.setFont(font)
        self.HeadlineInputField.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.HeadlineInputField)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.formLayout.setContentsMargins(2, 0, -1, -1)
        self.emailLabel = QLabel(self.verticalLayoutWidget)
        self.emailLabel.setObjectName(u"emailLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.emailLabel)

        self.emailLineEdit = QLineEdit(self.verticalLayoutWidget)
        self.emailLineEdit.setObjectName(u"emailLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.emailLineEdit)

        self.passwordLabel = QLabel(self.verticalLayoutWidget)
        self.passwordLabel.setObjectName(u"passwordLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.passwordLabel)

        self.passwordLineEdit = QLineEdit(self.verticalLayoutWidget)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setInputMethodHints(Qt.ImhHiddenText)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.passwordLineEdit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout.setItem(2, QFormLayout.FieldRole, self.horizontalSpacer_2)

        self.totpLabel = QLabel(self.verticalLayoutWidget)
        self.totpLabel.setObjectName(u"totpLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.totpLabel)

        self.totpLineEdit = QLineEdit(self.verticalLayoutWidget)
        self.totpLineEdit.setObjectName(u"totpLineEdit")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.totpLineEdit)

        self.loginButton = QPushButton(self.verticalLayoutWidget)
        self.loginButton.setObjectName(u"loginButton")

        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.loginButton)


        self.verticalLayout.addLayout(self.formLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 474, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.HeadlineInputField.setText(QCoreApplication.translate("MainWindow", u"Amazon Anmeldedaten", None))
        self.emailLabel.setText(QCoreApplication.translate("MainWindow", u"Email:", None))
        self.emailLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Geben sie ihre E-Mail ein", None))
        self.passwordLabel.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
        self.passwordLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Geben sie ihr Passwort ein", None))
        self.totpLabel.setText(QCoreApplication.translate("MainWindow", u"2FA-Code:", None))
        self.totpLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"TOTP Code/2FA-Code", None))
        self.loginButton.setText(QCoreApplication.translate("MainWindow", u"Login", None))
    # retranslateUi

