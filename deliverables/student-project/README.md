# week-1
# Cost-Optimized Multi-Class Bayesian Token Risk Agent — Week 2

A sequential, Value-of-Information-driven Bayesian agent for cryptocurrency rug-pull risk
assessment. This extends the Week 1 agent with explicit beliefs, an information-theoretic
evidence-selection rule, a cost-derived decision threshold, and a full experiment across 60
scenarios.

See `paper/preprint.pdf` for the full write-up — the PDF is the deliverable and is meant to
stand alone. Everything else in this repository is supporting material.

## What the agent does, in one paragraph

The agent holds a belief over 7 mutually exclusive hidden states a token could be (Legitimate,
one of five malicious mechanisms, or Something Else). At each step it picks the single
remaining evidence category with the highest Expected Information Gain per rupee (Value of
Information), observes that category's real outcome, updates its belief via Bayes' theorem,
and checks a cost-derived threshold to decide whether to stop (PROCEED / BLOCK) or keep
gathering evidence. If every category is exhausted without a clear call, it falls through to
an end-of-loop check that either BLOCKs or ESCALATEs. Full details, derivations, and the
worked example are in the paper.

## Repository structure

```
week2/
|-- README.md                  <- this file
|-- research-file.md           <- background reading notes (PwC article, YouTube videos)
|-- discussion-record.md       <- human/social feedback log (updated, not replaced, from Week 1)
|-- paper/
|   |-- main.tex               <- LaTeX source for the preprint (IJCAI-style)
|   |-- references.bib         <- bibliography, only sources actually read
|   |-- figures/                <- chart_cost_comparison.png, chart_category_frequency.png
|   `-- preprint.pdf           <- THE DELIVERABLE
|-- src/
|   |-- main.py                <- entry point; runs the VoI loop end-to-end
|   |-- bayes.py                <- Bayesian belief update (pure function)
|   |-- voi.py                  <- Value-of-Information category selection
|   |-- entropy.py              <- entropy / expected-entropy-if-run calculations
|   |-- decision.py             <- mid-loop and end-of-loop decision policy
|   |-- evidence.py             <- evidence category list and costs
|   |-- evidence_input.py       <- reads real scenario outcomes from JSON
|   |-- states.py               <- hidden-state list and fixed prior
|   `-- likelihoods.py          <- the six likelihood tables (P(outcome | state))
|-- notebooks/                 <- exploratory analysis (optional; not required to reproduce results)
|-- experiments/
|   `-- scenarios/              <- the 60 hand-built scenario input JSON files
|       |-- batch1_scenario_diversity/   <- 50 files (test_NN_<label>_...json)
|       `-- batch2_decision_policy/      <- 10 files (policy_NN_<checkpoint>_...json)
|-- results/                   <- one *_result.json per scenario, written by main.py
|-- decisions/
|   `-- decision-record.md     <- log of design decisions made and why (e.g. resolving the
|                                  spec's combined-threshold issue, Section 7 of the paper)

## Running it

```bash
# Single scenario
python src/main.py experiments/scenarios/batch1_scenario_diversity/test_01_legit_benchmark.json

# Whole batch (folder mode — main.py accepts a directory)
python src/main.py experiments/scenarios/batch1_scenario_diversity/
python src/main.py experiments/scenarios/batch2_decision_policy/
```

Each run writes `results/<scenario_name>_result.json`, containing the final verdict,
confidence score, full belief trajectory, which categories were checked and in what order,
and total INR cost spent. No randomness is involved anywhere in the pipeline — the Bayesian
update and the VoI selection are both deterministic given the belief and the fixed likelihood
tables in `likelihoods.py`, so no seed is needed to reproduce a result.

## Key results (see the paper for full detail)

Across the 50 Batch 1 scenarios, the agent reached a verdict after checking an average of
2.44 of 6 evidence categories, cutting total evidence cost by 90.9% against an
all-categories-every-time baseline (INR 1,370 vs. INR 15,000), and matched the scenario's
intended label on 87.1% of unambiguous cases. The main finding worth reading the paper for:
the two most expensive, most diagnostic categories (Runtime Execution Simulation and
On-Chain Wallet Flows & Distribution) were never selected across any of the 60 runs — a
structural property of the current cost/prior combination, not a bug, and the direct cause of
two scam scenarios clearing as PROCEED (see Failure Analysis in the paper).

## Status / what's not yet in this repository

- `notebooks/` is exploratory and not required to reproduce the paper's results — everything
  reported comes directly from `src/main.py` and the files in `results/`.
- `social/linkedin-posts.md`, `social/x-thread.md`, and `discussion-record.md` are being
  filled in as the social-learning component of this week's work progresses.
- `decisions/decision-record.md` currently covers the one major design resolution documented
  in the paper (Section 7): replacing the original spec's combined-threshold rule with the
  two-check policy actually implemented in `decision.py`.

## AI-use disclosure

AI assistance (Claude, Anthropic) was used for research and understanding (blockchain/crypto
mechanics, evidence-category design), for implementation help across the `src/` modules, and
for drafting/editing the paper itself. Full disclosure, what was verified and how, and which
experiments were personally run are in the paper's AI-Use Statement section — that is the
canonical version; this line is a pointer, not a substitute.
