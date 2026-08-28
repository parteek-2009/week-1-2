# Multi-class Bayesian update (spec Section 5). Pure function, no I/O.


def update(belief, category, observed_outcome, likelihoods):
    unnormalized = {}
    total = 0.0

    for state in belief:
        likelihood = likelihoods[category][state][observed_outcome]
        value = likelihood * belief[state]
        unnormalized[state] = value
        total = total + value

    new_belief = {}
    for state in belief:
        new_belief[state] = unnormalized[state] / total

    return new_belief
