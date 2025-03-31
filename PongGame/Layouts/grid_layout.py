from kivy.app import App
from kivy.lang import Builder

GUI = Builder.load_string("""
GridLayout:
    cols:2
    rows:2
    
    Button:
        text: 'No 1'
    Button:
        text: 'No 2'
    Button:
        text: 'No 3'
    Button:
        text: 'No 4'
""")


class GridApp(App):
    def build(self):
        return GUI


GridApp().run()
