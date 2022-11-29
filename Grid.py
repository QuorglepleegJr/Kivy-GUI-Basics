from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

class Application(App):

    def __init__(self, mode=0):
        self.mode = mode
        super(Application, self).__init__()

    def build(self):

        self.first_num_in = TextInput(multiline=False)
        self.second_num_in = TextInput(multiline=False)

        if self.mode == 0:
            button_text = "Multiply"
        else:
            button_text = "Add"
        self.calculate_button = Button(text=button_text)
        self.calculate_button.bind(on_press=self.handleButtonClick)

        self.result_label = Label(text="")

        elements = [
            Label(text="First Number") , self.first_num_in ,
            Label(text="Second Number"), self.second_num_in,
            self.calculate_button      , self.result_label ,
        ]

        grid = GridLayout(cols=2)
        for element in elements:
            grid.add_widget(element)
        
        return grid
    
    def handleButtonClick(self, instance):
        if self.mode == 0:
            result = self.getFirstNum() * self.getSecondNum()
        else:
            result = self.getFirstNum() + self.getSecondNum()
        self.result_label.text = f"Result: {result}"
    
    def getFirstNum(self):
        return int(self.first_num_in.text)
    
    def getSecondNum(self):
        return int(self.second_num_in.text)

if __name__ == "__main__":
   a = Application()
   a.run()
   b = Application(1)
   b.run()