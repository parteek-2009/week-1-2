# Entry point: run the VoI loop for one or more scenario files and write results.

import json
import os
import sys

import bayes
import decision
import entropy
import evidence
import evidence_input
import likelihoods
import states
import voi


RESULTS_DIR = "results"


def copy_belief(belief):
    copied = {}
    for state in states.STATES:
        copied[state] = belief[state]
    return copied


def list_scenario_paths(path_argument):
    if os.path.isfile(path_argument):
        return [path_argument]

    if os.path.isdir(path_argument):
        names = os.listdir(path_argument)
        names.sort()
        paths = []
        for name in names:
            if name.endswith(".json"):
                full = os.path.join(path_argument, name)
                if os.path.isfile(full):
                    paths.append(full)
        return paths

    return []


def result_filename(scenario_path):
    base = os.path.basename(scenario_path)
    name_without_ext = os.path.splitext(base)[0]
    return name_without_ext + "_result.json"


def percent_text(probability):
    return str(round(probability * 100, 1)) + "%"


def remaining_entropy_entries(belief, remaining_categories, likelihood_tables):
    entries = []
    for category in remaining_categories:
        entry = {
            "category": category,
            "cost_inr": evidence.get_cost(category),
            "expected_entropy_if_run": entropy.expected_entropy_if_run(
                belief, category, likelihood_tables
            ),
        }
        entries.append(entry)
    return entries


def run_one_scenario(scenario_path):
    loaded = evidence_input.load_scenario(scenario_path)
    token_name = evidence_input.get_token_name(loaded)
    likelihood_tables = likelihoods.get_likelihoods()

    belief = states.get_fixed_prior()
    remaining_categories = evidence.get_categories()
    checked_categories = []
    running_cost_spent = 0
    reasoning = []

    while True:
        category = voi.select_best_category(
            belief, remaining_categories, likelihood_tables
        )
        value = voi.value_per_rupee(belief, category, likelihood_tables)
        cost = evidence.get_cost(category)

        if len(checked_categories) == 0:
            count = len(remaining_categories)
            reasoning.append(
                "Selected '"
                + category
                + "' first: highest value-per-rupee among all "
                + str(count)
                + " categories (value-per-rupee "
                + str(round(value, 4))
                + ", cost "
                + str(cost)
                + " INR)."
            )
        else:
            count = len(remaining_categories)
            reasoning.append(
                "Selected '"
                + category
                + "' next: highest value-per-rupee among the remaining "
                + str(count)
                + " categories (value-per-rupee "
                + str(round(value, 4))
                + ", cost "
                + str(cost)
                + " INR)."
            )

        outcome = evidence_input.get_outcome(loaded, category)
        belief = bayes.update(belief, category, outcome, likelihood_tables)

        remaining_list = []
        for name in remaining_categories:
            if name != category:
                remaining_list.append(name)
        remaining_categories = remaining_list

        running_cost_spent = running_cost_spent + cost
        checked_categories.append(
            {
                "category": category,
                "observed_outcome": outcome,
                "cost_inr": cost,
                "belief_after": copy_belief(belief),
            }
        )

        reasoning.append(
            "Observed outcome '"
            + outcome
            + "'. Updated belief accordingly."
        )

        verdict = decision.check_mid_loop(belief)
        stopping_state = decision.mid_loop_stopping_state(belief)

        if verdict == "PROCEED":
            reasoning.append(
                "State "
                + stopping_state
                + " reached "
                + percent_text(belief[stopping_state])
                + " (>= 67%) — stopping loop, verdict PROCEED."
            )
            break

        if verdict == "BLOCK":
            reasoning.append(
                "State "
                + stopping_state
                + " reached "
                + percent_text(belief[stopping_state])
                + " (>= 33%) — stopping loop, verdict BLOCK."
            )
            break

        if len(remaining_categories) == 0:
            combined = decision.combined_malicious_and_something_else(belief)
            verdict = decision.check_end_of_loop(belief)
            if verdict == "BLOCK":
                reasoning.append(
                    "All categories checked. Combined malicious+something-else reached "
                    + percent_text(combined)
                    + " (> 67%) — verdict BLOCK."
                )
            else:
                reasoning.append(
                    "All categories checked. Combined malicious+something-else reached "
                    + percent_text(combined)
                    + " (not above 67%) — verdict ESCALATE."
                )
            break

        highest_state = decision.highest_individual_state(belief)
        reasoning.append(
            "No single state reached 67% (highest was "
            + highest_state
            + " at "
            + percent_text(belief[highest_state])
            + ") — continuing the loop."
        )

    result = {
        "token_name": token_name,
        "final_answer": verdict,
        "confidence_score": decision.confidence_score(belief, verdict),
        "final_belief": copy_belief(belief),
        "checked_categories": checked_categories,
        "unchecked_categories": remaining_entropy_entries(
            belief, remaining_categories, likelihood_tables
        ),
        "total_cost_inr": running_cost_spent,
        "reasoning": reasoning,
    }
    return result


def write_result(scenario_path, result):
    if not os.path.isdir(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    out_path = os.path.join(RESULTS_DIR, result_filename(scenario_path))
    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)
        file.write("\n")
    return out_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <scenario.json or folder>")
        sys.exit(1)

    path_argument = sys.argv[1]
    scenario_paths = list_scenario_paths(path_argument)

    if len(scenario_paths) == 0:
        print("No scenario JSON files found at: " + path_argument)
        sys.exit(1)

    for scenario_path in scenario_paths:
        result = run_one_scenario(scenario_path)
        out_path = write_result(scenario_path, result)
        print(json.dumps(result, indent=2))
        print("Wrote " + out_path)


if __name__ == "__main__":
    main()