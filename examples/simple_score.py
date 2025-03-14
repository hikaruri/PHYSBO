import numpy as np
import physbo

# Make a set of candidates, test_X
D = 3  # The number of params (the dimension of parameter space)
N = 100  # The number of candidates
test_X = np.random.randn(N, D)  # Generated from Gaussian
score = "EI"


def simulator(actions: np.ndarray) -> np.ndarray:
    """Objective function

    Quadratic function, -Σ_i x_i^2
    Recieves an array of actions (indices of candidates) and returns the corresponding results as an array
    """
    return -np.sum(test_X[actions, :] ** 2, axis=1)


policy = physbo.search.discrete.policy(test_X)

# Random search (10 times)
policy.random_search(max_num_probes=10, simulator=simulator)

# Bayesian search (100 times)
#   score function (acquisition function): expectation of improvement (EI)
policy.bayes_search(max_num_probes=0, simulator=simulator, score=score)

print("Mean values of prediction")
scores = policy.get_post_fmean(xs=test_X)
print(scores)
print()

print("Standard derivations of prediction")
scores = policy.get_post_fcov(xs=test_X)
print(np.sqrt(scores))
print()

print("Acquisition function")
scores = policy.get_score(mode=score, xs=test_X)
print(scores)
