# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.factoryImageFilePathHorizontalLayout = QHBoxLayout()
        self.factoryImageFilePathHorizontalLayout.setObjectName(u"factoryImageFilePathHorizontalLayout")
        self.factoryImageFilePathLabel = QLabel(self.centralwidget)
        self.factoryImageFilePathLabel.setObjectName(u"factoryImageFilePathLabel")

        self.factoryImageFilePathHorizontalLayout.addWidget(self.factoryImageFilePathLabel)

        self.factoryImageFilePathLineEdit = QLineEdit(self.centralwidget)
        self.factoryImageFilePathLineEdit.setObjectName(u"factoryImageFilePathLineEdit")
        self.factoryImageFilePathLineEdit.setReadOnly(True)

        self.factoryImageFilePathHorizontalLayout.addWidget(self.factoryImageFilePathLineEdit)

        self.factoryImageFilePathPushButton = QPushButton(self.centralwidget)
        self.factoryImageFilePathPushButton.setObjectName(u"factoryImageFilePathPushButton")

        self.factoryImageFilePathHorizontalLayout.addWidget(self.factoryImageFilePathPushButton)


        self.verticalLayout.addLayout(self.factoryImageFilePathHorizontalLayout)

        self.aospBuildImgFilePathListHorizontalLayout = QHBoxLayout()
        self.aospBuildImgFilePathListHorizontalLayout.setObjectName(u"aospBuildImgFilePathListHorizontalLayout")
        self.aospBuildImgFilePathListLabel = QLabel(self.centralwidget)
        self.aospBuildImgFilePathListLabel.setObjectName(u"aospBuildImgFilePathListLabel")

        self.aospBuildImgFilePathListHorizontalLayout.addWidget(self.aospBuildImgFilePathListLabel)

        self.aospBuildImgFilePathListLineEdit = QLineEdit(self.centralwidget)
        self.aospBuildImgFilePathListLineEdit.setObjectName(u"aospBuildImgFilePathListLineEdit")
        self.aospBuildImgFilePathListLineEdit.setReadOnly(True)

        self.aospBuildImgFilePathListHorizontalLayout.addWidget(self.aospBuildImgFilePathListLineEdit)

        self.aospBuildImgFilePathListPushButton = QPushButton(self.centralwidget)
        self.aospBuildImgFilePathListPushButton.setObjectName(u"aospBuildImgFilePathListPushButton")

        self.aospBuildImgFilePathListHorizontalLayout.addWidget(self.aospBuildImgFilePathListPushButton)


        self.verticalLayout.addLayout(self.aospBuildImgFilePathListHorizontalLayout)

        self.logTextBrowser = QTextBrowser(self.centralwidget)
        self.logTextBrowser.setObjectName(u"logTextBrowser")

        self.verticalLayout.addWidget(self.logTextBrowser)

        self.buildPushButton = QPushButton(self.centralwidget)
        self.buildPushButton.setObjectName(u"buildPushButton")

        self.verticalLayout.addWidget(self.buildPushButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Build AOSP Image", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.factoryImageFilePathLabel.setText(QCoreApplication.translate("MainWindow", u"factoryImageFilePath: ", None))
        self.factoryImageFilePathPushButton.setText(QCoreApplication.translate("MainWindow", u"choose", None))
        self.aospBuildImgFilePathListLabel.setText(QCoreApplication.translate("MainWindow", u"aospBuildImgFilePathList: ", None))
        self.aospBuildImgFilePathListPushButton.setText(QCoreApplication.translate("MainWindow", u"choose", None))
        self.buildPushButton.setText(QCoreApplication.translate("MainWindow", u"build", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

