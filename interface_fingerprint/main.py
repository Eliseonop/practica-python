from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

class KinectViewerApp(App):
    def build(self):
        root = BoxLayout(orientation='horizontal')

        # Left panel
        left_panel = BoxLayout(orientation='vertical')
        toggle_kinect_viewer = ToggleButton(text='Kinect Viewer', group='menu', state='down')
        toggle_kivy = ToggleButton(text='Kivy', group='menu',)
        left_panel.add_widget(toggle_kinect_viewer)
        left_panel.add_widget(toggle_kivy)
        close_button = Button(text='Close', size_hint=(1, 0.1))
        left_panel.add_widget(close_button)

        # Right panel
        right_panel = GridLayout(cols=2, padding=10, spacing=10)

        # Kinect section
        right_panel.add_widget(Label(text='Kinect Viewer', bold=True))
        right_panel.add_widget(Label())
        right_panel.add_widget(Label(text='Kinect', size_hint_x=None, width=100))
        right_panel.add_widget(TextInput())
        right_panel.add_widget(Label(text='Index', size_hint_x=None, width=100))
        right_panel.add_widget(TextInput(text='0'))
        right_panel.add_widget(Label(text='Shaders', bold=True))
        right_panel.add_widget(Label())
        right_panel.add_widget(Label(text='Theme', size_hint_x=None, width=100))
        right_panel.add_widget(TextInput(text='rgb'))

        root.add_widget(left_panel)
        root.add_widget(right_panel)

        return root

if __name__ == '__main__':
    KinectViewerApp().run()
