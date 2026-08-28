import json
import os

SCENARIOS_DIR = "scenarios"

test_cases = [
    # --- BUCKET 1: Legitimate Archetypes (1-10) ---
    {
        "filename": "test_01_legit_benchmark.json",
        "data": {
            "token_name": "BenchmarkLegitToken",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_02_legit_centralized_idle.json",
        "data": {
            "token_name": "IdleOwnerCoin",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_03_legit_potential_dilution.json",
        "data": {
            "token_name": "DaoMintableToken",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Potential-Dilution",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_04_legit_adjustable_tax.json",
        "data": {
            "token_name": "FlexibleTaxDeFi",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Adjustable-Moderate",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_05_legit_high_slippage.json",
        "data": {
            "token_name": "LowLiquidityLegit",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "High-Slippage",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_06_legit_whale_concentrated.json",
        "data": {
            "token_name": "VestedFounderToken",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_07_legit_quiet_socials.json",
        "data": {
            "token_name": "QuietDevProtocol",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_08_legit_dao_utility.json",
        "data": {
            "token_name": "GovernanceUtility",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Potential-Dilution",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_09_legit_meme_community.json",
        "data": {
            "token_name": "CleanMemeCoin",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "High-Slippage",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_10_legit_corporate_web3.json",
        "data": {
            "token_name": "EnterpriseChain",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Adjustable-Moderate",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Maintained"
        }
    },

    # --- BUCKET 2: Honeypot Exploits (11-20) ---
    {
        "filename": "test_11_honeypot_classic_reverted.json",
        "data": {
            "token_name": "MoonRocketHoneypot",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Honeypot-Tax",
            "Runtime Execution Simulation": "Execution-Reverted",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },
    {
        "filename": "test_12_honeypot_stealth_reverted.json",
        "data": {
            "token_name": "StealthTrapToken",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Execution-Reverted",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },
    {
        "filename": "test_13_honeypot_extreme_tax.json",
        "data": {
            "token_name": "NinetyNinePercentTax",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Honeypot-Tax",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_14_honeypot_active_admin_revert.json",
        "data": {
            "token_name": "AdminBlockedSell",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Potential-Dilution",
            "Fee & Tax Configuration": "Adjustable-Moderate",
            "Runtime Execution Simulation": "Execution-Reverted",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },
    {
        "filename": "test_15_honeypot_fake_hype.json",
        "data": {
            "token_name": "HypeHoneypot100x",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Execution-Reverted",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_16_honeypot_slippage_trap.json",
        "data": {
            "token_name": "SlippageDrainer",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Honeypot-Tax",
            "Runtime Execution Simulation": "High-Slippage",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },
    {
        "filename": "test_17_honeypot_rug_combo.json",
        "data": {
            "token_name": "HoneypotDumpCombo",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Potential-Dilution",
            "Fee & Tax Configuration": "Honeypot-Tax",
            "Runtime Execution Simulation": "Execution-Reverted",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },
    {
        "filename": "test_18_honeypot_mint_combo.json",
        "data": {
            "token_name": "InfiniteMintHoneypot",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Active-Mint-Abuse",
            "Fee & Tax Configuration": "Honeypot-Tax",
            "Runtime Execution Simulation": "Execution-Reverted",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },
    {
        "filename": "test_19_honeypot_dormant_contract.json",
        "data": {
            "token_name": "SleepingHoneypot",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Honeypot-Tax",
            "Runtime Execution Simulation": "Execution-Reverted",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_20_honeypot_fake_renounced.json",
        "data": {
            "token_name": "FakeRenouncedTrap",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Honeypot-Tax",
            "Runtime Execution Simulation": "Execution-Reverted",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },

    # --- BUCKET 3: Rug Pulls & Mint Abuses (21-30) ---
    {
        "filename": "test_21_liq_rug_drained.json",
        "data": {
            "token_name": "DrainedPoolCoin",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },
    {
        "filename": "test_22_token_dump_insider.json",
        "data": {
            "token_name": "InsiderDumpExpress",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_23_mint_abuse_hyperinflation.json",
        "data": {
            "token_name": "InfinitePrinterToken",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Active-Mint-Abuse",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },
    {
        "filename": "test_24_mint_abuse_stealth.json",
        "data": {
            "token_name": "StealthPrinterDeFi",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Active-Mint-Abuse",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_25_tax_rug_fee_spike.json",
        "data": {
            "token_name": "SpikeTaxScam",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Honeypot-Tax",
            "Runtime Execution Simulation": "High-Slippage",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },
    {
        "filename": "test_26_liq_rug_slow_bleed.json",
        "data": {
            "token_name": "SlowBleedProtocol",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Potential-Dilution",
            "Fee & Tax Configuration": "Adjustable-Moderate",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_27_token_dump_whale_exodus.json",
        "data": {
            "token_name": "WhaleDumpRun",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Potential-Dilution",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "High-Slippage",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },
    {
        "filename": "test_28_mint_abuse_unlimited.json",
        "data": {
            "token_name": "UnlimitedSupplyScam",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Active-Mint-Abuse",
            "Fee & Tax Configuration": "Adjustable-Moderate",
            "Runtime Execution Simulation": "High-Slippage",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_29_tax_rug_drain.json",
        "data": {
            "token_name": "TaxDrainNetwork",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Adjustable-Moderate",
            "Runtime Execution Simulation": "High-Slippage",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },
    {
        "filename": "test_30_liq_rug_active_admin.json",
        "data": {
            "token_name": "ActiveAdminRug",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "High-Slippage",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },

    # --- BUCKET 4: Mixed & Conflicting Signals (31-40) ---
    {
        "filename": "test_31_mixed_clean_contract_bad_wallet.json",
        "data": {
            "token_name": "CleanCodeBadWallets",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_32_mixed_weaponized_admin_clean_flows.json",
        "data": {
            "token_name": "ScaryAdminCleanFlows",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_33_mixed_active_mint_vibrant_social.json",
        "data": {
            "token_name": "HypedPrinterProject",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Active-Mint-Abuse",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_34_mixed_high_slippage_good_social.json",
        "data": {
            "token_name": "HighSlippageCommunity",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "High-Slippage",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_35_mixed_honeypot_tax_clean_swaps.json",
        "data": {
            "token_name": "HighTaxWorkingSwaps",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Honeypot-Tax",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_36_mixed_execution_reverted_clean_rest.json",
        "data": {
            "token_name": "BrokenContractCleanTeam",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Execution-Reverted",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_37_mixed_centralized_rug_dump.json",
        "data": {
            "token_name": "CentralizedDumpCoin",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_38_mixed_abandoned_social_clean_onchain.json",
        "data": {
            "token_name": "DeadSocialsCleanChain",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },
    {
        "filename": "test_39_mixed_potential_dilution_high_slippage.json",
        "data": {
            "token_name": "DilutionSlippageMixed",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Potential-Dilution",
            "Fee & Tax Configuration": "Adjustable-Moderate",
            "Runtime Execution Simulation": "High-Slippage",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_40_mixed_weaponized_idle_tax.json",
        "data": {
            "token_name": "WeaponizedIdleTax",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Adjustable-Moderate",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },

    # --- BUCKET 5: Ghost Town & Boundary Cases (41-50) ---
    {
        "filename": "test_41_dead_ghost_project.json",
        "data": {
            "token_name": "GhostTownProject",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_42_dead_experimental_dev.json",
        "data": {
            "token_name": "ExperimentalTestnetCoin",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Potential-Dilution",
            "Fee & Tax Configuration": "Adjustable-Moderate",
            "Runtime Execution Simulation": "High-Slippage",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_43_edge_single_flag_mint.json",
        "data": {
            "token_name": "SingleFlagActiveMint",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Active-Mint-Abuse",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_44_edge_single_flag_tax.json",
        "data": {
            "token_name": "SingleFlagPredatoryTax",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Honeypot-Tax",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_45_edge_single_flag_execution.json",
        "data": {
            "token_name": "SingleFlagReverted",
            "Static Contract Permissions": "Renounced",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Execution-Reverted",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_46_edge_single_flag_permissions.json",
        "data": {
            "token_name": "SingleFlagWeaponizedAdmin",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Hard-Capped",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_47_edge_two_yellow_flags.json",
        "data": {
            "token_name": "TwoYellowFlagsToken",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Potential-Dilution",
            "Fee & Tax Configuration": "Low-Immutable",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Distributed",
            "Off-Chain & Social Viability": "Maintained"
        }
    },
    {
        "filename": "test_48_edge_three_yellow_flags.json",
        "data": {
            "token_name": "ThreeYellowFlagsToken",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Potential-Dilution",
            "Fee & Tax Configuration": "Adjustable-Moderate",
            "Runtime Execution Simulation": "Swaps-OK",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    },
    {
        "filename": "test_49_edge_all_worst_outcomes.json",
        "data": {
            "token_name": "AbsoluteWorstScam",
            "Static Contract Permissions": "Weaponized",
            "Token Supply & Minting Mechanics": "Active-Mint-Abuse",
            "Fee & Tax Configuration": "Honeypot-Tax",
            "Runtime Execution Simulation": "Execution-Reverted",
            "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
            "Off-Chain & Social Viability": "Abandoned-Fraud"
        }
    },
    {
        "filename": "test_50_edge_all_middle_outcomes.json",
        "data": {
            "token_name": "AmbiguousMiddleToken",
            "Static Contract Permissions": "Centralized-Idle",
            "Token Supply & Minting Mechanics": "Potential-Dilution",
            "Fee & Tax Configuration": "Adjustable-Moderate",
            "Runtime Execution Simulation": "High-Slippage",
            "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
            "Off-Chain & Social Viability": "Ghost-Town"
        }
    }
]

def generate_scenarios():
    if not os.path.exists(SCENARIOS_DIR):
        os.makedirs(SCENARIOS_DIR)
        print(f"Created directory: {SCENARIOS_DIR}")

    for tc in test_cases:
        path = os.path.join(SCENARIOS_DIR, tc["filename"])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(tc["data"], f, indent=2)
            f.write("\n")
            
    print(f"Successfully wrote {len(test_cases)} test scenario JSON files into '{SCENARIOS_DIR}/'.")

if __name__ == "__main__":
    generate_scenarios()