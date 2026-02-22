import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog

from ui_mainwindow import Ui_MainWindow
from logger import UILogger


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.logger = UILogger(self._ui.logTextBrowser, log_file="app.log")

        self._ui.factoryImageFilePathPushButton.clicked.connect(self.choose_factory_image_file_path)
        self._ui.aospBuildImgFilePathListPushButton.clicked.connect(self.choose_aosp_build_img_file_path_list)
        self._ui.buildPushButton.clicked.connect(self.build_aosp_image)

    def choose_factory_image_file_path(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Factory Image File Path",
            "",
            "Factory Image File Path (*.zip)"
        )

        if file_path:
            self._ui.factoryImageFilePathLineEdit.setText(file_path)

    def choose_aosp_build_img_file_path_list(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Choose AOSP Build Img File Path List",
            "",
            "AOSP Build Img File Path List (*.img)"
        )

        if file_paths:
            result = ";".join(file_paths)
            self._ui.aospBuildImgFilePathListLineEdit.setText(result)

    def build_aosp_image(self):
        self.logger.debug("Building AOSP image")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
