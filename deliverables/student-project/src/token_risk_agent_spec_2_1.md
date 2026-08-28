# Cost-Optimized Multi-Class Bayesian Token Risk Agent
## Technical Specification

---

## 1. System Overview

This specification defines a sequential, multi-class Bayesian belief network for evaluating Web3 cryptocurrency tokens for potential exploits, scams, and rug pulls.

The system combines three core mechanisms:

- A **Value of Information (VoI) stopping rule** that greedily selects the most cost-efficient test at each step
- **Six independent evidence categories**, each with mutually exclusive, domain-specific classifications
- A **cost-optimized decision threshold**, derived from a 10,000 INR investment model, that converts belief into a block/proceed decision

---

## 2. Hidden States (Target Clusters)

The agent maintains a probability distribution across **7 mutually exclusive hidden states**, summing to 1.0:

| # | Hidden State | Description |
|---|---|---|
| 1 | Legitimate Project | Token behaves as advertised |
| 2 | Liquidity Rug Pull | Liquidity pool drained by insiders |
| 3 | Token Dump Rug Pull | Insiders dump held supply on the market |
| 4 | Honeypot | Buyers can enter but not exit (sell-blocked) |
| 5 | Minting Abuse | Supply inflated post-launch to dilute holders |
| 6 | Fee/Tax Rug Pull | Extractive fee/tax logic drains value on trade |
| 7 | Something Else | Dead project, experimental, or otherwise inactive |

---

## 3. Evidence Categories & Classifications

To prevent double-counting and overlapping logic, all tests are strictly partitioned into **six independent categories**. Each yields one of three unique, mutually exclusive classifications.

### Category 1 — Static Contract Permissions
*("The Control Panel")*

| Classification | Meaning |
|---|---|
| Renounced / Decentralized | Ownership renounced; no privileged control |
| Privileged / Centralized-Idle | Owner retains control but has not exercised it |
| Weaponized / Active-Admin-Control | Owner actively exercises privileged control |

### Category 2 — Token Supply & Minting Mechanics
*("The Ledger Rules")*

| Classification | Meaning |
|---|---|
| Fixed / Hard-Capped | Supply is capped; minting disabled |
| Unminted / Potential-Dilution | Minting function exists but is unused |
| Inflated / Active-Mint-Abuse | Minting function actively used to inflate supply |

### Category 3 — Fee & Tax Configuration
*("The Extraction Rules")*

| Classification | Meaning |
|---|---|
| Transparent / Low-Immutable | Fees are low and fixed |
| Flexible / Adjustable-Moderate | Fees can be changed within a moderate range |
| Predatory / Honeypot-Tax | Fees can be set to extreme/extractive levels |

### Category 4 — Runtime Execution Simulation
*("The Sandbox Stress-Test")*

| Classification | Meaning |
|---|---|
| Fluid / Swaps-Successfully | Buy and sell simulate cleanly |
| Frictional / High-Slippage-Warning | Swaps succeed but with high slippage |
| Deadlocked / Execution-Reverted | Sell transactions revert (cannot exit) |

### Category 5 — On-Chain Wallet Flows & Distribution
*("The Whale & Insider Footprint")*

| Classification | Meaning |
|---|---|
| Organic / Widely-Distributed | Token holdings spread across many wallets |
| Clustered / Whale-Concentrated | Holdings concentrated in a few wallets |
| Coordinated / Rug-Pull-Dumping | Coordinated sell/dump pattern detected |

### Category 6 — Off-Chain & Social Viability
*("The Project Pulse")*

| Classification | Meaning |
|---|---|
| Vibrant / Maintained-Active | Active social presence and development |
| Stale / Ghost-Town | Minimal activity; project appears dormant |
| Fabricated / Abandoned-Fraud | Evidence of fake engagement or abandonment |

---

## 4. Evidence Selection Algorithm (Value of Information)

At each step, the agent selects the single most informative-per-rupee test from the remaining, un-run evidence categories:

1. **Simulate outcomes** — For each remaining category, simulate all possible unique classification outcomes.
2. **Compute expected posteriors** — Calculate the expected posterior probability distribution for each outcome using the multi-class Bayesian update (Section 5).
3. **Measure information gain** — Quantify the shift from current beliefs to each expected posterior using **Jensen-Shannon Divergence (D_JS)**.
4. **Weight by likelihood** — Weight each outcome's divergence by its probability of occurring to obtain the **Expected Information Gain (EIG)**.
5. **Normalize by cost** — Compute Value per Rupee for each remaining category:

$$
\text{Value/Rupee} = \frac{\text{Expected Information Gain (JS Divergence)}}{\text{Cost of Test (INR)}}
$$

