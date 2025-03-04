from kivy.app import App
from kivy.lang import Builder

GUI = Builder.load_string("""
Label:
    text:
        ('[b]Hello[/b][color=ff0099]World[/color]\\n'
        '[color=ff0099]Hello[/color][b]World[/b]\\n'
        '[i]Hello[/i][color=ff0099]World[/color]')
    markup: True
    font_size :'64pt'
""")


class LabelWithMarkup(App):
    def build(self):
        return GUI


LabelWithMarkup().run()
