# Value-of-Information selection (spec Section 4). Simulation only.
# This module must never import or call evidence_input.py.

import math

import bayes
import evidence


def kl_divergence(p, q):
    total = 0.0
    for state in p:
        p_i = p[state]
        q_i = q[state]
        if p_i == 0.0:
            continue
        total = total + p_i * math.log2(p_i / q_i)
    return total


def mixture_distribution(p, q):
    mixed = {}
    for state in p:
        mixed[state] = 0.5 * p[state] + 0.5 * q[state]
    return mixed


def js_divergence(current_belief, posterior_belief):
    mixed = mixture_distribution(current_belief, posterior_belief)
    from_current = kl_divergence(current_belief, mixed)
    from_posterior = kl_divergence(posterior_belief, mixed)
    return 0.5 * from_current + 0.5 * from_posterior


def probability_of_outcome(belief, category, outcome, likelihoods):
    total = 0.0
    for state in belief:
        likelihood = likelihoods[category][state][outcome]
        total = total + likelihood * belief[state]
    return total


def divergence_for_one_outcome(belief, category, outcome, likelihoods):
    posterior = bayes.update(belief, category, outcome, likelihoods)
    return js_divergence(belief, posterior)


def expected_information_gain(belief, category, likelihoods):
    outcomes = evidence.get_outcomes(category)
    eig = 0.0
    for outcome in outcomes:
        outcome_prob = probability_of_outcome(belief, category, outcome, likelihoods)
        divergence = divergence_for_one_outcome(belief, category, outcome, likelihoods)
        eig = eig + outcome_prob * divergence
    return eig


def value_per_rupee(belief, category, likelihoods):
    eig = expected_information_gain(belief, category, likelihoods)
    cost = evidence.get_cost(category)
    return eig / cost


def select_best_category(belief, remaining_categories, likelihoods):
    best_category = remaining_categories[0]
    best_value = value_per_rupee(belief, best_category, likelihoods)

    for category in remaining_categories:
        value = value_per_rupee(belief, category, likelihoods)
        if value > best_value:
            best_value = value
            best_category = category

    return best_category
