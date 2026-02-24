import datetime
import html
import os
import shutil
import subprocess
import sys
import zipfile

from PySide6.QtCore import QObject, QThread, Signal, QUrl
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextBrowser

from ui_mainwindow import Ui_MainWindow


class Logger(QObject):
    log_signal = Signal(str, str, bool)

    def __init__(self, text_browser: QTextBrowser, log_file_path: str = None):
        super().__init__()
        self.text_browser = text_browser
        self.log_file_path = log_file_path

        app = QApplication.instance()
        if app:
            app.aboutToQuit.connect(self.close)

        self.log_signal.connect(self._handle_log_signal)

        self.text_browser.setOpenExternalLinks(False)
        self.text_browser.setOpenLinks(False)
        self.text_browser.anchorClicked.connect(self._handle_anchorClicked)

        if self.log_file_path:
            self._file = open(self.log_file_path, "a", encoding="utf-8")
        else:
            self._file = None

    def _handle_log_signal(self, text, color, is_html):
        if not is_html:
            safe_text = html.escape(text)
        else:
            safe_text = text
        html_text = f'<span style="color:{color};">{safe_text}</span>'

        self.text_browser.append(html_text)
        self.text_browser.moveCursor(QTextCursor.End)

    @staticmethod
    def _handle_anchorClicked(url: QUrl):  # noqa
        if not url or not url.isValid():
            return

        path = url.toLocalFile()
        if not path:
            return

        path = os.path.normpath(path)

        if not os.path.exists(path):
            return

        if sys.platform.startswith("win"):
            if os.path.isfile(path):
                subprocess.Popen(
                    ["explorer", "/select,", path],
                    shell=False
                )
            else:
                subprocess.Popen(
                    ["explorer", path],
                    shell=False
                )

        elif sys.platform == "darwin":
            if os.path.isfile(path):
                subprocess.Popen(["open", "-R", path])
            else:
                subprocess.Popen(["open", path])

        else:
            if os.path.isfile(path):
                folder = os.path.dirname(path)
                subprocess.Popen(["xdg-open", folder])
            else:
                subprocess.Popen(["xdg-open", path])

    def _log(self, level, msg, color, is_html=False):
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_msg = f"{datetime_str} {level} [*] {msg}"

        self.log_signal.emit(full_msg, color, is_html)

        if self._file:
            self._file.write(full_msg + "\n")
            self._file.flush()

    def debug(self, msg: str, is_html: bool = False) -> None:
        self._log("DEBUG", msg, "gray", is_html)

    def info(self, msg: str, is_html: bool = False) -> None:
        self._log("INFO", msg, "black", is_html)

    def success(self, msg: str, is_html: bool = False) -> None:
        self._log("SUCCESS", msg, "green", is_html)

    def warning(self, msg: str, is_html: bool = False) -> None:
        self._log("WARNING", msg, "orange", is_html)

    def error(self, msg: str, is_html: bool = False) -> None:
        self._log("ERROR", msg, "red", is_html)

    def close(self) -> None:
        if self._file and not self._file.closed:
            self._file.flush()
            self._file.close()


