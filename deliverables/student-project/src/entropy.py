# Shannon entropy of a belief, and expected entropy if a category were run next.

import math

import bayes
import evidence
import voi


def shannon_entropy(belief):
    total = 0.0
    for state in belief:
        p = belief[state]
        if p == 0.0:
            continue
        total = total + p * math.log2(p)
    return -total


def expected_entropy_if_run(belief, category, likelihoods):
    outcomes = evidence.get_outcomes(category)
    expected = 0.0
    for outcome in outcomes:
        outcome_prob = voi.probability_of_outcome(
            belief, category, outcome, likelihoods
        )
        posterior = bayes.update(belief, category, outcome, likelihoods)
        posterior_entropy = shannon_entropy(posterior)
        expected = expected + outcome_prob * posterior_entropy
    return expected
