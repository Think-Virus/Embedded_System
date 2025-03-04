from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout


class SimpleStackApp(App):
    def build(self):
        _stack_layout = StackLayout(orientation='lr-tb')

        _button1 = Button(
            size_hint=(.2, .1),
            text="No 1"
        )
        _button2 = Button(
            size_hint=(.2, .1),
            text="No 2"
        )
        _button3 = Button(
            size_hint=(.2, .1),
            text="No 3"
        )
        _button4 = Button(
            size_hint=(.3, .1),
            text="No 4"
        )
        _button5 = Button(
            size_hint=(.2, .1),
            text="No 5"
        )
        _button6 = Button(
            size_hint=(.2, .1),
            text="No 6"
        )
        _button7 = Button(
            size_hint=(.2, .1),
            text="No 7"
        )

        _stack_layout.add_widget(_button1)
        _stack_layout.add_widget(_button2)
        _stack_layout.add_widget(_button3)
        _stack_layout.add_widget(_button4)
        _stack_layout.add_widget(_button5)
        _stack_layout.add_widget(_button6)
        _stack_layout.add_widget(_button7)

        return _stack_layout


SimpleStackApp().run()
