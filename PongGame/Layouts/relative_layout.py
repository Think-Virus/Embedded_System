from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout


class SimpleRelativeLayout(App):
    def build(self):
        _relative_layout = RelativeLayout()

        _button1 = Button(
            size_hint=(.2, .2),
            pos_hint={'x': 0, 'y': 0},
            text="No 1"
        )
        _button2 = Button(
            size_hint=(.2, .2),
            pos_hint={'right': 1, 'y': 0},
            text="No 2"
        )
        _button3 = Button(
            size_hint=(.2, .2),
            pos_hint={'right': 1, 'top': 1},
            text="No 3"
        )
        _button4 = Button(
            size_hint=(.2, .2),
            pos_hint={'left': 1, 'top': 1},
            text="No 4"
        )
        _button5 = Button(
            size_hint=(.2, .2),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            text="No 5"
        )

        _relative_layout.add_widget(_button1)
        _relative_layout.add_widget(_button2)
        _relative_layout.add_widget(_button3)
        _relative_layout.add_widget(_button4)
        _relative_layout.add_widget(_button5)

        return _relative_layout


SimpleRelativeLayout().run()
