from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit
from PyQt6.QtGui import QFont



class InputText(QWidget):

    def __init__(self, window, label, x, y):
        super().__init__()

        self.window = window
        self.able = True

        self.label = QLabel(label, window)
        self.label.move(x, y)
        self.label.setFont(QFont('Arial', 20))

        self.info = QLabel("", window)
        self.info.resize(240, 20)
        self.info.move(x + 80, y - 24)
        self.info.setFont(QFont('Arial', 12))

        self.box = QLineEdit(window)
        self.box.move(x + 80, y - 5)
        self.box.resize(240, 40)
        self.box.setFont(QFont('Arial', 20))
        self.box.textChanged.connect(self.verify)

    def verify(self):
        pass

class CodeInput(InputText):

    def __init__(self, window, x, y):
        super().__init__(window, 'Code:', x, y)

    def verify(self, code):
        if len(code) == 0:
            self.info.setText("")
            self.able = False
            return None
        for c in code[0:3]:
            if not c.isalpha() or not c.isupper():
                self.info.setText("First 3 characters must be uppercase letters")
                self.able = False
                return None
        for c in code[3:]:
            if not c.isdigit():
                self.info.setText("Last 4 characters must be numbers")
                self.able = False
                return None
        if len(code) != 7:
            self.info.setText("Code must have 7 characters")
            self.able = False
            return None
        self.info.clear()
        self.able = True
        return None

class NaInput(InputText):

    def __init__(self, window, x, y):
        super().__init__(window, 'RUT:', x, y)

        self.box.returnPressed.connect(self.parse_na)

    def parse_na(self):
        na = self.box.text()
        if len(na) == 120:
            self.box.setText(na.split("¿")[1].split("/")[0].replace("'", ""))
        print(self.box.text())

    def verify(self, na):
        if len(na) == 0:
            self.info.clear()
            self.able = False
        elif "-" in na:
            self.info.setText("RUT must not have '-'")
            self.able = False
        elif len(na) >= 9:
            self.info.clear()
            self.able = True
        else:
            self.info.setText("RUT must have least 8 characters")
            self.able = False