6. **Select greedily** — Run the single category with the highest Value per Rupee.
7. **Update and loop** — Update the 7-state belief distribution with the real observed result (Section 5). If uncertainty remains and cumulative risk is undecided (Section 6), return to step 1.

---

## 5. Multi-Class Bayesian Update Engine

When evidence $E$ is observed from a test, beliefs are updated across all 7 hidden states $H_i$ via Bayes' theorem:

$$
P(H_i \mid E) = \frac{P(E \mid H_i) \cdot P(H_i)}{\sum_{j} P(E \mid H_j) \cdot P(H_j)}
$$

Where:
- $P(H_i)$ — prior probability of hidden state $i$ (before this evidence)
- $P(E \mid H_i)$ — likelihood of observing evidence $E$ given hidden state $i$ (from the likelihood tables in Section 8)
- $P(H_i \mid E)$ — posterior probability of hidden state $i$ (after this evidence)

---

## 6. Financial Cost Model & Decision Threshold

### 6.1 Investment Parameters

| Parameter | Value | Definition |
|---|---|---|
| Capital at Risk (False Negative cost) | 10,000 INR | Full loss if a malicious token is wrongly approved |
| Opportunity Loss (False Positive cost) | 5,000 INR | Missed 50% return if a legitimate token is wrongly blocked |

### 6.2 Optimal Threshold Derivation

$$
T = \frac{\text{Cost of False Positive}}{\text{Cost of False Positive} + \text{Cost of False Negative}} = \frac{5000}{5000 + 10000} = \frac{1}{3} \approx 0.33
$$

### 6.3 Decision Rule

**Cumulative Risk Score** is defined as the sum of posterior probabilities across all five malicious states:

$$
\text{Risk Score} = P(\text{Liquidity Rug}) + P(\text{Token Dump}) + P(\text{Honeypot}) + P(\text{Minting Abuse}) + P(\text{Fee/Tax Rug})
$$

**Genuine Score** is its complement — the combined posterior across the two non-malicious states:

$$
\text{Genuine Score} = P(\text{Legitimate}) + P(\text{Dead / Experimental}) = 1 - \text{Risk Score}
$$

These two scores always sum to 1, so they express the same line from opposite sides:

| Condition | Equivalent Condition | Action |
|---|---|---|
| Risk Score ≥ 0.33 | Genuine Score ≤ 0.67 | **BLOCK** the trade |
| Risk Score < 0.33 | Genuine Score > 0.67 | **PROCEED** with the trade |

Section 7.2 uses the Genuine Score form of this rule mid-loop, and the Risk Score form at the end of the loop — but it is one threshold, not two.

---

## 7. Test Costs & Decision Policy

### 7.1 Evidence Costs

| Evidence Category | Cost (INR) |
|---|---|
| Static Contract Permissions | 10 |
| Token Supply & Minting Mechanics | 10 |
| Fee & Tax Configuration | 10 |
| Off-Chain & Social Viability | 40 |
| On-Chain Wallet Flows & Distribution | 80 |
| Runtime Execution Simulation | 150 |

### 7.2 Decision Policy

Both checkpoints below apply the single threshold from Section 6.3 — Risk Score ≥ 0.33, equivalently Genuine Score ≤ 0.67. There is no separate threshold at either checkpoint.

1. **Mid-loop check** — After each evidence category is run and beliefs are updated (Section 5), before deciding whether to continue the VoI loop, check the *current* posteriors:
   - If **Genuine Score > 0.67**, stop the loop immediately and **PROCEED**.
   - If **Risk Score ≥ 0.33**, stop the loop immediately and **BLOCK**.
   - Otherwise, neither side has crossed the line yet — continue the loop (Section 4, step g) if evidence categories remain.
2. **End-of-loop check** — If every evidence category has been run and neither condition above has fired, apply the same Risk Score threshold one final time:
   - If **Risk Score ≥ 0.33**, **BLOCK** the trade.
   - Otherwise, **ESCALATE** for manual/secondary review — the model has exhausted its evidence and remains under the block threshold, but hasn't cleared it by enough margin to close out as PROCEED on its own.

---

## 8. Multi-Class Bayesian Likelihood Tables

The tables below give $P(\text{Evidence Outcome} \mid \text{Hidden State})$ for each of the six evidence categories. Each row sums to 1.0.

### 8.1 Static Contract Permissions

| Hidden State | Renounced | Centralized-Idle | Active-Admin-Control |
|---|---|---|---|
| Legitimate Project | 0.70 | 0.28 | 0.02 |
| Liquidity Rug Pull | 0.30 | 0.40 | 0.30 |
| Token Dump Rug Pull | 0.50 | 0.45 | 0.05 |
| Honeypot | 0.05 | 0.15 | 0.80 |
| Minting Abuse | 0.10 | 0.40 | 0.50 |
| Fee/Tax Rug Pull | 0.10 | 0.30 | 0.60 |
| Dead / Experimental | 0.60 | 0.35 | 0.05 |

