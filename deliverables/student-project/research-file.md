# Research File

A running log of what I researched, why, and how it changed the design of the token-risk
agent. This is separate from `discussion-record.md` (human/social feedback) and
`paper/references.bib` (formal citations) — this file is the informal trail: what I didn't
know, what I looked up, and what stuck.

## Problem statement

Cryptocurrency rug pulls are common enough that a large share of newly listed tokens turn out
to be some form of scam rather than a functioning project. Figuring out whether a specific
token is safe to buy isn't one check — it's a sequence of them: reading the smart contract,
checking liquidity, checking who holds the supply, checking wallet history, checking social
presence, then weighing all of it before deciding. Doing this properly for every candidate
token is slow, and skipping steps is exactly how obvious scams get missed. Narrowed down per
the Week 2 brief's format: *given a token's evidence arriving one category at a time, which
evidence category should the agent check next, and at what belief should it stop checking and
either approve, block, or escalate the token?*

## Where I started: I didn't know what crypto was

I went in with close to zero background on how cryptocurrency or blockchain actually works.
The original plan was a large, general-purpose agent; after seeing how those tend to get built
and how unfocused that would end up, I switched to something specific — which is how I landed
on rug pulls once I found the topic.

**Search query used:** `basics of crypto`
**Source found:** PwC overview article on Bitcoin, blockchain, and cryptocurrency —
https://www.pwc.com/us/en/industries/financial-services/fintech/bitcoin-blockchain-cryptocurrency.html
**What it gave me:** General orientation on blockchain and crypto mechanics. Useful as a
starting point but fairly high-level/obvious once I understood the basic shape of the problem.

**Search query used:** `scams in crypto` (on YouTube)
**Sources found:** Three explainer videos on rug pulls specifically —
- https://youtu.be/YFaqng3YESE
- https://youtu.be/RwHGp4mELbU
- https://youtu.be/dVJzcFDo498

**What they gave me:** This is where the project actually took shape. Rug pulls turned out to
have several distinct variations rather than being one thing, which directly shaped the hidden
states (Section 4.1 of the paper): a **liquidity pull** (scammers drain the 1:1 liquidity pool
that trading against the token relies on), **share/token dumping** (the team keeps a large
share of supply and sells it once the price rises, collapsing it), and a **honeypot** (the
contract lets you buy but blocks you from selling). These three mechanisms, learned directly
from these videos, are the seed of three of the paper's seven hidden states.

## Technical terms I had to look up

Terms encountered while reading around this problem, in roughly the order I ran into them:

- **Liquidity pool / liquidity pull** — the pooled trading capital (typically token + a paired
  valuable coin) behind a token; a liquidity pull is insiders draining that pool.
- **Rug pull** (general) — an umbrella term I initially treated as one hidden state before
  learning it covers several distinct mechanisms (see above).
- **Honeypot (contract)** — a contract that allows buy transactions to succeed but blocks or
  reverts sell transactions.
- **Minting / mint function** — the contract capability to create new supply after launch;
  relevant to the Minting Abuse hidden state.
- **Renounced ownership** — a contract state where the deployer has given up privileged admin
  control, used in Category 1 (Static Contract Permissions).
- **Slippage** — price movement between when a trade is submitted and when it executes; used
  as one of the three Runtime Execution Simulation outcomes (Frictional / High-Slippage).
- **SPF / DKIM** — not part of this project's domain, but encountered while working through
  the Week 2 brief's own worked example (email authentication), useful for understanding the
  likelihood-table pattern the brief was demonstrating before I built my own tables.
- **Bayes' theorem / prior / likelihood / posterior** — the core update mechanism; looked up
  via AI-assisted explanation (see below) after finding the brief's own explanation useful but
  wanting the arithmetic double-checked by hand.
- **Jensen–Shannon Divergence** — needed once I'd chosen KL divergence as an initial candidate
  for measuring belief shift and ran into its asymmetry problem; searched for a symmetric,
  bounded alternative.
- **Value of Information** — the idea that a piece of evidence is only worth what it can
  change about the decision, not just how many bits it carries; this reframed the whole
  evidence-selection design (Section 6 of the paper) away from a naive "always check the most
  informative category" rule.

## AI-assisted research

Used Claude for:
- Understanding how each of the six evidence categories in this project actually maps onto
  something detectable on-chain or off-chain (e.g. what "runtime execution simulation" means
  concretely, what wallet-flow clustering looks like in practice).
- General back-and-forth on blockchain/crypto mechanics beyond what the PwC article and videos
  covered, to sanity-check terminology before writing the likelihood tables.
- Exploring and narrowing the hidden-state taxonomy — the five-revision process described in
  the paper (Section 4.1) went through several candidate splits before landing on the current
  seven states, and Claude was used as a sounding board for whether states were genuinely
  mutually exclusive and whether the evidence categories could actually distinguish them.
- Reviewing and helping implement the Python modules (`bayes.py`, `voi.py`, `entropy.py`,
  `decision.py`, and the rest) against the technical specification once the design was set.

Full disclosure of AI use, including verification steps and which experiments were personally
run, is in the paper's AI-Use Statement — this section is the research-process view of the
same work, not a replacement for that statement.

## What I did not research

I did not read academic literature on rug-pull detection, sequential evidence selection, or
Bayesian fraud-screening systems — the background here is informal, aimed at understanding the
domain rather than surveying prior formal approaches. This is stated plainly in the paper's
Related Work section rather than padded out with citations I didn't actually read.

## How this research changed the design

- The three-video research directly produced the three-way split of "rug pull" into distinct
  mechanisms (liquidity pull, dumping, honeypot) instead of one undifferentiated malicious
  state — this is the single biggest design decision that traces back to a specific source.
- Realizing rug pulls had further sub-variations (minting abuse, fee/tax extraction) that used
  the *same* evidence categories but represented genuinely different mechanisms led to
  expanding from five to seven hidden states.
- Running into KL divergence's asymmetry (via AI-assisted explanation, then checked against my
  own two-state example) is what sent me looking for Jensen-Shannon Divergence specifically,
  rather than starting from JSD as a known destination.
