# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 19:08:12 2016

@author: Fujiichang
"""

import numpy as np
from scipy.stats import norm
import random
import bayes_filter


class Continuous1dControllor(object):
    def __init__(self, goals):
        self.goals = goals

    def determine_a(self, determined_s):
        next_goal = self.goals[0]
        eps = 0.3
        diff = next_goal - determined_s
        direction = np.sign(diff)
        distance = abs(diff)

        if distance < eps:
            self.goals.pop(0)
            if self.is_terminated() is False:
                next_goal = self.goals[0]
            a = direction * distance
        elif distance > eps:
            a = direction * 1
        else:
            a = 0
        return a

    def is_terminated(self):
        return bayes_filter.is_empty(self.goals)


class Continuous1dParticlefilter(object):
    def __init__(self, var_a, var_o):
        self.std_a = var_a ** 0.5
        self.std_o = var_o ** 0.5

    def update_p_s_bar(self, particle, a):
        for i, s in enumerate(particle):
            new_s = random.gauss(s+a, self.std_a)
            particle[i] = new_s
        return particle

    def update_p_s(self, particle, o):
        particle_num = len(particle)
        weights = []

        for s in particle:
            weights.append(norm.pdf(o[0], particle, self.std_o))
        sum_w = sum(weights)
        weights = []
        new_particle = []
        new_w_particle = particle_num * [0]

        for i, weight in enumerate(weights):
            new_w_particle[i] = weight / sum_w

        for _ in range(particle_num):
            i = bayes_filter.multinomial(new_w_particle)
            new_particle.append(particle[i])
        return new_particle
