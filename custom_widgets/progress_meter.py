# Kivy dependencies 
from kivy.uix.widget import Widget
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.metrics import dp

# Controller dependency
import ModelController

# ocr-a text font for label
LabelBase.register("ocr-a", fn_regular='assets/ocr-a-extended.ttf')

class ProgressMeter(Widget):

    def __init__(self, **kwargs):
        super(
            ProgressMeter, 
            self,
        ).__init__(**kwargs)

        # Add Progress Bar
        self.bar = ProgressBar(
            max=1000, 
            pos=(dp(100), dp(25)),
            size=(dp(600), dp(50))
            )
        self.add_widget(self.bar)

        # Add Label Corresponding to Progress Bar
        self.label = Label(
            text = "75.0%",
            font_name = "ocr-a",
            font_size = 25,
            halign = 'left',
            pos = (self.bar.center_x - dp(50), self.bar.y - dp(50))
        )
        self.add_widget(self.label)

    # Our handler for when progress has been updated
    def progress_update(self, progress):
        self.bar.value = progress * 10
        self.label.text = str(progress * 1.00) + "%"