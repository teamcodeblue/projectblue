import kivy
from kivy.config import Config
Config.set('graphics', 'resizable', False) # Static window size
Config.set('kivy','window_icon','assets\Logo.ico')
import ModelController
import threading
kivy.require('2.1.0') 
from kivy.properties import StringProperty, ListProperty
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import *
from functools import partial
from kivy.core.text import LabelBase
from kivy.core.window import Window
import time
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
"Taking a break",
"Conquer Humanity",
"Oops..."
]

WINDOW_WIDTH = 750
WINDOW_HEIGHT = 250

class YourWidget(Widget):
    label_text = StringProperty()
    counter = 0
    anim_pt = ListProperty([])
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
        self.canvas.before.clear()
        self.label_text = string
        anim = Animation(opacity=1, duration=3)
        self.strikethrough(anim)
        anim += Animation(opacity=0, duration=3)
        anim.start(self.al)
        return

    def strikethrough(self, anim):
        # start the red line with no points
        with self.canvas.before:
            Color(0/255.0, 204/255.0, 204/255.0)
            self.line = Line(width=5)    # saves a reference to the line

        # animate the end point (self.anim_pt)
        self.anim_pt = [50, 100]
        anim = Animation(anim_pt=[50, 200], d=3)
        anim.start(self)

    def on_anim_pt(self, widget, progress):
        # called when anim_pt changes

        # set up the line points
        points = [50, 100]
        points.extend(self.anim_pt)

        # remove the old line
        self.canvas.before.remove(self.line)

        # draw the updated line
        with self.canvas.before:
            self.line = Line(points=points, width=5)
        return
    


    

class MainApp(App):
    anim_event = 0
    def build(self):
        w = YourWidget()
        t = threading.Thread(target=ModelController.model_main, daemon=True)
        t.start()
        Clock.schedule_once(partial(self.run_animate, t), 0)
        self.anim_event = Clock.schedule_interval(partial(self.run_animate, t), 7)
        Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.icon = 'assets\Logo.ico'
        self.title = 'T-C-B Recommender'
        return w

    def run_animate(self, thread, *args):
        self.root.idle(thread)
        if(not thread.is_alive()):
            self.anim_event.cancel()
            Clock.schedule_once(self.shutdown, 5)

    def shutdown(self, *args):
        exit(0)

if __name__ == '__main__':
    MainApp().run()