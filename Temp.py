from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

class Application(App):
    def build(self):

        # Label

        self.celcius_in = TextInput()

        self.convert_button = Button(text="Convert")
        self.convert_button.bind(on_press=self.handleConvertButton)

        self.result_label = Label()

        widgets = [
            Label(text="Celcius Input"), self.celcius_in  ,
            self.convert_button        , self.result_label,
        ]

        layout = GridLayout(cols=2)
        for widget in widgets:
            layout.add_widget(widget)
        
        return layout
    
    def handleConvertButton(self, button):
        faren = 1.8 * float(self.celcius_in.text) + 32
        self.result_label.text = f"Farenheit Equivalent: {faren}"

if __name__ == "__main__":
    a = Application()
    a.run()