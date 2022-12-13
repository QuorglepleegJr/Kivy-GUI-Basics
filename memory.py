from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock

from random import choice
from math import ceil

import sys
import os

class Cell(BoxLayout):

    def __init__(self, image, parent):
        super(Cell, self).__init__()
        self.image_id = image
        self.image = Image(source=f"assets/{self.image_id}")
        self.button = Button()
        self.button.bind(on_press=self.cellClicked)
        self.add_widget(self.button)
        self.revealed = False
        self.correct = False
        self.super = parent
        self.scheduled_close = None
    
    def cellClicked(self, instance):
        if not self.revealed:
            self.reveal()
            self.scheduled_close = Clock.schedule_once(self.hide, 3)

    def reveal(self):
        self.remove_widget(self.button)
        self.add_widget(self.image)
        self.revealed = True
        self.super.cell_revealed(self)
    
    def hide(self, delta):
        if self.correct or not self.revealed:
            return
        if self.scheduled_close is not None:
            self.scheduled_close.cancel()
        self.remove_widget(self.image)
        self.add_widget(self.button)
        self.super.cell_hidden(self)
        self.revealed = False


class Memory(App):

    def generateImages(self):
        dic = {}
        files = os.listdir(self.path + "/assets")
        for index in range(len(files)):
            dic[index+1] = files[index]
        return dic


    def __init__(self):
        super(Memory, self).__init__()
        self.shown_cells = []
        self.correct_pairs = 0
        self.path = sys.path[0]
        self.images = self.generateImages()

    def build(self):
        cells = []
        images_left = list(self.images.keys())*2
        while len(images_left) > 0:
            value = choice(images_left)
            images_left.remove(value)
            cells.append(Cell(self.images[value], self))
        
        grid = GridLayout(cols=ceil(len(cells)**0.5))
        for cell in cells:
            grid.add_widget(cell)
        
        return grid


    def cell_revealed(self, cell):
        self.shown_cells.append(cell)
        if len(self.shown_cells) >= 2:
            if self.shown_cells[0].image_id == self.shown_cells[1].image_id:
                cell1 = self.shown_cells.pop(0)
                cell2 = self.shown_cells.pop(0)
                cell1.correct = True
                cell2.correct = True
                self.correct_pairs += 1
                if self.correct_pairs == len(self.images):
                    Clock.schedule_once(self.stop, 3)
            else:
                Clock.schedule_once(self.shown_cells[0].hide, 1)
                Clock.schedule_once(self.shown_cells[1].hide, 1)
                self.cell_hidden(self.shown_cells[1])
                self.cell_hidden(self.shown_cells[0])

    def cell_hidden(self, cell):
        try:
            self.shown_cells.remove(cell)
        except ValueError:
            pass

if __name__ == "__main__":
    a = Memory()
    a.run()