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
from PySide6.QtWidgets import (QApplication, QDateEdit, QFormLayout, QGridLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QStatusBar, QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(475, 565)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 0, 471, 541))
        self.page_login = QWidget()
        self.page_login.setObjectName(u"page_login")
        self.verticalLayoutWidget = QWidget(self.page_login)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(60, 100, 351, 319))
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
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setContentsMargins(2, 0, -1, -1)
        self.le_email = QLineEdit(self.verticalLayoutWidget)
        self.le_email.setObjectName(u"le_email")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.le_email)

        self.l_password = QLabel(self.verticalLayoutWidget)
        self.l_password.setObjectName(u"l_password")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.l_password)

        self.le_password = QLineEdit(self.verticalLayoutWidget)
        self.le_password.setObjectName(u"le_password")
        self.le_password.setInputMethodHints(Qt.ImhHiddenText|Qt.ImhNoAutoUppercase|Qt.ImhNoPredictiveText|Qt.ImhSensitiveData)
        self.le_password.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.le_password)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout.setItem(3, QFormLayout.FieldRole, self.horizontalSpacer_2)

        self.l_totp = QLabel(self.verticalLayoutWidget)
        self.l_totp.setObjectName(u"l_totp")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.l_totp)

        self.le_totp = QLineEdit(self.verticalLayoutWidget)
        self.le_totp.setObjectName(u"le_totp")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.le_totp)

        self.b_login = QPushButton(self.verticalLayoutWidget)
        self.b_login.setObjectName(u"b_login")

        self.formLayout.setWidget(12, QFormLayout.LabelRole, self.b_login)

        self.l_email = QLabel(self.verticalLayoutWidget)
        self.l_email.setObjectName(u"l_email")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.l_email)

        self.l_email_error = QLabel(self.verticalLayoutWidget)
        self.l_email_error.setObjectName(u"l_email_error")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.l_email_error)

        self.l_totp_error = QLabel(self.verticalLayoutWidget)
        self.l_totp_error.setObjectName(u"l_totp_error")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.l_totp_error)


        self.verticalLayout.addLayout(self.formLayout)

        self.stackedWidget.addWidget(self.page_login)
        self.page_carwl_action = QWidget()
        self.page_carwl_action.setObjectName(u"page_carwl_action")
        self.gridLayoutWidget = QWidget(self.page_carwl_action)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 10, 431, 501))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.b_start = QPushButton(self.gridLayoutWidget)
        self.b_start.setObjectName(u"b_start")

        self.gridLayout_2.addWidget(self.b_start, 3, 2, 1, 1)

        self.l_start_date = QLabel(self.gridLayoutWidget)
        self.l_start_date.setObjectName(u"l_start_date")

        self.gridLayout_2.addWidget(self.l_start_date, 2, 1, 1, 1)

        self.pushButton_2 = QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout_2.addWidget(self.pushButton_2, 3, 1, 1, 1)

        self.b_logout = QPushButton(self.gridLayoutWidget)
        self.b_logout.setObjectName(u"b_logout")

        self.gridLayout_2.addWidget(self.b_logout, 3, 0, 1, 1)

        self.start_date = QDateEdit(self.gridLayoutWidget)
        self.start_date.setObjectName(u"start_date")

        self.gridLayout_2.addWidget(self.start_date, 2, 2, 1, 1)

        self.textBrowser = QTextBrowser(self.gridLayoutWidget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout_2.addWidget(self.textBrowser, 4, 0, 1, 3)

        self.stackedWidget.addWidget(self.page_carwl_action)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 475, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.HeadlineInputField.setText(QCoreApplication.translate("MainWindow", u"Amazon Anmeldedaten", None))
        self.le_email.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Geben sie ihre E-Mail ein", None))
        self.l_password.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
        self.le_password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Geben sie ihr Passwort ein", None))
        self.l_totp.setText(QCoreApplication.translate("MainWindow", u"2FA-Code:", None))
        self.le_totp.setPlaceholderText(QCoreApplication.translate("MainWindow", u"TOTP Code/2FA-Code", None))
        self.b_login.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.l_email.setText(QCoreApplication.translate("MainWindow", u"Email:", None))
        self.l_email_error.setText("")
        self.l_totp_error.setText("")
        self.b_start.setText(QCoreApplication.translate("MainWindow", u"Lade Daten", None))
        self.l_start_date.setText(QCoreApplication.translate("MainWindow", u"Startjahr", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.b_logout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
    # retranslateUi

