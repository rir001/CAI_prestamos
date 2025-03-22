
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
import requests
import datetime
import sys
from env import VERSION, DATABASE_ID, HEADERS, USERNAME
from utils import get_debt, debt_format, get_pendient, pay_format
from params import WINDOW_POSITION, WINDOW_SIZE, BUTTON_POSITION, BUTTON_SIZE
from datetime import datetime, datetime, timezone
fromisoformat = datetime.fromisoformat
now_time = lambda : datetime.now(timezone.utc)
from src.input import CodeInput, NaInput
from github_utils import check_last_version





class Ventana(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('logo/Logo_CAi.png'))
        self.setWindowTitle(f'Prestamos - BanCAi - {VERSION}')
        self.setGeometry(*WINDOW_POSITION, *WINDOW_SIZE)
        self.load_gui()
        self.show()

    def load_gui(self):
        self.load_main_view()
        self.load_info_view()
        self.load_payment_view()
        self.load_headder()

        if not HEADERS():
            self.load_token_form()
            self.token_form.show()
        else:
            self.main_view.show()
        # self.payment_view.show()
        # self.info_view.show()


    def load_token_form(self):
        self.token_form = QWidget(self)
        self.token_form.setGeometry(0, 0, *WINDOW_SIZE)
        self.token_form.setFont(QFont('Arial', 12))
        # self.token_form.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        # self.token_form.move(0, 0)
        # self.token_form.resize(*WINDOW_SIZE)

        self.label_token_form = QLabel("No se ha encontrado el token de Notion", self.token_form)
        self.label_token_form.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.label_token_form.move(0, 50)
        self.label_token_form.resize(WINDOW_SIZE[0], 40)

        self.token_input = QLineEdit(self.token_form)
        self.token_input.move(20, 90)
        self.token_input.resize(WINDOW_SIZE[0]-40, 40)
        self.token_input.setFont(QFont('Arial', 12))
        self.token_input.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.token_input.setPlaceholderText("Token de Notion")

        self.button_token_form = QPushButton("Guardar", self.token_form)
        self.button_token_form.move(20, 130)
        self.button_token_form.resize(WINDOW_SIZE[0]-40, 40)
        self.button_token_form.setFont(QFont('Arial', 12))
        self.button_token_form.clicked.connect(self.save_token)

    def save_token(self):
        # TODO: Evaluate if the token is valid
        HEADERS(self.token_input.text())
        self.token_form.hide()
        self.main_view.show()

    def load_headder(self):
        self.headder = QWidget(self)
        self.headder.setGeometry(0, 0, WINDOW_SIZE[0], 40)
        self.label_headder = QLabel("", self.headder)
        # self.label_headder.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.label_headder.move(0, 0)
        self.label_headder.setFont(QFont('Arial', 18))
        self.label_headder.resize(WINDOW_SIZE[0], 40)
        self.label_headder.setText(f"   Hola {USERNAME()}")

        self.button_change_name_headder = QPushButton('change', self.headder)
        self.button_change_name_headder.move(280, 0)
        self.button_change_name_headder.resize(80, 40)
        self.button_change_name_headder.setFont(QFont('Arial', 16))
        self.button_change_name_headder.clicked.connect(self.load_name_view)

        self.name_input = QLineEdit(self.headder)
        self.name_input.move(20, 0)
        self.name_input.resize(WINDOW_SIZE[0]-40, 40)
        self.name_input.setFont(QFont('Arial', 16))
        self.name_input.hide()
        self.name_input.returnPressed.connect(self.show_name)

    def load_name_view(self):
        self.label_headder.hide()
        self.button_change_name_headder.hide()
        self.name_input.show()

    def show_name(self):
        USERNAME(self.name_input.text())
        self.label_headder.show()
        self.button_change_name_headder.show()
        self.name_input.hide()
        self.label_headder.setText(f"   Hola {USERNAME()}")

    def load_main_view(self):

        self.main_view = QWidget(self)
        self.main_view.setGeometry(0, 0, *WINDOW_SIZE)

        self.code = CodeInput(self.main_view, 20, 60)
        self.na   = NaInput(self.main_view, 20, 120)

        self.label_main = QLabel("", self.main_view)
        self.label_main.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.label_main.move(20, 155)
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
        self.headder.hide()
        self.main_view.hide()
        self.info_view.hide()

        self.label_payment.setText(str(data))
        self.payment_view.show()

    def show_info_view(self, data):
        self.headder.hide()
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
        self.headder.show()


    def able_send_button(self):
        if self.na.able and self.code.able:
            self.button_send.setEnabled(True)
        else:
            self.button_send.setEnabled(False)
        self.label_main.setText("")
        self.button_send.setText("SEND")


    def publish_new_debt(self, ID, PERSON, NOW, COMMENT=""):
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
                "Comentarios": {"rich_text": [{"text": {"content": f"Prestado por {USERNAME()} - {COMMENT}"}}]},
            }
        }

        response = requests.post(url, headers=HEADERS(), json=data_)

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
            "Comentarios": {"rich_text": [{"text": {"content": f"Prestado por {USERNAME()} - {COMMENT}"}}]},

        }}
        response = requests.patch(url, headers=HEADERS(), json=data_)

        if response.status_code != 200:
            self.button_send.setEnabled(False)
            self.button_send.setText("ERROR PUBLICANDO " + str(response.status_code))
            return False
        else:
            self.button_send.setEnabled(False)
            self.na.box.clear()
            self.code.box.clear()
            self.code.box.setFocus()
            self.button_send.setText("SUCCESS")
            return True

    def analize(self):

        if self.button_send.isEnabled():

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
                        if len(get_pendient(ID)) == 0:
                            self.publish_new_debt(ID, PERSON, NOW)
                        else:
                            self.button_send.setEnabled(False)
                            self.button_send.setText("Ya fue prestado")

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