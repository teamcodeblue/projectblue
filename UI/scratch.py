from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ListProperty
from kivy.config import Config
from kivy.graphics import Line, Color
from kivy.animation import Animation

class results(Screen):
    anim_pt = ListProperty([])    # this is the line endpoint

    def on_pre_enter(self):
        with self.canvas.before:
            Color(1,1,1)
            Line(points=[100, 100, 100, 200, 200, 200, 200, 100, 300, 100, 300, 200], width=3)

    def on_enter(self):
        # start the red line with no points
        with self.canvas.before:
            Color(1,0,0)
            self.line = Line(width=5)    # saves a reference to the line

        # animate the end point (self.anim_pt)
        self.anim_pt = [100, 100]
        anim = Animation(anim_pt=[100, 200], d=3)
        anim.start(self)

    def on_anim_pt(self, widget, progress):
        # called when anim_pt changes

        # set up the line points
        points = [100, 100]
        points.extend(self.anim_pt)

        # remove the old line
        self.canvas.before.remove(self.line)

        # draw the updated line
        with self.canvas.before:
            self.line = Line(points=points, width=5)

class mazeupdateApp(App):
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '600')
    def build(self):
        FadeTransition.clearcolor = (1,1,1,1)
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(results(name='one'))
        return sm
if __name__ == '__main__':
    mazeupdateApp().run()