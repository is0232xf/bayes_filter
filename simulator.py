# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 16:09:40 2016

@author: Fujiichang
"""

import random
import continuous1d_particle_filter
import bayes_filter


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

if __name__ == "__main__":
    std_a = 0.1
    std_o = 0.1
    var_a = std_a ** 2
    var_o = std_o ** 2
    goals = [4, 0]
    o_log = []
    determined_s_log = []
    a_log = []
    actual_s_log = []
    actual_s_log.append(0)
    estimator = continuous1d_particle_filter.Continuous1dParticlefilter(
        var_a, var_o)
    simulator = Continuous1dSimulator(var_a, var_o)
    goals = [4, 0]
    controller = continuous1d_particle_filter.Continuous1dControllor(goals)
    particle_num = 1000
    w_particle = particle_num * [0]
    w_particle[0] = 1
    particle = particle_num * [0]
    t = 0

    while True:
        print "step:", t, "##########################"
        o = simulator.get_o()
        o_log.append(o[0])
        print "o =", o
        particle = estimator.update_p_s(particle, o)
        determined_s = calculate_average_place(particle)
        determined_s_log.append(determined_s)

        a = controller.determine_a(determined_s)
        a_log.append(a)
        print "a =", a

        if controller.is_terminated():
            break

        simulator.set_a(a)
        s = simulator.get_s()
        actual_s_log.append(s)
        print "s =", s
        t = t + 1
        particle = estimator.update_p_s_bar(particle, a)
    bayes_filter.print_result(o_log, actual_s_log,
                              determined_s_log, a_log, t)
    print "Finish"
