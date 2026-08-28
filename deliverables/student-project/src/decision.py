import states

def check_mid_loop(belief):
    if belief["Legitimate Project"] >= 0.67:
        return "PROCEED"
        
    for state in states.MALICIOUS_STATES:
        if belief[state] >= 0.33:
            return "BLOCK"
            
    if belief["Something Else"] >= 0.33:
        return "BLOCK"
        
    return "CONTINUE"

def mid_loop_stopping_state(belief):
    if belief["Legitimate Project"] >= 0.67:
        return "Legitimate Project"
    for state in states.MALICIOUS_STATES:
        if belief[state] >= 0.33:
            return state
    if belief["Something Else"] >= 0.33:
        return "Something Else"
    return "None"

def check_end_of_loop(belief):
    combined = combined_malicious_and_something_else(belief)
    if combined > 0.67:
        return "BLOCK"
    return "ESCALATE"

def combined_malicious_and_something_else(belief):
    total = 0.0
    for state in states.MALICIOUS_STATES:
        total = total + belief[state]
    total = total + belief["Something Else"]
    return total

def highest_individual_state(belief):
    best_state = states.STATES[0]
    best_val = belief[best_state]
    for state in states.STATES:
        if belief[state] > best_val:
            best_val = belief[state]
            best_state = state
    return best_state

def confidence_score(belief, verdict):
    if verdict == "PROCEED":
        return belief["Legitimate Project"]
        
    if verdict == "BLOCK":
        state = mid_loop_stopping_state(belief)
        if state != "None":
            return belief[state]
        return combined_malicious_and_something_else(belief)
        
    if verdict == "ESCALATE":
        return combined_malicious_and_something_else(belief)
        
    return 0.0