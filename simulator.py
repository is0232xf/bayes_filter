# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 16:09:40 2016

@author: Fujiichang
"""

import random


class Simulator(object):
    def __init__(self):
        self._s = 0
        self.sigma = 0.1
        self.landmark = [0, 1, 2, 3, 4]

    def _draw_s(self, actual_a):
        new_s = self._s + actual_a
        return new_s

    def get_o(self):
        o = 5 * [0]
        for i in range(len(self.landmark)):
            mu = self.landmark[i] - self._s
            o[i] = random.gauss(mu, self.sigma)
        return o

    def set_a(self, a):
        actual_a = random.gauss(a, self.sigma)
        self._s = self._draw_s(actual_a)

    def get_s(self):
        return self._s


if __name__ == "__main__":
    simulator = Simulator()
    a = 1

    for i in range(4):
        simulator.set_a(a)
        s = simulator.get_s()
        o = simulator.get_o()

        print "s :", s
        print "o :", o
