# The 6 evidence categories, their 3 outcome labels each, and INR costs.

CATEGORIES = [
    "Static Contract Permissions",
    "Token Supply & Minting Mechanics",
    "Fee & Tax Configuration",
    "Runtime Execution Simulation",
    "On-Chain Wallet Flows & Distribution",
    "Off-Chain & Social Viability",
]

OUTCOMES = {
    "Static Contract Permissions": [
        "Renounced",
        "Centralized-Idle",
        "Weaponized",
    ],
    "Token Supply & Minting Mechanics": [
        "Hard-Capped",
        "Potential-Dilution",
        "Active-Mint-Abuse",
    ],
    "Fee & Tax Configuration": [
        "Low-Immutable",
        "Adjustable-Moderate",
        "Honeypot-Tax",
    ],
    "Runtime Execution Simulation": [
        "Swaps-OK",
        "High-Slippage",
        "Execution-Reverted",
    ],
    "On-Chain Wallet Flows & Distribution": [
        "Distributed",
        "Whale-Concentrated",
        "Rug-Dumping",
    ],
    "Off-Chain & Social Viability": [
        "Maintained",
        "Ghost-Town",
        "Abandoned-Fraud",
    ],
}

COSTS = {
    "Static Contract Permissions": 10,
    "Token Supply & Minting Mechanics": 10,
    "Fee & Tax Configuration": 10,
    "Off-Chain & Social Viability": 40,
    "On-Chain Wallet Flows & Distribution": 80,
    "Runtime Execution Simulation": 150,
}


def get_categories():
    names = []
    for name in CATEGORIES:
        names.append(name)
    return names


def get_outcomes(category):
    labels = []
    for label in OUTCOMES[category]:
        labels.append(label)
    return labels


def get_cost(category):
    return COSTS[category]
