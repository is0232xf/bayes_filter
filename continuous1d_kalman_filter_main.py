# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 20:55:54 2016

@author: Fujiichang
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import continuous1d_kalman_filter
import continuous1d_simulator


def show_particle_distribution(particle, s, determined_s, title,
                               ylabel="density"):
    plt.plot(determined_s, 0.2, 'o', markersize=20, label="determined_s")
    plt.plot(s, 0.2, 'r*', markersize=20, label="actual_s")
    plt.legend(loc='upper right', fontsize=15, numpoints=1)
    plt.grid()
    plt.hist(particle, bins=20, normed=True, histtype='stepfilled')
    plt.title(title)
    plt.xlabel("state")
    plt.ylabel(ylabel)
    plt.xlim(-1, 5)
    plt.ylim(0, 2)
    plt.show()


def show_result(s, title, line_type):
    plt.xlim(-1, 5)
    plt.grid()
    plt.title(title)
    plt.tight_layout()
    plt.gca().invert_yaxis()
    plt.xlabel("state")
    plt.ylabel("time")
    plt.plot(s, range(len(s)), line_type, markersize=10)
    plt.show()


def show_merged_result(s, determined_s):
    plt.xlim(-1, 5)
    plt.title("merged result")
    plt.tight_layout()
    plt.gca().invert_yaxis()
    plt.xlabel("state")
    plt.ylabel("time")
    plt.plot(determined_s, range(len(determined_s)), "-+", markersize=10,
             label="determined_s")
    plt.plot(s, range(len(s)), "g--x", markersize=10, label="actual_s")
    plt.legend(loc='upper right', fontsize=12)
    plt.grid()
    plt.show()


def show_distribution(mu, sigma, title):
    x = np.linspace(-1, 5, 100)
    p = norm(mu, sigma**-0.5)
    plt.xlim(-1, 5)
    plt.grid()
    plt.title(title)
    plt.tight_layout()
    plt.xlabel("state")
    plt.ylabel("prediction")
    plt.plot(x, p.pdf(x))
    plt.show()


def calculate_rms(actual_s_log, determined_s_log):
    accidental_error = []
    for t in range(len(actual_s_log)):
        accidental_error.append(abs(actual_s_log[t] - determined_s_log[t])**2)
    sum_a = sum(accidental_error)
    rms = math.sqrt(sum_a)
    return rms

if __name__ == "__main__":
    std_a = 0.3
    std_o = 0.1
    std_s = 0.5
    var_a = std_a ** 2
    var_o = std_o ** 2
    # alpha is precision of state distribution
    alpha = (std_s ** 2) ** -1
    # beta is precision of motion model variance
    beta = (std_a ** 2) ** -1
    # gamma is precision of observation model variance
    gamma = (std_o ** 2) ** -1
    mu_bar = 0
    alpha_bar = 0.05
    allowable_range = 0.3
    o_log = []
    determined_s_log = []
    a_log = []
    actual_s_log = []
    actual_s_log.append(0)
    simulator = continuous1d_simulator.Continuous1dSimulator(
        var_a, var_o)
    estimator = continuous1d_kalman_filter.Continuous1dKalmanfilter(
         alpha, beta, gamma, simulator.landmarks)
    goals = [4, 0]
    controller = continuous1d_kalman_filter.Continuous1dControllor(
        goals, allowable_range)
    s = 0
    t = 0

    while True:
        print "step:", t, "##########################"
        o = simulator.get_o()
        o_log.append(o[0])
        print "o =", o
        mu, alpha = estimator.update_p_s(mu_bar, alpha_bar, o)
        determined_s = controller.determine_s(mu, alpha**-1)
        determined_s_log.append(determined_s)
        show_distribution(mu, alpha, "after observation")

        print "detemined_s =", determined_s
        print "          s =", s

        a = controller.determine_a(determined_s)
        a_log.append(a)
        print "a =", a

        if controller.is_terminal():
            break

        simulator.set_a(a)
        s = simulator.get_s()
        actual_s_log.append(s)
        print "s =", s
        t = t + 1
        mu_bar, alpha_bar = estimator.update_p_s_bar(mu, a)

    show_result(actual_s_log, "actual s", "g--x")
    show_result(determined_s_log, "determined s", "-+")
    show_merged_result(actual_s_log, determined_s_log)
    print "RMS =",  calculate_rms(actual_s_log, determined_s_log)
    print "Finish"
