import kivy.app as Apps
import kivy.uix.label as Labels

class Application(Apps.App):
    def build(self):
        return Labels.Label(text="Hello World!")

if __name__ == "__main__":
    myApp = Application()
    myApp.run()