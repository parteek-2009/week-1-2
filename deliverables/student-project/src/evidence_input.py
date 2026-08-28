# Loads one scenario JSON file. Callers may only look up one category at a time.

import json

_evidence_by_id = {}
_next_id = 0


def load_scenario(path):
    global _next_id

    with open(path, encoding="utf-8") as file:
        data = json.load(file)

    token_name = data["token_name"]

    evidence_only = {}
    for key in data:
        if key != "token_name":
            evidence_only[key] = data[key]

    _next_id = _next_id + 1
    handle_id = _next_id
    _evidence_by_id[handle_id] = evidence_only

    return {"id": handle_id, "token_name": token_name}


def get_token_name(loaded_scenario):
    return loaded_scenario["token_name"]


def get_outcome(loaded_scenario, category):
    stored = _evidence_by_id[loaded_scenario["id"]]
    return stored[category]