class Worker(QObject):
    finished = Signal()

    def __init__(self, main_window: "MainWindow"):
        super().__init__()
        self.main_window = main_window

    def _zip(self, unzip_dir_path: str, zip_file_path: str) -> None:
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)
            self.main_window.logger.info(f"remove {zip_file_path!r}")

        self.main_window.logger.debug(f"start zip {unzip_dir_path!r}")
        with zipfile.ZipFile(zip_file_path, "w", compression=zipfile.ZIP_STORED) as zf:
            for root, dirs, files in os.walk(unzip_dir_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    arc_name = os.path.relpath(full_path, unzip_dir_path)
                    zf.write(full_path, arc_name)
        self.main_window.logger.debug(f"finish zip {zip_file_path!r}")

    def _unzip(self, zip_file_path: str, unzip_dir_path: str) -> None:
        if os.path.exists(unzip_dir_path):
            shutil.rmtree(unzip_dir_path)
            self.main_window.logger.info(f"rmtree {unzip_dir_path!r}")

        os.makedirs(unzip_dir_path, exist_ok=True)
        self.main_window.logger.info(f"makedirs {unzip_dir_path!r}")

        self.main_window.logger.debug(f"start unzip {zip_file_path!r}")
        with zipfile.ZipFile(zip_file_path, "r", compression=zipfile.ZIP_STORED) as zf:
            zf.extractall(unzip_dir_path)
        self.main_window.logger.debug(f"finish unzip {unzip_dir_path!r}")

    def run(self):
        try:
            self.main_window.logger.debug("start build aosp image")

            factory_image_file_path = self.main_window.ui.factoryImageFilePathLineEdit.text()
            aosp_build_img_file_path_list = self.main_window.ui.aospBuildImgFilePathListLineEdit.text().split(";")

            prefix, suffix = os.path.splitext(os.path.basename(factory_image_file_path))
            aosp_image_file_path = os.path.join(
                self.main_window.dir_path,
                prefix + "_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + suffix
            )
            factory_image_unzip_dir_path = os.path.join(
                self.main_window.dir_path,
                prefix
            )
            self._unzip(factory_image_file_path, factory_image_unzip_dir_path)

            if len(lst := os.listdir(factory_image_unzip_dir_path)) != 1:
                self.main_window.logger.error(f"illegal {factory_image_unzip_dir_path!r}")
                return

            inner_dir_path = os.path.join(factory_image_unzip_dir_path, lst[0])
            lst: list[str] = list(
                filter(lambda x: os.path.splitext(x)[-1] == ".zip",
                       map(lambda x: os.path.join(inner_dir_path, x), os.listdir(inner_dir_path)))
            )
            if len(lst) != 1:
                self.main_window.logger.error(f"illegal {inner_dir_path!r}")
                return
            inner_zip_file_path = lst[0]

            inner_zip_unzip_dir_path = os.path.join(
                os.path.dirname(inner_zip_file_path), os.path.splitext(inner_zip_file_path)[0]
            )
            self._unzip(inner_zip_file_path, inner_zip_unzip_dir_path)

            for aosp_build_img_file_path in aosp_build_img_file_path_list:
                shutil.copy2(aosp_build_img_file_path, inner_zip_unzip_dir_path)
                self.main_window.logger.info(f"copy {aosp_build_img_file_path!r} ==> {inner_zip_unzip_dir_path!r}")

            self._zip(inner_zip_unzip_dir_path, inner_zip_file_path)

            shutil.rmtree(inner_zip_unzip_dir_path)
            self.main_window.logger.info(f"rmtree {inner_zip_unzip_dir_path!r}")

            self._zip(factory_image_unzip_dir_path, aosp_image_file_path)

            shutil.rmtree(factory_image_unzip_dir_path)
            self.main_window.logger.info(f"remove {factory_image_unzip_dir_path!r}")

            path = aosp_image_file_path
            url = QUrl.fromLocalFile(path).toString()
            self.main_window.logger.success(f'''<a href="{url}">{path}</a>''', is_html=True)

        except Exception as e:
            self.main_window.logger.error(f"exception: {e}")

        finally:
            self.main_window.logger.debug("finish build aosp image")

            self.finished.emit()
            self.main_window.ui.factoryImageFilePathPushButton.setEnabled(True)
            self.main_window.ui.aospBuildImgFilePathListPushButton.setEnabled(True)
            self.main_window.ui.buildPushButton.setEnabled(True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.dir_path: str = os.path.dirname(os.path.abspath(__file__))

        self.logger = Logger(self._ui.logTextBrowser, log_file_path="app.log")

        self._threads = []

        self._ui.factoryImageFilePathPushButton.clicked.connect(self.on_factoryImageFilePathPushButton_clicked)
        self._ui.aospBuildImgFilePathListPushButton.clicked.connect(self.on_aospBuildImgFilePathListPushButton_clicked)
        self._ui.buildPushButton.clicked.connect(self.on_buildPushButton_clicked)

    @property
    def ui(self):
        return self._ui

    def on_factoryImageFilePathPushButton_clicked(self):  # noqa
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Factory Image File Path",
            "",
            "Factory Image File Path (*.zip)"
        )

        if file_path:
            self._ui.factoryImageFilePathLineEdit.setText(file_path)

    def on_aospBuildImgFilePathListPushButton_clicked(self):  # noqa
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Choose AOSP Build Img File Path List",
            "",
            "AOSP Build Img File Path List (*.img)"
        )

        if file_paths:
            result = ";".join(file_paths)
            self._ui.aospBuildImgFilePathListLineEdit.setText(result)

    def on_buildPushButton_clicked(self):  # noqa
        self._ui.factoryImageFilePathPushButton.setEnabled(False)
        self._ui.aospBuildImgFilePathListPushButton.setEnabled(False)
        self._ui.buildPushButton.setEnabled(False)

        thread = QThread()
        worker = Worker(self)

        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        thread.finished.connect(thread.deleteLater)
        worker.finished.connect(worker.deleteLater)

        self._threads.append((thread, worker))
        thread.finished.connect(lambda: self._threads.remove((thread, worker)))

        thread.start()


if __name__ == '__main__':
    def main():
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())


    main()
