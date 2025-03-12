from threading import Thread

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
    pass


GUI = Builder.load_file("main.kv")

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '900')
Config.write()


class MainApp(App):

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

    def get_port(self):
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if port.manufacturer.startswith("STM"):
                port_number = port.device
        return port_number

    def thread_init(self):
        try:
            self.iot_device = serial.Serial(port=self.get_port(), baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=1)
        except serial.SerialException as e:
            print(e)
        Clock.schedule_interval(self.update_dashboard_ui, 1)

        self.main_thread = Thread(target=self.get_sensor_data)
        self.main_thread.daemon = True
        self.main_thread.start()

    def get_sensor_data(self):
        pass

    def update_dashboard_ui(self):
        pass

    def process_switch1(self):
        pass

    def process_switch2(self):
        pass

    def send_data(self, data):
        pass

    def process_signup(self):
        GUI.current = "signup_screen"

    def process_login(self):
        GUI.current = "login_screen"

    def close(self):
        quit()

    def minimize(self):
        Window.minimize()


MainApp().run()
