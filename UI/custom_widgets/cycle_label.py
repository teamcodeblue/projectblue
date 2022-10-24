# Kivy Dependencies
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text import LabelBase
from kivy.app import App
from kivy.animation import Animation

# Register the font family name
LabelBase.register("o-sans", fn_regular='assets/OdibeeSans-Regular.ttf')

class CycleLabel(FloatLayout):

    # Phrases for our animation to use while model is running
    phrases = [
    "Making Model",
    "Feeding Html",
    "Judging feed",
    "Scraping HTML",
    "Recommending",
    "Taking a break",]

    phrase_index = 0
    def __init__(self, **kwargs):
        super(
            CycleLabel, 
            self,
        ).__init__(**kwargs)

        # Manage layout
        self.size = (450,90)
        self.pos = (100,110)
        # Initialize label
        self.anim_label = Label(
            text = self.phrases[0],
            font_name = "o-sans",
            halign="left",
            font_size = 70,
            pos = self.pos
        )
        self.anim_label.text_size = self.size

        # Add to anchor layout
        self.add_widget(self.anim_label)

        # Initialize counter for cycle animation
        self.counter = 0

    def cycle_step(self):
        # Fade out 
        anim = Animation(opacity=0, duration=3.5)
        anim.bind(on_complete=self.cycle_back)
        anim.start(self.anim_label)
        
    # Callback for second part of animation
    def cycle_back(self, *kwargs):
        # Modify text field
        self.counter += 1
        self.anim_label.text = self.phrases[self.counter % len(self.phrases)]
        # Fade in 
        anim = Animation(opacity=1, duration=3.5)
        anim.start(self.anim_label)