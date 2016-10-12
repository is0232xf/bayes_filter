# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 19:08:12 2016

@author: Fujiichang
"""

import numpy as np
from scipy.stats import norm
import bayes_filter


class Continuous1dControllor(object):
    def __init__(self, goals, allowable_range):
        self.goals = goals
        self.allowable_range = allowable_range

    def determine_s(self, particle):
        avg = sum(particle) / len(particle)
        return avg

    def determine_next_goal(self, determined_s):
        next_goal = self.goals[0]
        allowable_range = self.allowable_range
        diff = next_goal - determined_s
        distance = abs(diff)

        if distance < allowable_range:
            self.goals.pop(0)
            if self.is_terminal() is False:
                next_goal = self.goals[0]
        return next_goal

    def determine_a(self, determined_s):
        next_goal = self.determine_next_goal(determined_s)
        diff = next_goal - determined_s
        direction = np.sign(diff)
        distance = abs(diff)

        a = direction * min(1, distance)
        return a

    def is_terminal(self):
        return bayes_filter.is_empty(self.goals)


class Continuous1dParticlefilter(object):
    def __init__(self, var_a, var_o, landmarks):
        self.std_a = var_a ** 0.5
        self.std_o = var_o ** 0.5
        self.landmarks = np.array(landmarks).reshape(-1, 1)

    def update_p_s_bar(self, particle, a):
        means = np.array(particle) + a
        new_particles = np.random.normal(means, self.std_a)
        return new_particles.tolist()

    def update_p_s(self, particle, o):
        particle_num = len(particle)
        weights = []
        l = len(self.landmarks)
        particle = np.array(particle)
        o_l = np.array(o[:l]).reshape(-1, 1)

        distance = self.landmarks[:l]-particle
        weights = norm.pdf(o_l, distance, self.std_o)
        p_weights = np.prod(weights, axis=0)

        new_w_particle = p_weights / p_weights.sum()

        new_particle = []

        for _ in range(particle_num):
            i = bayes_filter.multinomial(new_w_particle)
            new_particle.append(particle[i])
        return new_particle
