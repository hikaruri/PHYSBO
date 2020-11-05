from __future__ import print_function

from itertools import product

import numpy as np
import pytest

physbo = pytest.importorskip("physbo")


def f(x):
    return -np.sum((x - 0.5) ** 2)


class simulator:
    def __init__(self):
        self.nslice = 11
        self.dim = 2
        self.N = self.nslice ** self.dim
        self.X = np.zeros((self.N, self.dim))
        for i, x in enumerate(
            product(np.linspace(0.0, 1.0, self.nslice), repeat=self.dim)
        ):
            self.X[i, :] = list(x)

    def __call__(self, action):
        return f(self.X[action, :])


def test_random_search():
    sim = simulator()
    policy = physbo.search.discrete.policy(test_X=sim.X)
    policy.set_seed(12345)
    nsearch = 20
    res = policy.random_search(max_num_probes=nsearch, simulator=sim)
    best_fx, best_action = res.export_all_sequence_best_fx()
    print(best_fx[-1])
    print(best_action[-1])
    assert best_fx[-1] == pytest.approx(-0.01, abs=0.001)
    assert best_action[-1] == 61


def test_bayes_search():
    sim = simulator()
    nrand = 10
    nsearch = 5
    policy = physbo.search.discrete.policy(test_X=sim.X)
    policy.set_seed(12345)
    res = policy.random_search(max_num_probes=nrand, simulator=sim)
    res = policy.bayes_search(max_num_probes=nsearch, simulator=sim, score="TS")
    best_fx, best_action = res.export_all_sequence_best_fx()
    print(best_fx)
    print(best_action)
    assert best_fx[-1] == pytest.approx(0.0, abs=0.001)
    assert best_action[-1] == 60
