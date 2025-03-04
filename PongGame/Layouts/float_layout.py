from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config

Config.set('graphics', 'resizeable', True)


class SimpleApp(App):

    def build(self):
        _layout = FloatLayout()

        _btn = Button(text='This is a button',
                      size_hint=(0.3, 0.2),
                      pos_hint={"left": 0.1, "top": 1}
                      )

        _layout.add_widget(_btn)
        return _layout


SimpleApp().run()
