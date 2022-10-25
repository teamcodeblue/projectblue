# Window specifications
from kivy.config import Config
Config.set('graphics', 'resizable', False) # Static window size
Config.set('kivy','window_icon','assets\Logo.ico') # Windows Window Icon

# Windows (OS) mouse cursor
#from ctypes import windll

# Kivy Dependencies
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget

# Callback/threading Dependencies
from functools import partial
import threading

# Widet Dependencies for main.kv
from custom_widgets import cycle_label
from custom_widgets import progress_meter

# Controller dependencies
from ModelController import Globals
from ModelController import model_main

# Specifying size of window
WINDOW_WIDTH = 850
WINDOW_HEIGHT = 250

#test dep
from model.ContentBasedReccomendation.model_defs import ArticleClassifier


# Root widget of application (will be parent of all others (container))
class RootWidget(Widget):

    def handle_anims(self):
        self.ids.c_label.cycle_step()
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        Window.bind(mouse_pos = self.button_mouseover) # mouse position handler

    # Check for collision between menu buttons and mouse
    def button_mouseover(self, instance, pos):
        # Check for collision with 
        if self.ids.settings_button.collide_point(*pos) or self.ids.status_button.collide_point(*pos):
            Window.set_system_cursor("hand")
        else:
            Window.set_system_cursor("arrow")
    
    # A handler for the button release event (Should start/stop model)
    def status_released(self):
        if self.ids.status_image.source == 'assets/play.png':
            self.ids.status_image.source = 'assets/pause.png'
            # Put method to pause model here
        else:
            self.ids.status_image.source = 'assets/play.png'
            # Put method to unpause model here
# Our entry point 
class MainApp(App):
    def build(self):
        Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

        # Create our worker thread
        self.thread = threading.Thread(target=model_main, daemon=True)
        self.thread.start()

        # Schedule our animations based on the worker thread
        self.thread_event = Clock.schedule_interval(partial(self.thread_anim, self.thread), 7.5)

        # Schedule our UI updates
        self.progress_update = Clock.schedule_interval(partial(self.progress_check), .1)
        return RootWidget()

    def thread_anim(self, thread, *args):
        if(not self.thread.is_alive()):
            self.thread_event.cancel() # Prevent all updates from happening again
            # Clock.schedule_once()  # Update our label to be done cycling
            return
        # All our animations for the children widgets

        # Updating text Anchor->CycleLabel
        self.root.handle_anims()
    
    def progress_check(self, *args):
        self.root.ids.p_bar.progress_update(Globals.PROGRESS)
    
if __name__ == '__main__':
    MainApp().run()