# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 16:09:40 2016

@author: Fujiichang
"""

import random
import matplotlib.pyplot as plt


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


def demo_continuous1d_simulator():
    std_a = 0.1
    std_o = 0.1
    var_a = std_a ** 2
    var_o = std_o ** 2
    simulator = Continuous1dSimulator(var_a, var_o)
    actions = [1] * 4 + [-1] * 4
    s = [simulator.get_s()]

    for a in actions:
        simulator.set_a(a)
        s.append(simulator.get_s())
        o = simulator.get_o()

        print "s :", s[-1]
        print "o :", o

        plt.ylim([-5.0, 5.0])
        plt.bar(range(len(o)), o, align='center')
        plt.grid()
        plt.show()

    plt.gca().invert_yaxis()
    plt.xlabel("state")
    plt.ylabel("time")
    plt.xlim([-1.0, 5.0])
    plt.plot(s, range(len(s)), "g--x", markersize=10)
    plt.grid()
    plt.show()


if __name__ == "__main__":
    demo_continuous1d_simulator()
