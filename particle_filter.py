# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 12:28:02 2016

@author: Fujiichang
"""

import bayes_filter
import collections


p_o_s = [[0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.01, 0.01, 0.01, 0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
         [0.01, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]]

p_s_a = [[[1, 0, 0, 0, 0], [0.9, 0.1, 0, 0, 0], [0, 0.9, 0.1, 0, 0], [0, 0, 0.9, 0.1, 0], [0, 0, 0, 0.9, 0.1]],
         [[0.1, 0.9, 0, 0, 0], [0, 0.1, 0.9, 0, 0], [0, 0, 0.1, 0.9, 0], [0, 0, 0, 0.1, 0.9],  [0, 0, 0, 0, 1]],
         [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]]]


class ParticleFilter(object):
    def __init__(self, p_s_a, p_o_s):
        self.p_s_a = p_s_a
        self.p_o_s = p_o_s

    def update_p_s_bar(self, particle, a):
        for i, s in enumerate(particle):
            p_s = self.p_s_a[a][s]
            new_s = bayes_filter.multinomial(p_s)
            particle[i] = new_s
        return particle

    def update_p_s(self, particle, o):
        particle_num = len(particle)
        weights = []
        new_particle = []
        new_w_particle = particle_num * [0]

        for s in particle:
            weights.append(self.p_o_s[s][o])
        sum_w = sum(weights)

        for i, weight in enumerate(weights):
            new_w_particle[i] = weight / sum_w

        for _ in range(particle_num):
            i = bayes_filter.multinomial(new_w_particle)
            new_particle.append(particle[i])
        return new_particle


class Controller(object):
    def __init__(self, goals):
        self.goals = goals

    def determine_a(self, determined_s):
        next_goal = self.goals[0]
        if next_goal == determined_s:
            self.goals.pop(0)
            if self.is_terminated() is False:
                next_goal = self.goals[0]
        if next_goal - determined_s < 0:
            a = 0
        elif next_goal - determined_s > 0:
            a = 1
        else:
            a = 2
        return a

    def is_terminated(self):
        return bayes_filter.is_empty(self.goals)


def calculate_ratio_of_particle(particle):
        particle_counter = 5 * [0]
        particle_ratio = 5 * [0]

        for i in range(len(particle_counter)):
            particle_counter[i] = particle.count(i)
        for i in range(len(particle_counter)):
            particle_ratio[i] = particle_counter[i] / float(len(particle))
        return particle_ratio


if __name__ == "__main__":
    o_log = []
    determined_s_log = []
    a_log = []
    actual_s_log = []
    actual_s_log.append(0)
    estimator = ParticleFilter(p_s_a, p_o_s)
    simulator = bayes_filter.Simulator(p_s_a, p_o_s)
    goals = [4, 0]
    controller = Controller(goals)
    particle_num = 1000
    w_particle = particle_num * [0]
    w_particle[0] = 1
    particle = particle_num * [0]
    t = 0

    while True:
        print "step:", t, "##########################"
        o = simulator.get_o()
        o_log.append(o)
        print "o =", o
        particle = estimator.update_p_s(particle, o)
        particle_ratio = calculate_ratio_of_particle(particle)
        bayes_filter.show_p_s(particle_ratio)
        print collections.Counter(particle).most_common(1)
        determined_s = collections.Counter(particle).most_common(1)[0][0]
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
        particle_ratio = calculate_ratio_of_particle(particle)
        bayes_filter.show_p_s(particle_ratio)

    bayes_filter.print_result(o_log, actual_s_log,
                              determined_s_log, a_log, t)
    print "Finish"
