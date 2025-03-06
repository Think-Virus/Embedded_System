from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior,Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from threading import Thread
import serial.tools.list_ports

import kivy.utils as utils

Window.borderless = True

#seperator is to create space and line in a floatlayout
class Separator(FloatLayout):
    pass

#spacer is used to place a space
class Spacer(Label):
    pass

class ImageButton(ButtonBehavior,Image):
    pass
class LabelButton(ButtonBehavior,Label):
    pass

class SignupScreen(Screen):
    pass

GUI =  Builder.load_file("main.kv")

Config.set('graphics', 'width','1200')
Config.set('graphics', 'height','900')
Config.write()

class MainApp(App):
    def build(self):
        return GUI

    def on_start(self):
        LabelBase.register(name='myraid_pro_reg',fn_regular ='MYRIADPRO-REGULAR.OTF')
        LabelBase.register(name= 'd_din_reg',fn_regular = 'd-din.regular.ttf')
        LabelBase.register(name= 'bistecca',fn_regular = 'Bistecca.ttf')
        LabelBase.register(name= 'teko-reg',fn_regular = 'Teko-Regular.ttf')
        LabelBase.register(name= 'barlow-reg',fn_regular = 'BarlowSemiCondensed-Regular.ttf')
        LabelBase.register(name= 'barlow-bold',fn_regular = 'BarlowSemiCondensed-SemiBold.ttf')
        LabelBase.register(name= 'roboto-medium',fn_regular = 'Roboto-Medium.ttf')
        LabelBase.register(name= 'roboto-thin',fn_regular = 'Roboto-Thin.ttf')

    def process_signup(self):
        pass

    def close(self):
        quit()

    def minimize(self):
        Window.minimize()

MainApp().run()
