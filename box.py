import kivy.app as Apps
import kivy.uix.label as Labels
import kivy.uix.button as Buttons
import kivy.uix.boxlayout as Layouts

class Application(Apps.App):
    def build(self):

        objects = [
            Labels.Label(text="First Label"),
            Labels.Label(text="Second Label"),
            Buttons.Button(text="Click me!"),
        ]

        layout = Layouts.BoxLayout(orientation="vertical")

        for element in objects:
            layout.add_widget(element)
        
        return layout

if __name__ == "__main__":
    a = Application()
    a.run()