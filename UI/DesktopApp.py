import kivy
import ModelController
import threading
kivy.require('2.1.0') 
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import *
from functools import partial
from kivy.core.text import LabelBase
'''
T-C-B UI for desktop App

Runs idle animations while model is being updated 
on a seperate thread 

version 1.0 

'''
# Phrases for our animation to use while model is running
phrases = [
"Generating model",
"Feeding Html",
"Judging your feed",
"Scraping HTML",
"Recommending",
"Taking a break"
]

class YourWidget(Widget):
    label_text = StringProperty()
    counter = 0

    def __init__(self, **kwargs):
        LabelBase.register("ocr-a", fn_regular='assets/ocr-a-extended.ttf')
        super(YourWidget, self).__init__(**kwargs)
        self.label_text = "Uninitialized"


    def idle(self, thread):
        # Play fade-to-cross animation cycling through phrases
        if(thread.is_alive()):
            self.fade_cross(phrases[self.counter])
            self.counter = (self.counter + 1) % len(phrases)
        else:
            self.fade_cross("Finished!")
        return
    
    def fade_cross(self, string):
        # Fade in 
        self.label_text = string
        anim = Animation(opacity=1, duration=3)
        anim += Animation(opacity=0, duration=3)
        anim.start(self.al)
        return
    
    # Animation function to do a strikethrough a string
    def strikethrough(self):
        return
    

class MainApp(App):
    def build(self):
        w = YourWidget()
        t = threading.Thread(target=ModelController.model_main, daemon=True)
        t.start()
        Clock.schedule_once(partial(self.run_animate, t), 0)
        Clock.schedule_interval(partial(self.run_animate, t), 7)
        return w

    def run_animate(self, thread, *args):
        if(not thread.is_alive()):
            Clock.unschedule(self.run_animate)
        self.root.idle(thread)

if __name__ == '__main__':
    MainApp().run()