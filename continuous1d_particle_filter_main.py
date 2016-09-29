# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:07:10 2016

@author: Fujiichang
"""

import matplotlib.pyplot as plt
import continuous1d_particle_filter
import bayes_filter
import continuous1d_simulator


def show_particle_distribution(particle, s, determined_s, title,
                               ylabel="density"):
    plt.plot(s, 0.2, 'r*', markersize=20)
    plt.plot(determined_s, 0.2, 'o', markersize=20)
    plt.hist(particle, bins=20, normed=True, histtype='stepfilled')
    plt.title(title)
    plt.xlabel("state")
    plt.ylabel(ylabel)
    plt.xlim(-1, 5)
    plt.ylim(0, 2)
    plt.show()

if __name__ == "__main__":
    std_a = 0.3
    std_o = 0.3
    var_a = std_a ** 2
    var_o = std_o ** 2
    eps = 0.3
    o_log = []
    determined_s_log = []
    a_log = []
    actual_s_log = []
    actual_s_log.append(0)
    estimator = continuous1d_particle_filter.Continuous1dParticlefilter(
        var_a, var_o)
    simulator = continuous1d_simulator.Continuous1dSimulator(
        var_a, var_o)
    goals = [4, 0]
    controller = continuous1d_particle_filter.Continuous1dControllor(goals,
                                                                     eps)
    particle_num = 1000
    w_particle = particle_num * [0]
    w_particle[0] = 1
    particle = particle_num * [0]
    s = 0
    t = 0

    while True:
        print "step:", t, "##########################"
        o = simulator.get_o()
        o_log.append(o[0])
        print "o =", o
        particle = estimator.update_p_s(particle, o)
        determined_s = controller.determine_s(particle)
        determined_s_log.append(determined_s)
        show_particle_distribution(particle, s, determined_s,
                                   "after observation", "$bel(s_t)$")
        print "detemined_s =", determined_s

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
        particle = estimator.update_p_s_bar(particle, a)
        show_particle_distribution(particle, s, determined_s,
                                   "before observation",
                                   "$\overline{bel}(s_t)$")
    bayes_filter.show_actual_s__result(actual_s_log)
    bayes_filter.show_determined_s_result(determined_s_log)
    bayes_filter.print_result(o_log, actual_s_log,
                              determined_s_log, a_log, t)
    print "Finish"
