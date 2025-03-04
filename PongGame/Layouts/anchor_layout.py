from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button


class AnchorApp(App):
    def build(self):
        _anchor_layout = AnchorLayout(anchor_x='right', anchor_y='bottom')

        _button1 = Button(size_hint=(.2, .2), text="No 1")

        _anchor_layout.add_widget(_button1)

        return _anchor_layout


AnchorApp().run()
