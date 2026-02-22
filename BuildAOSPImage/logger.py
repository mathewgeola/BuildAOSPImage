from datetime import datetime

from PySide6.QtCore import QObject, Signal


class UILogger(QObject):
    log_signal = Signal(str, str)  # (text, color)

    def __init__(self, text_edit, log_file=None):
        super().__init__()
        self.text_edit = text_edit
        self.log_file = log_file

        self.log_signal.connect(self._append_log)

    def _log(self, level, msg, color):
        datetime_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_msg = f"{datetime_str} {level} [*] {msg}"

        self.log_signal.emit(full_msg, color)

        if self.log_file:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(full_msg + "\n")

    def info(self, msg):
        self._log("INFO", msg, "black")

    def debug(self, msg):
        self._log("DEBUG", msg, "gray")

    def warning(self, msg):
        self._log("WARNING", msg, "orange")

    def error(self, msg):
        self._log("ERROR", msg, "red")

    def _append_log(self, text, color):
        self.text_edit.append(f'<span style="color:{color};">{text}</span>')

        scrollbar = self.text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