### 8.2 Token Supply & Minting Mechanics

| Hidden State | Hard-Capped | Potential-Dilution | Active-Mint-Abuse |
|---|---|---|---|
| Legitimate Project | 0.85 | 0.14 | 0.01 |
| Liquidity Rug Pull | 0.60 | 0.35 | 0.05 |
| Token Dump Rug Pull | 0.50 | 0.40 | 0.10 |
| Honeypot | 0.40 | 0.40 | 0.20 |
| Minting Abuse | 0.02 | 0.08 | 0.90 |
| Fee/Tax Rug Pull | 0.70 | 0.25 | 0.05 |
| Dead / Experimental | 0.65 | 0.30 | 0.05 |

### 8.3 Fee & Tax Configuration

| Hidden State | Low-Immutable | Adjustable-Moderate | Honeypot-Tax |
|---|---|---|---|
| Legitimate Project | 0.88 | 0.11 | 0.01 |
| Liquidity Rug Pull | 0.55 | 0.35 | 0.10 |
| Token Dump Rug Pull | 0.60 | 0.35 | 0.05 |
| Honeypot | 0.10 | 0.20 | 0.70 |
| Minting Abuse | 0.70 | 0.25 | 0.05 |
| Fee/Tax Rug Pull | 0.01 | 0.09 | 0.90 |
| Dead / Experimental | 0.80 | 0.18 | 0.02 |

### 8.4 Runtime Execution Simulation

| Hidden State | Swaps-OK | High-Slippage | Execution-Reverted |
|---|---|---|---|
| Legitimate Project | 0.95 | 0.04 | 0.01 |
| Liquidity Rug Pull | 0.80 | 0.15 | 0.05 |
| Token Dump Rug Pull | 0.85 | 0.12 | 0.03 |
| Honeypot | 0.01 | 0.04 | 0.95 |
| Minting Abuse | 0.80 | 0.15 | 0.05 |
| Fee/Tax Rug Pull | 0.10 | 0.40 | 0.50 |
| Dead / Experimental | 0.75 | 0.20 | 0.05 |

### 8.5 On-Chain Wallet Flows & Distribution

| Hidden State | Distributed | Whale-Concentrated | Rug-Dumping |
|---|---|---|---|
| Legitimate Project | 0.82 | 0.16 | 0.02 |
| Liquidity Rug Pull | 0.05 | 0.25 | 0.70 |
| Token Dump Rug Pull | 0.02 | 0.18 | 0.80 |
| Honeypot | 0.20 | 0.50 | 0.30 |
| Minting Abuse | 0.30 | 0.40 | 0.30 |
| Fee/Tax Rug Pull | 0.40 | 0.40 | 0.20 |
| Dead / Experimental | 0.45 | 0.45 | 0.10 |

### 8.6 Off-Chain & Social Pulse

| Hidden State | Maintained | Ghost-Town | Abandoned-Fraud |
|---|---|---|---|
| Legitimate Project | 0.78 | 0.20 | 0.02 |
| Liquidity Rug Pull | 0.25 | 0.35 | 0.40 |
| Token Dump Rug Pull | 0.35 | 0.35 | 0.30 |
| Honeypot | 0.15 | 0.25 | 0.60 |
| Minting Abuse | 0.30 | 0.40 | 0.30 |
| Fee/Tax Rug Pull | 0.30 | 0.40 | 0.30 |
| Dead / Experimental | 0.02 | 0.88 | 0.10 |

---

## 9. Open Items to Reconcile

A few inconsistencies from the original draft are worth resolving before implementation:

1. **"Escalate" undefined** — The end-of-loop policy in 7.2 has a branch to "escalate for manual/secondary review," but this path isn't defined elsewhere (who reviews, what timeframe, what happens to the trade in the meantime).
2. **End-of-loop ESCALATE branch may be unreachable** — With one shared threshold at both checkpoints (Section 6.3), if the mid-loop check never fires BLOCK or PROCEED across every category, Risk Score has stayed under 0.33 the entire time with no new evidence left to change it — meaning the end-of-loop check in 7.2 can only land on PROCEED-equivalent territory, never trigger its own BLOCK, and the ESCALATE branch has no belief state that reaches it. Worth confirming whether ESCALATE is meant to fire on a narrower margin (e.g., Risk Score landing in a band just under 0.33, like 0.25–0.33) rather than the same 0.33 line.
3. **Likelihood table integrity** — Verified: all 42 rows (7 states × 6 categories) across the tables in Section 8 sum to 1.0. No correction needed here.

