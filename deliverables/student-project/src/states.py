# The 7 hidden states in a fixed order, plus the starting belief.
# MALICIOUS_STATES is used by the per-state mid-loop BLOCK check and by
# the end-of-loop combined (malicious + Something Else) score.

STATES = [
    "Legitimate Project",
    "Liquidity Rug Pull",
    "Token Dump Rug Pull",
    "Honeypot",
    "Minting Abuse",
    "Fee/Tax Rug Pull",
    "Something Else",
]

MALICIOUS_STATES = [
    "Liquidity Rug Pull",
    "Token Dump Rug Pull",
    "Honeypot",
    "Minting Abuse",
    "Fee/Tax Rug Pull",
]

FIXED_PRIOR = {
    "Legitimate Project": 0.30,
    "Liquidity Rug Pull": 0.10,
    "Token Dump Rug Pull": 0.15,
    "Honeypot": 0.10,
    "Minting Abuse": 0.15,
    "Fee/Tax Rug Pull": 0.10,
    "Something Else": 0.10,
}

def get_fixed_prior():
    prior = {}
    for state in STATES:
        prior[state] = FIXED_PRIOR[state]
    return prior