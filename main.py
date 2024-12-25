from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
import requests
import datetime
import sys
from env import DATABASE_ID, HEADERS
from utils import get_debt, calculate_fee, debt_format, pay_format
from params import WINDOW_POSITION, WINDOW_SIZE, BUTTON_POSITION, BUTTON_SIZE
from datetime import datetime, timedelta, datetime, timezone
fromisoformat = datetime.fromisoformat
now_time = lambda : datetime.now(timezone.utc)
from src.input import CodeInput, NaInput


class Ventana(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('logo/Logo_CAi.png'))
        self.setWindowTitle('Prestamos - BanCAi')
        self.setGeometry(*WINDOW_POSITION, *WINDOW_SIZE)
        self.load_gui()
        self.show()

    def load_gui(self):
        self.load_main_view()
        self.load_info_view()
        self.load_payment_view()

        self.main_view.show()
        # self.payment_view.show()

    def load_main_view(self):

        self.main_view = QWidget(self)
        self.main_view.setGeometry(0, 0, *WINDOW_SIZE)

        self.code = CodeInput(self.main_view, 20, 25)
        self.na   = NaInput(self.main_view, 20, 100)

        self.label_main = QLabel("", self.main_view)
        self.label_main.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.label_main.move(20, 150)
        self.label_main.resize(360, 200)
        self.label_main.setFont(QFont('Arial', 12))

        self.button_send = QPushButton('SEND', self.main_view)
        self.button_send.move(*BUTTON_POSITION)
        self.button_send.resize(*BUTTON_SIZE)
        self.button_send.setFont(QFont('Arial', 20))
        self.button_send.setEnabled(False)

        self.code.box.textChanged.connect(self.able_send_button)
        self.code.box.returnPressed.connect(self.na.box.setFocus)
        self.na.box.textChanged.connect(self.able_send_button)
        self.na.box.returnPressed.connect(self.button_send.click)
        self.button_send.clicked.connect(self.analize)

        self.main_view.hide()

    def load_info_view(self):

        self.info_view = QWidget(self)
        self.info_view.setGeometry(0, 0, *WINDOW_SIZE)

        self.label_info = QLabel("", self.info_view)
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.label_info.move(20, 25)
        self.label_info.resize(360, 200)
        self.label_info.setFont(QFont('Arial', 12))

        self.button_back = QPushButton('Back', self.info_view)
        self.button_back.move(*BUTTON_POSITION)
        self.button_back.resize(*BUTTON_SIZE)
        self.button_back.setFont(QFont('Arial', 20))
        self.button_back.clicked.connect(lambda: self.show_main_view())

        self.info_view.hide()

    def load_payment_view(self):

        self.payment_view = QWidget(self)
        self.payment_view.setGeometry(0, 0, *WINDOW_SIZE)

        self.label_payment = QLabel("", self.payment_view)
        self.label_payment.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.label_payment.move(0, 0)
        self.label_payment.resize(360, 200)
        self.label_payment.margin = 20
        self.label_payment.setFont(QFont('Arial', 18))

        self.button_pay = QPushButton('Pay', self.payment_view)
        self.button_pay.move(*[60, 200])
        self.button_pay.resize(*BUTTON_SIZE)
        self.button_pay.setFont(QFont('Arial', 20))
        self.button_pay.clicked.connect(lambda: self.pay_debt())

        self.button_back_pay = QPushButton('Back', self.payment_view)
        self.button_back_pay.move(*BUTTON_POSITION)
        self.button_back_pay.resize(*BUTTON_SIZE)
        self.button_back_pay.setFont(QFont('Arial', 20))
        self.button_back_pay.clicked.connect(lambda: self.show_main_view())

        self.payment_view.hide()

    def pay_debt(self):
        self.update_date(self.debt_info["id"], now_time(), f"Cobro: {self.debt_info['fee']}")
        self.show_main_view("Cobro exitoso")


    def show_payment_view(self, data):
        self.main_view.hide()
        self.info_view.hide()

        self.label_payment.setText(str(data))
        self.payment_view.show()

    def show_info_view(self, data):
        self.main_view.hide()
        self.payment_view.hide()

        self.label_info.setText(str(data))
        self.info_view.show()


    def show_main_view(self, data:str=""):
        self.info_view.hide()
        self.payment_view.hide()

        self.na.box.clear()
        self.code.box.clear()
        self.code.box.setFocus()
        self.label_main.setText(str(data))

        self.main_view.show()


    def able_send_button(self):
        if self.na.able and self.code.able:
            self.button_send.setEnabled(True)
        else:
            self.button_send.setEnabled(False)
        self.label_main.setText("")
        self.button_send.setText("SEND")


    def publish_new_debt(self, ID, PERSON, NOW):
        url = "https://api.notion.com/v1/pages"

        data_ = {
            "parent": {
                "database_id": DATABASE_ID
            },
            "properties": {
                "Codigo"    : {"title": [{"text": {"content": ID }}]},
                "Persona"   : {"rich_text": [{"text": {"content": PERSON }}]},
                "Prestamo"  : {'date': {
                    'start': NOW.isoformat(),
                    'end': None,
                    'time_zone': None
                    }
                },
            }
        }

        response = requests.post(url, headers=HEADERS, json=data_)

        if response.status_code != 200:
            self.button_send.setEnabled(False)
            self.button_send.setText("ERROR PUBLICANDO " + str(response.status_code))
        else:
            self.button_send.setEnabled(False)
            self.na.box.clear()
            self.code.box.clear()
            self.code.box.setFocus()
            self.button_send.setText("SUCCESS")

    def update_date(self, ID, NOW, COMMENT=""):
        url = f"https://api.notion.com/v1/pages/{ID}"
        data_ = {"properties": {
            "Devolucion": {"date": {"start": NOW.isoformat()}},
            "Comentarios": {"rich_text": [{"text": {"content": COMMENT}}]},

        }}
        response = requests.patch(url, headers=HEADERS, json=data_)

        if response.status_code != 200:
            self.button_send.setEnabled(False)
            self.button_send.setText("ERROR PUBLICANDO " + str(response.status_code))
        else:
            self.button_send.setEnabled(False)
            self.na.box.clear()
            self.code.box.clear()
            self.code.box.setFocus()
            self.button_send.setText("SUCCESS")

    def analize(self):

        NOW = now_time()
        ID = self.code.box.text().strip()
        PERSON = self.na.box.text().strip()

        data = get_debt(PERSON)

        if type(data) == int:
            self.button_send.setEnabled(False)
            self.button_send.setText("ERROR RECIBIENDO " + str(data))
            return None

        elif type(data) == list:
            data_no_fee = [n for n in data if n["fee"] == 0]
            data_with_fee = [n for n in data if n["fee"] > 0]

            if ID not in [d["code"] for d in data]:
                if len(data_with_fee) >= 1:
                    self.show_info_view(debt_format(data))
                else:
                    self.publish_new_debt(ID, PERSON, NOW)

            else:
                if ID in [d["code"] for d in data_with_fee]:
                    CARD = data_with_fee.pop([d["code"] for d in data_with_fee].index(ID))
                    self.debt_info = CARD
                    self.show_payment_view(pay_format(CARD))

                elif ID in [d["code"] for d in data_no_fee]:
                    CARD_ID = data_no_fee.pop([d["code"] for d in data_no_fee].index(ID))["id"]
                    self.update_date(CARD_ID, NOW)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    sys.exit(app.exec())