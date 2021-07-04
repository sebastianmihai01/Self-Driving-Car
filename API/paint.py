import numpy as np

""" Paint tool to draw maps and levels """
""" Also used to save or load the progress """


class Paint(object):

    def clean(self, brain, obstacles, x, y):
        obstacles = np.zeros((x, y))

    def progress_save(self, ai):
        ai.save()

    def progress_load(self, ai):
        ai.load()

