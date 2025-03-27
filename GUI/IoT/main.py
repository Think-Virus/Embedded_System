import json
import traceback
from threading import Thread

import requests
import serial.tools.list_ports
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.button import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex

Window.borderless = True  # Hide the basic button to minimize, maximize and close screen functions


# seperator is to create space and line in a floatlayout
class Separator(FloatLayout):
    pass


# spacer is used to place a space
class Spacer(Label):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class LabelButton(ButtonBehavior, Label):
    pass


class SignupScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class DashboardScreen(Screen):
    def on_enter(self):
        App.get_running_app().thread_init()


GUI = Builder.load_file("main.kv")

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '900')
Config.write()


class MainApp(App):
    # Firebase
    wak = 'AIzaSyDLkkzgHf0dulDOIzfWTWhziBnYIgRxxjw'
    local_id = ""
    id_token = ""

    # STM Board
    iot_device = None

    temp_sensor_val = 0
    pressure_sensor_val = 0
    cloud_src1_val = 0
    cloud_src2_val = 0

    bat1_val = 0
    bat2_val = 0

    val_ctr1_val = 0
    val_ctr2_val = 0
    val_ctr3_val = 0
    val_ctr4_val = 0
    val_ctr5_val = 0

    switch1_val = 0
    switch2_val = 0

    def build(self):
        return GUI

    def on_start(self):
        LabelBase.register(name='myraid_pro_reg', fn_regular='fonts/MYRIADPRO-REGULAR.OTF')
        LabelBase.register(name='d_din_reg', fn_regular='fonts/d-din.regular.ttf')
        LabelBase.register(name='bistecca', fn_regular='fonts/Bistecca.ttf')
        LabelBase.register(name='teko-reg', fn_regular='fonts/Teko-Regular.ttf')
        LabelBase.register(name='barlow-reg', fn_regular='fonts/BarlowSemiCondensed-Regular.ttf')
        LabelBase.register(name='barlow-bold', fn_regular='fonts/BarlowSemiCondensed-SemiBold.ttf')
        LabelBase.register(name='roboto-medium', fn_regular='fonts/Roboto-Medium.ttf')
        LabelBase.register(name='roboto-thin', fn_regular='fonts/Roboto-Thin.ttf')

    def process_sign_up(self):
        self.sign_up(self.root.ids['signup_screen'].ids['sign_up_email_id'].text, self.root.ids['signup_screen'].ids['sign_up_password_id'].text)

    def sign_up(self, email, password):
        sign_up_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.wak
        sign_up_payload = {"email": email, "password": password, "returnSecureToken": True}
        sign_up_request = requests.post(sign_up_url, data=sign_up_payload)

        print(sign_up_request.ok)
        print(sign_up_request.content.decode('utf-8'))

        sign_up_data = json.loads(sign_up_request.content.decode('utf-8'))
        if not sign_up_request.ok:
            error_data = json.loads(sign_up_request.content.decode('utf-8'))
            error_message = error_data['error']['message']
            self.root.ids['signup_screen'].ids['error_label_id'].text = error_message
            self.root.ids['signup_screen'].ids['error_label_id'].color = get_color_from_hex('#ff0000')
        else:
            realtime_database_url = "https://iotdashboard-ffb97-default-rtdb.firebaseio.com/"

            refresh_toke = sign_up_data['refreshToken']
            self.local_id = sign_up_data['localId']
            self.id_token = sign_up_data['idToken']

            device_data = '{"battery": 0, "battery1": 0, "cloud1": 0, "cloud2": 0, "pressure": 0, "switch1": 0, "switch2": 0, "temperature": 0}'
            requests.patch(realtime_database_url + self.local_id + ".json?auth=" + self.id_token, data=device_data)

            self.process_dashboard()

    @staticmethod
    def get_port():
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if port.manufacturer.startswith("STM"):
                port_number = port.device
        return port_number

    def thread_init(self):
        try:
            self.iot_device = serial.Serial(port=self.get_port(), baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=1)
        except serial.SerialException as e:
            print(traceback.format_exc())
        Clock.schedule_interval(self.update_dashboard_ui, 1)
        Clock.schedule_interval(self.update_firebase, 1)

        self.main_thread = Thread(target=self.get_sensor_data)
        self.main_thread.daemon = True
        self.main_thread.start()

    def update_firebase(self, arg):
        realtime_database_url = "https://iotdashboard-ffb97-default-rtdb.firebaseio.com/"
        device_data = {
            "battery": int(self.bat1_val / 52),  # 예시: 배터리 퍼센트를 0~10으로 환산
            "battery1": int(self.bat2_val / 52),
            "cloud1": self.cloud_src1_val,
            "cloud2": self.cloud_src2_val,
            "pressure": self.pressure_sensor_val,
            "switch1": self.switch1_val,
            "switch2": self.switch2_val,
            "temperature": int(self.temp_sensor_val / 50)
        }
        requests.patch(realtime_database_url + self.local_id + ".json?auth=" + self.id_token, data=json.dumps(device_data))

    def get_sensor_data(self):
        while True:
            try:
                value = self.iot_device.readline()
            except Exception as e:
                print(traceback.format_exc())
                pass

            try:
                new_value = int(value[1:].decode('utf-8'))
                if chr(value[0]) == 'A':
                    self.temp_sensor_val = new_value
                if chr(value[0]) == 'B':
                    self.pressure_sensor_val = new_value
                if chr(value[0]) == 'C':
                    self.bat1_val = new_value
                if chr(value[0]) == 'D':
                    self.bat2_val = new_value

            except Exception as e:
                print(value)
                print(traceback.format_exc())
                pass

    def update_dashboard_ui(self, arg):
        try:
            _celsius = int(self.temp_sensor_val / 50)
            if _celsius < 10:
                _celsius = 10
            self.root.ids['dashboard_screen'].ids['temp_sensor_label_id'].text = str(_celsius) + "ºC"
            if _celsius > 75:
                self.root.ids['dashboard_screen'].ids['temp_sensor_img_id'].source = "icons/7.png"
            elif _celsius > 65:
                self.root.ids['dashboard_screen'].ids['temp_sensor_img_id'].source = "icons/6.png"
            elif _celsius > 55:
                self.root.ids['dashboard_screen'].ids['temp_sensor_img_id'].source = "icons/5.png"
            elif _celsius > 45:
                self.root.ids['dashboard_screen'].ids['temp_sensor_img_id'].source = "icons/4.png"
            elif _celsius > 35:
                self.root.ids['dashboard_screen'].ids['temp_sensor_img_id'].source = "icons/3.png"
            elif _celsius > 25:
                self.root.ids['dashboard_screen'].ids['temp_sensor_img_id'].source = "icons/2.png"
            else:
                self.root.ids['dashboard_screen'].ids['temp_sensor_img_id'].source = "icons/1.png"

            _battery1 = int(self.bat1_val / 52)
            if _battery1 < 5:
                _battery1 = 5
            if _battery1 > 40:
                self.root.ids['dashboard_screen'].ids['bat1_img_id'].source = "icons/bat5.png"
            elif _battery1 > 30:
                self.root.ids['dashboard_screen'].ids['bat1_img_id'].source = "icons/bat4.png"
            elif _battery1 > 20:
                self.root.ids['dashboard_screen'].ids['bat1_img_id'].source = "icons/bat3.png"
            elif _battery1 > 10:
                self.root.ids['dashboard_screen'].ids['bat1_img_id'].source = "icons/bat2.png"
            else:
                self.root.ids['dashboard_screen'].ids['bat1_img_id'].source = "icons/bat1.png"

            _battery2 = int(self.bat2_val / 52)
            if _battery2 < 5:
                _battery2 = 5
            if _battery2 > 40:
                self.root.ids['dashboard_screen'].ids['bat2_img_id'].source = "icons/bat5.png"
            elif _battery2 > 30:
                self.root.ids['dashboard_screen'].ids['bat2_img_id'].source = "icons/bat4.png"
            elif _battery2 > 20:
                self.root.ids['dashboard_screen'].ids['bat2_img_id'].source = "icons/bat3.png"
            elif _battery2 > 10:
                self.root.ids['dashboard_screen'].ids['bat2_img_id'].source = "icons/bat2.png"
            else:
                self.root.ids['dashboard_screen'].ids['bat2_img_id'].source = "icons/bat1.png"

        except Exception as e:
            print(traceback.format_exc())
            pass

    def process_switch1(self):
        if self.switch1_val:
            self.root.ids['dashboard_screen'].ids['switch_1_id'].source = "icons/switchon.png"
            self.root.ids['dashboard_screen'].ids['switch_1_label_id'].text = "ON"
            self.root.ids['dashboard_screen'].ids['switch_1_label_id'].color = get_color_from_hex('#f26a21')

            self.switch1_val = 0
            self.send_data("A1")
            print("Switch 1 toggled ON")
        else:
            self.root.ids['dashboard_screen'].ids['switch_1_id'].source = "icons/switchoff.png"
            self.root.ids['dashboard_screen'].ids['switch_1_label_id'].text = "OFF"
            self.root.ids['dashboard_screen'].ids['switch_1_label_id'].color = get_color_from_hex('#0b172e')

            self.switch1_val = 1
            self.send_data("A0")
            print("Switch 1 toggled OFF")

    def process_switch2(self):
        if self.switch2_val:
            self.root.ids['dashboard_screen'].ids['switch_2_id'].source = "icons/switchon.png"
            self.root.ids['dashboard_screen'].ids['switch_2_label_id'].text = "ON"
            self.root.ids['dashboard_screen'].ids['switch_2_label_id'].color = get_color_from_hex('#f26a21')

            self.switch2_val = 0
            self.send_data("B1")
            print("Switch 2 toggled ON")
        else:
            self.root.ids['dashboard_screen'].ids['switch_2_id'].source = "icons/switchoff.png"
            self.root.ids['dashboard_screen'].ids['switch_2_label_id'].text = "OFF"
            self.root.ids['dashboard_screen'].ids['switch_2_label_id'].color = get_color_from_hex('#0b172e')

            self.switch2_val = 1
            self.send_data("B0")
            print("Switch 2 toggled OFF")

    def send_data(self, data):
        try:
            self.iot_device.write(data.encode())
        except Exception as e:
            print(traceback.format_exc())
            pass

    def process_dashboard(self):
        GUI.current = "dashboard_screen"

    def process_signup(self):
        GUI.current = "signup_screen"

    def process_login(self):
        GUI.current = "login_screen"

    def close(self):
        quit()

    def minimize(self):
        Window.minimize()


MainApp().run()
