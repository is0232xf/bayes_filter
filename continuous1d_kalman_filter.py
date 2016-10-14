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

    def determine_s(self, mu, alpha):
        determined_s = random.gauss(mu, alpha)
        return determined_s

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
    def __init__(self, alpha, beta, gamma, landmarks):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.landmarks = np.array(landmarks).reshape(-1, 1)

    def update_p_s_bar(self, mu, a):
        mu_bar = mu + a
        alpha_bar = (self.alpha**-1 + self.beta**-1)**-1
        return mu_bar, alpha_bar

    def update_p_s(self, mu_bar, alpha_bar, o):
        mu = (self.gamma*(-o[0]) + alpha_bar*mu_bar) / (self.gamma + alpha_bar)
        alpha = self.gamma + alpha_bar
        return mu, alpha
