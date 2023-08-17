import discord
from PIL import Image


class Matrix():
    def __init__(self, background:str):
        self.background = Image.open(background)
        self.background_url = background

    def show(self):
        """Returns a file of the processed image"""
        return discord.File(self.background_url)
        #self.background.show

    def save(self):
        """Saves the processed image """
        self.background.save(self.background_url)


    def add(self, colour:str, x:int, y:int):

        content = Image.new('RGBA',(10,10),colour)

        x_pos = ((content.width) * (x - 1))
        y_pos = ((content.height) * (y - 1))

        self.background.paste(content, (x_pos, y_pos), content)