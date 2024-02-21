# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_interface.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_LoginForm(object):
    def setupUi(self, LoginForm):
        if not LoginForm.objectName():
            LoginForm.setObjectName(u"LoginForm")
        LoginForm.resize(400, 200)
        self.verticalLayout = QVBoxLayout(LoginForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(LoginForm)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.emailLineEdit = QLineEdit(LoginForm)
        self.emailLineEdit.setObjectName(u"emailLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.emailLineEdit)

        self.label_2 = QLabel(LoginForm)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.passwordLineEdit = QLineEdit(LoginForm)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setInputMethodHints(Qt.ImhHiddenText)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.passwordLineEdit)

        self.totpLineEdit = QLineEdit(LoginForm)
        self.totpLineEdit.setObjectName(u"totpLineEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.totpLineEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout.setItem(3, QFormLayout.SpanningRole, self.horizontalSpacer)

        self.loginButton = QPushButton(LoginForm)
        self.loginButton.setObjectName(u"loginButton")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.loginButton)


        self.verticalLayout.addLayout(self.formLayout)


        self.retranslateUi(LoginForm)

        QMetaObject.connectSlotsByName(LoginForm)
    # setupUi

    def retranslateUi(self, LoginForm):
        LoginForm.setWindowTitle(QCoreApplication.translate("LoginForm", u"Login Form", None))
        self.label.setText(QCoreApplication.translate("LoginForm", u"Email:", None))
        self.label_2.setText(QCoreApplication.translate("LoginForm", u"Password:", None))
        self.loginButton.setText(QCoreApplication.translate("LoginForm", u"Login", None))
    # retranslateUi

