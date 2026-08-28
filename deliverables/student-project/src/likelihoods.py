# Likelihood tables: table[category][state][outcome] = P(outcome | state).
# Outcome "Weaponized" is the Active-Admin-Control column from spec Section 8.1.
# State "Something Else" is the Dead / Experimental row from the spec tables.

LIKELIHOODS = {
    "Static Contract Permissions": {
        "Legitimate Project": {
            "Renounced": 0.70,
            "Centralized-Idle": 0.28,
            "Weaponized": 0.02,
        },
        "Liquidity Rug Pull": {
            "Renounced": 0.30,
            "Centralized-Idle": 0.40,
            "Weaponized": 0.30,
        },
        "Token Dump Rug Pull": {
            "Renounced": 0.50,
            "Centralized-Idle": 0.45,
            "Weaponized": 0.05,
        },
        "Honeypot": {
            "Renounced": 0.05,
            "Centralized-Idle": 0.15,
            "Weaponized": 0.80,
        },
        "Minting Abuse": {
            "Renounced": 0.10,
            "Centralized-Idle": 0.40,
            "Weaponized": 0.50,
        },
        "Fee/Tax Rug Pull": {
            "Renounced": 0.10,
            "Centralized-Idle": 0.30,
            "Weaponized": 0.60,
        },
        "Something Else": {
            "Renounced": 0.60,
            "Centralized-Idle": 0.35,
            "Weaponized": 0.05,
        },
    },
    "Token Supply & Minting Mechanics": {
        "Legitimate Project": {
            "Hard-Capped": 0.85,
            "Potential-Dilution": 0.14,
            "Active-Mint-Abuse": 0.01,
        },
        "Liquidity Rug Pull": {
            "Hard-Capped": 0.60,
            "Potential-Dilution": 0.35,
            "Active-Mint-Abuse": 0.05,
        },
        "Token Dump Rug Pull": {
            "Hard-Capped": 0.50,
            "Potential-Dilution": 0.40,
            "Active-Mint-Abuse": 0.10,
        },
        "Honeypot": {
            "Hard-Capped": 0.40,
            "Potential-Dilution": 0.40,
            "Active-Mint-Abuse": 0.20,
        },
        "Minting Abuse": {
            "Hard-Capped": 0.02,
            "Potential-Dilution": 0.08,
            "Active-Mint-Abuse": 0.90,
        },
        "Fee/Tax Rug Pull": {
            "Hard-Capped": 0.70,
            "Potential-Dilution": 0.25,
            "Active-Mint-Abuse": 0.05,
        },
        "Something Else": {
            "Hard-Capped": 0.65,
            "Potential-Dilution": 0.30,
            "Active-Mint-Abuse": 0.05,
        },
    },
    "Fee & Tax Configuration": {
        "Legitimate Project": {
            "Low-Immutable": 0.88,
            "Adjustable-Moderate": 0.11,
            "Honeypot-Tax": 0.01,
        },
        "Liquidity Rug Pull": {
            "Low-Immutable": 0.55,
            "Adjustable-Moderate": 0.35,
            "Honeypot-Tax": 0.10,
        },
        "Token Dump Rug Pull": {
            "Low-Immutable": 0.60,
            "Adjustable-Moderate": 0.35,
            "Honeypot-Tax": 0.05,
        },
        "Honeypot": {
            "Low-Immutable": 0.10,
            "Adjustable-Moderate": 0.20,
            "Honeypot-Tax": 0.70,
        },
        "Minting Abuse": {
            "Low-Immutable": 0.70,
            "Adjustable-Moderate": 0.25,
            "Honeypot-Tax": 0.05,
        },
        "Fee/Tax Rug Pull": {
            "Low-Immutable": 0.01,
            "Adjustable-Moderate": 0.09,
            "Honeypot-Tax": 0.90,
        },
        "Something Else": {
            "Low-Immutable": 0.80,
            "Adjustable-Moderate": 0.18,
            "Honeypot-Tax": 0.02,
        },
    },
    "Runtime Execution Simulation": {
        "Legitimate Project": {
            "Swaps-OK": 0.95,
            "High-Slippage": 0.04,
            "Execution-Reverted": 0.01,
        },
        "Liquidity Rug Pull": {
            "Swaps-OK": 0.80,
            "High-Slippage": 0.15,
            "Execution-Reverted": 0.05,
        },
        "Token Dump Rug Pull": {
            "Swaps-OK": 0.85,
            "High-Slippage": 0.12,
            "Execution-Reverted": 0.03,
        },
        "Honeypot": {
            "Swaps-OK": 0.01,
            "High-Slippage": 0.04,
            "Execution-Reverted": 0.95,
        },
        "Minting Abuse": {
            "Swaps-OK": 0.80,
            "High-Slippage": 0.15,
            "Execution-Reverted": 0.05,
        },
        "Fee/Tax Rug Pull": {
            "Swaps-OK": 0.10,
            "High-Slippage": 0.40,
            "Execution-Reverted": 0.50,
        },
        "Something Else": {
            "Swaps-OK": 0.75,
            "High-Slippage": 0.20,
            "Execution-Reverted": 0.05,
        },
    },
    "On-Chain Wallet Flows & Distribution": {
        "Legitimate Project": {
            "Distributed": 0.82,
            "Whale-Concentrated": 0.16,
            "Rug-Dumping": 0.02,
        },
        "Liquidity Rug Pull": {
            "Distributed": 0.05,
            "Whale-Concentrated": 0.25,
            "Rug-Dumping": 0.70,
        },
        "Token Dump Rug Pull": {
            "Distributed": 0.02,
            "Whale-Concentrated": 0.18,
            "Rug-Dumping": 0.80,
        },
        "Honeypot": {
            "Distributed": 0.20,
            "Whale-Concentrated": 0.50,
            "Rug-Dumping": 0.30,
        },
        "Minting Abuse": {
            "Distributed": 0.30,
            "Whale-Concentrated": 0.40,
            "Rug-Dumping": 0.30,
        },
        "Fee/Tax Rug Pull": {
            "Distributed": 0.40,
            "Whale-Concentrated": 0.40,
            "Rug-Dumping": 0.20,
        },
        "Something Else": {
            "Distributed": 0.45,
            "Whale-Concentrated": 0.45,
            "Rug-Dumping": 0.10,
        },
    },
    "Off-Chain & Social Viability": {
        "Legitimate Project": {
            "Maintained": 0.78,
            "Ghost-Town": 0.20,
            "Abandoned-Fraud": 0.02,
        },
        "Liquidity Rug Pull": {
            "Maintained": 0.25,
            "Ghost-Town": 0.35,
            "Abandoned-Fraud": 0.40,
        },
        "Token Dump Rug Pull": {
            "Maintained": 0.35,
            "Ghost-Town": 0.35,
            "Abandoned-Fraud": 0.30,
        },
        "Honeypot": {
            "Maintained": 0.15,
            "Ghost-Town": 0.25,
            "Abandoned-Fraud": 0.60,
        },
        "Minting Abuse": {
            "Maintained": 0.30,
            "Ghost-Town": 0.40,
            "Abandoned-Fraud": 0.30,
        },
        "Fee/Tax Rug Pull": {
            "Maintained": 0.30,
            "Ghost-Town": 0.40,
            "Abandoned-Fraud": 0.30,
        },
        "Something Else": {
            "Maintained": 0.02,
            "Ghost-Town": 0.88,
            "Abandoned-Fraud": 0.10,
        },
    },
}


def get_likelihoods():
    return LIKELIHOODS
