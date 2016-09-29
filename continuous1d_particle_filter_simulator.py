# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 16:09:40 2016

@author: Fujiichang
"""

import random


class Continuous1dSimulator(object):
    def __init__(self, var_a, var_o):
        self._s = 0
        self.std_a = var_a ** 0.5
        self.std_o = var_o ** 0.5
        self.landmarks = [0, 1, 2, 3, 4]

    def _draw_s(self, a):
        actual_a = random.gauss(a, self.std_a)
        new_s = self._s + actual_a
        return new_s

    def get_o(self):
        o = 5 * [0]
        for i in range(len(self.landmarks)):
            distance = self.landmarks[i] - self._s
            o[i] = random.gauss(distance, self.std_o)
        return o

    def set_a(self, a):
        self._s = self._draw_s(a)

    def get_s(self):
        return self._s


def calculate_average_place(particle):
    avg = sum(particle) / len(particle)
    return avg
