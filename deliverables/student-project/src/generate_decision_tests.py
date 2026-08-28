import json
import os

OUTPUT_DIR = "decision_scenarios"

decision_test_cases = [
    # 1. Mid-Loop PROCEED: Legitimate Project >= 67%
    # First test (Static Contract Permissions -> Renounced) pushes Legitimate from 30% to ~55.8%,
    # second cheap test (Token Supply -> Hard-Capped) pushes Legitimate past 67%.
    {
        "filename": "policy_01_mid_loop_proceed.json",
        "data": {
            "token_name": "PolicyTest_MidLoopProceed",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    # 2. Mid-Loop BLOCK: Single Malicious State (Honeypot >= 33%)
    # Cheap test (Static Contract Permissions -> Weaponized) immediately spikes Honeypot to ~48%, crossing 33%.
    {
        "filename": "policy_02_mid_loop_block_honeypot.json",
        "data": {
            "token_name": "PolicyTest_HoneypotBlock",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    # 3. Mid-Loop BLOCK: Single Malicious State (Minting Abuse >= 33%)
    # Token Supply -> Active-Mint-Abuse immediately spikes Minting Abuse to ~76.7%, crossing 33%.
    {
        "filename": "policy_03_mid_loop_block_mint_abuse.json",
        "data": {
            "token_name": "PolicyTest_MintAbuseBlock",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Active-Mint-Abuse",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    # 4. Mid-Loop BLOCK: Single Malicious State (Fee/Tax Rug Pull >= 33%)
    # Fee & Tax Configuration -> Honeypot-Tax immediately spikes Fee/Tax Rug Pull & Honeypot past 33%.
    {
        "filename": "policy_04_mid_loop_block_fee_tax_rug.json",
        "data": {
            "token_name": "PolicyTest_FeeTaxRugBlock",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Honeypot-Tax",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    # 5. Mid-Loop BLOCK: Single Malicious State (Token Dump Rug Pull >= 33%)
    # Wallet Flows -> Rug-Dumping spikes Token Dump Rug Pull to ~48.8%, crossing 33%.
    {
        "filename": "policy_05_mid_loop_block_token_dump.json",
        "data": {
            "token_name": "PolicyTest_TokenDumpBlock",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    # 6. Mid-Loop BLOCK: Single Malicious State (Liquidity Rug Pull >= 33%)
    # Combination of Centralized-Idle and Rug-Dumping pushes Liquidity Rug Pull past 33%.
    {
        "filename": "policy_06_mid_loop_block_liquidity_rug.json",
        "data": {
            "token_name": "PolicyTest_LiquidityRugBlock",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    # 7. Mid-Loop BLOCK: Single Non-Malicious Target State (Something Else >= 33%)
    # Social Viability -> Ghost-Town spikes Something Else from 10% to ~43.8%, triggering 33% BLOCK.
    {
        "filename": "policy_07_mid_loop_block_something_else.json",
        "data": {
            "token_name": "PolicyTest_SomethingElseBlock",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    # 8. Mid-Loop Order/Precedence Test
    # Tests that Legitimate Project >= 67% returns PROCEED cleanly without evaluating subsequent malicious branches.
    {
        "filename": "policy_08_precedence_legit_first.json",
        "data": {
            "token_name": "PolicyTest_PrecedenceCheck",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    # 9. End-of-Loop Check: Combined Malicious + Something Else > 67%
    # Blends mild yellow flags across all 6 categories so no single state hits 33% mid-loop.
    # Forces all 6 tests to run, then checks combined risk score > 67% at the end.
    {
        "filename": "policy_09_end_of_loop_block.json",
        "data": {
            "token_name": "PolicyTest_EndOfLoopBlock",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Potential-Dilution",
            "Fee & Tax Configuration": "Adjustable-Moderate",
            "Runtime Execution Simulation": "High-Slippage",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    # 10. End-of-Loop Check: Combined Malicious + Something Else <= 67% -> ESCALATE
    # Carefully balanced mixed signals (some clean, some moderate) so no state hits mid-loop thresholds,
    # and total combined risk ends below 67%, triggering the ESCALATE fallback.
    {
        "filename": "policy_10_end_of_loop_escalate.json",
        "data": {
            "token_name": "PolicyTest_EndOfLoopEscalate",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Potential-Dilution",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Maintained"
        }
    }
]

def generate_decision_tests():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    for tc in decision_test_cases:
        path = os.path.join(OUTPUT_DIR, tc["filename"])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(tc["data"], f, indent=2)
            f.write("\n")

    print(f"Successfully generated {len(decision_test_cases)} policy test cases in '{OUTPUT_DIR}/'.")

if __name__ == "__main__":
    generate_decision_tests()