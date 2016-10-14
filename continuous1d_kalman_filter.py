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
    def __init__(self, goals, allowable_range):
        self.goals = goals
        self.allowable_range = allowable_range

    def determine_s(self, p_s):
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


class Continuous1dKalmanfilter(object):
    def __init__(self, var_a, var_o, var_s, landmarks):
        self.std_a = var_a ** 0.5
        self.std_o = var_o ** 0.5
        self.std_s = var_s ** 0.5
        self.landmarks = np.array(landmarks).reshape(-1, 1)

    def update_p_s_bar(self, p_s, a):
        std_s_bar = (self.std_s+self.std_a)**-1
        p_s_bar = random.gauss(p_s+a, std_s_bar)
        return p_s_bar

    def update_p_s(self, p_s_bar, o):
        std_s_bar = (self.std_s+self.std_a)**-1
        precision_o = self.std_o**-1 + std_s_bar
        p_s = random.gauss((self.std_o**1*o[0]+std_s_bar*p_s_bar)/precision_o,
                           (self.std_o**-1+std_s_bar)**-1)
        return p_s
