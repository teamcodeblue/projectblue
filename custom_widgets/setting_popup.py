

from kivy.uix.popup import Popup


class SettingPopup(Popup):
    
    def limit_changed(self):
        self.ids.GPU_limit_value_label.text = str(self.ids.GPU_Slider.value) + "%"