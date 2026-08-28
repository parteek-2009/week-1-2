# Requirements: Token Risk Agent — Python Prototype

## Context for the coding agent

This is a **local, offline Python prototype**. There is no API, no real blockchain
data, and no real money. The system pretends to evaluate a cryptocurrency token
for scam risk, using a hardcoded specification (hidden states, evidence
categories, likelihood tables, costs) and pretend evidence supplied by the
developer via a JSON file. All "money spent on evidence" and "money at risk" are
simulated bookkeeping only — nothing is transacted.

The full technical specification this implementation must follow is attached
separately (`token_risk_agent_spec_2.md`). Read it before writing any code — it
is the source of truth for the math and the categories. The **decision policy**
is defined in this document (Decision policy section below), not in spec
Sections 6.3 / 7.2 — those combined-threshold rules are replaced entirely.
This document also adds the starting belief, the file layout, and how
evidence is supplied.

---

## 1. Fixed prior belief (starting point for Section 5's Bayes update)

The spec (Section 5) requires a prior $P(H_i)$ to perform the first update, but
does not state what it is. Use this exact fixed distribution — do not compute,
infer, or default to a uniform prior:

| Hidden State          | Prior  |
|------------------------|--------|
| Legitimate Project      | 0.30  |
| Liquidity Rug Pull       | 0.10  |
| Token Dump Rug Pull      | 0.15  |
| Honeypot             | 0.10  |
| Minting Abuse          | 0.15  |
| Fee/Tax Rug Pull        | 0.10  |
| Something Else         | 0.10  |

(Sums to 1.00 — verified.) This should live as a constant, not be hardcoded
inline where it's used — the agent may need to reset to this prior at the start
of each run.

---

## 2. How evidence is supplied — the evidence file mechanism

There is no live data source. Instead, evidence is supplied through a
**pre-written JSON file representing one pretend token's true evidence**,
decided by the developer before the run starts.

### 2.1 File format

One JSON object per scenario. Two parts:

- **`token_name`** — a string, first key in the file. This is a made-up label
  for the pretend token in this scenario (e.g. `"SafeMoonClone"`,
  `"MoonRocketV2"`) — purely for the humans reading input/output files to tell
  scenarios apart. **The program must never use this value for any decision,
  branch, or lookup.** Its only job is to be read in with the rest of the file
  and copied through unchanged into that scenario's result output (Section 5),
  so a person can match a result back to its input by name instead of by
  filename alone.
- The remaining keys — one per evidence category, using the exact category
  names from the spec, each holding the real outcome for that category.

```json
{
  "token_name": "SafeMoonClone",
  "Static Contract Permissions": "Renounced",
  "Token Supply & Minting Mechanics": "Hard-Capped",
  "Fee & Tax Configuration": "Low-Immutable",
  "Runtime Execution Simulation": "Swaps-OK",
  "On-Chain Wallet Flows & Distribution": "Distributed",
  "Off-Chain & Social Viability": "Maintained"
}
```

All 6 categories must be present in every scenario file (in addition to
`token_name`), each with exactly one of that category's 3 valid outcome
labels (see Section 3 of the spec for the valid labels per category).

### 2.2 Critical constraint: the agent must not see this file's contents up front

This is the core behavioral requirement, not just a data-loading detail:

- The Value-of-Information selection logic (spec Section 4) simulates all
  possible outcomes for each remaining category to decide *which category to
  run next*. This simulation step must NOT read the evidence file, and must
  have no code path that could access it. It only uses the likelihood tables
  and the current belief.
- Only *after* a category has been selected does the program look up that
  one category's value in the evidence file, and treat it as the real observed
  outcome for the Bayesian update (spec Section 5).
- Categories not yet selected must never be looked up. If the loop ends (via
  BLOCK/PROCEED/ESCALATE) with categories remaining, their evidence-file
  values are simply never read.
- Practical implication: whatever function loads/looks up evidence-file values
  should require a specific category name as input and return only that
  category's value — never expose the whole file to the selection logic.
- `token_name` is not evidence and is exempt from this restriction — it may be
  read once at load time (e.g. by `main.py`, to carry into the output), since
  it plays no role in any decision.

### 2.3 Multiple scenario files

Provide at least these 3 example scenario files so the decision logic can be
tested against different cases immediately:

1. **`scenario_clearly_legit.json`** — every category's outcome is the single
   most-likely outcome for the "Legitimate Project" state, per the likelihood
   tables. Expected agent behavior: should PROCEED, likely early via the
   mid-loop check once Legitimate Project's own probability reaches 0.67.
2. **`scenario_clearly_scam_honeypot.json`** — every category's outcome is the
   single most-likely outcome for the "Honeypot" state. Expected agent
   behavior: should BLOCK, likely early via the mid-loop check once one
   malicious state's own probability (typically Honeypot) reaches 0.67.
3. **`scenario_mixed_signals.json`** — a deliberately blended case: several
   categories look clean (legit-typical outcomes) while the wallet-flow
   category shows a "Rug-Dumping" pattern (typical of a Token Dump Rug Pull).
   This scenario should NOT resolve on the very first category checked — it
   exists to exercise the loop actually continuing past one piece of evidence
   and to test how the agent weighs conflicting signals. Expected behavior is
   intentionally not stated here — that's what running the agent against it
   should reveal.

Exact contents for all 3 files are provided in the appendix at the end of this
document — copy them verbatim rather than regenerating them, since their
outcomes were deliberately checked against the real likelihood tables for
internal consistency.

> **Note on scenario 2:** its Token Supply & Minting outcome is "Hard-Capped,"
> which may look counterintuitive next to "Weaponized" and
> "Execution-Reverted." This is correct, not a mistake — per the likelihood
> table in spec Section 8.2, Hard-Capped (0.40) is *marginally* more likely
> than Potential-Dilution (0.40, tied) or Active-Mint-Abuse (0.20) even under
> the Honeypot state; a honeypot's danger is typically in its
> sell-blocking/tax logic, not necessarily its minting behavior. Leave this
> value as-is.

### 2.4 Input: file path or folder path, given on the command line

The program takes exactly one command-line argument: a path. That path may
point to either:

- **a single scenario JSON file** — the program runs the agent once, against
  that one scenario, and writes one result file; or
- **a folder containing multiple scenario JSON files** — the program runs the
  agent once per `.json` file found directly inside that folder (each run is
  fully independent — belief resets to the fixed prior for each one), and
  writes one result file per scenario.

This must work for both a handful of files and 30–50 files without any change
in usage — same command either way:

```
python main.py scenarios/scenario_clearly_legit.json
python main.py scenarios/
```

No interactive terminal prompts, no pasting JSON into the terminal. The only
input mechanism is the path argument plus whatever files it points to.

---

## 3. Required file structure

```
token_risk_agent/
├── main.py                  # entry point; runs the loop; writes result JSON per scenario
├── states.py                 # the 7 hidden states (Section 2) + the fixed prior (this doc, Section 1)
├── evidence.py                 # the 6 categories, their 3 outcome labels each, and costs (spec Sections 3, 7.1)
├── likelihoods.py               # the 6 likelihood tables, hardcoded (spec Section 8)
├── bayes.py                  # belief-update function (spec Section 5) — pure function, no I/O
├── voi.py                    # EIG / JS-divergence / value-per-rupee selection (spec Section 4) — simulation only, never touches real evidence
├── entropy.py                  # entropy of a belief distribution; remaining-entropy-per-category for output (this doc, Section 5)
├── decision.py                 # per-state mid-loop checks + end-of-loop combined check (this doc, Decision policy)
├── evidence_input.py              # loads one scenario file; exposes a per-category lookup only (this doc, Section 2)
├── scenarios/
│   ├── scenario_clearly_legit.json
│   ├── scenario_clearly_scam_honeypot.json
│   └── scenario_mixed_signals.json
└── results/                   # created by the program; one result JSON per scenario run (this doc, Section 5)
```

### Code style — read this before writing anything

- **No classes anywhere in this codebase.** Every file above is plain
  functions operating on plain data (dicts, lists, tuples). No custom
  classes, no OOP patterns, no inheritance. This applies even where a class
  might feel natural (e.g. "a Belief class") — use a dict instead
  (`{"Legitimate Project": 0.20, ...}`).
- Every function should be short enough and plainly-named enough that someone
  who has never seen this codebase, and is new to Python, can read it and
  understand what it does without needing to trace through other files
  first. Prefer a few small, obviously-named functions over one clever
  compact one.
- Avoid advanced/unfamiliar Python features where a plain approach works
  just as well (e.g. plain `for` loops over comprehensions where a loop is
  clearer; explicit `if/else` over one-liners; no decorators, no
  metaprogramming, no `*args`/`**kwargs` unless genuinely necessary).
- This rule applies to every file in the structure above without exception —
  including `voi.py` and `bayes.py`, where the math itself is the complex
  part; keep the *code* simple even where the *concept* isn't. Break the
  math into small named steps (e.g. a function that computes one outcome's
  divergence, called once per outcome in a loop) rather than one dense
  formula-in-one-line.

### Responsibilities per file (do not blur these — each function should only need the inputs listed)

- **`states.py`** — Data only. The 7 state names in a fixed order; which 5 are
  "malicious" (for the mid-loop per-state BLOCK check and the end-of-loop
  combined score); the fixed prior from Section 1 above.
- **`evidence.py`** — Data only. Category names, their 3 valid outcome labels,
  their INR costs (spec Section 7.1).
- **`likelihoods.py`** — Data only. The 6 tables from spec Section 8, structured
  as `table[category][state][outcome] = probability`. This is the only file
  containing the raw likelihood numbers.
- **`bayes.py`** — One function: `(belief, category, observed_outcome,
  likelihoods) -> new_belief`. Implements spec Section 5's formula exactly.
  Must not know about cost, evidence files, or the decision policy.
- **`voi.py`** — Implements spec Section 4 steps (a)–(f): for each remaining
  category, simulate all 3 outcomes, compute expected posterior via
  `bayes.py`, measure Jensen-Shannon Divergence against current belief, weight
  by outcome probability for EIG, divide by cost, return the
  highest-value-per-rupee category. **Must never import or call
  `evidence_input.py`.** This is a hard requirement, not a style preference —
  see Section 2.2 above.
- **`entropy.py`** — Two functions. One computes the Shannon entropy of any
  7-state belief distribution (a single number). The other computes, for one
  *unchecked* category, the expected entropy of the belief if that category
  were run next — this reuses the same outcome-simulation approach `voi.py`
  already does (simulate each of the category's 3 outcomes, compute the
  hypothetical posterior via `bayes.py` for each, take the entropy of each
  resulting belief, then weight by that outcome's probability and sum). This
  second function is what produces the "remaining entropy per evidence
  category" figures in the output (Section 5) — it does not touch the real
  evidence file, same restriction as `voi.py`.
- **`decision.py`** — Applies the mid-loop and end-of-loop checks from this
  document's Decision policy section. Mid-loop inspects each of the 7 states
  individually (never a summed score). End-of-loop is the only place a
  combined score is used. Returns one of: CONTINUE, PROCEED, BLOCK,
  ESCALATE. Pure function of the belief — no knowledge of categories, costs,
  or files.
- **`evidence_input.py`** — Loads a scenario JSON file given its path.
  Exposes exactly one lookup function: given a category name, return that
  category's outcome value from the loaded file (see Section 2.2 for the
  `token_name` exemption). Must not expose the full parsed file's evidence
  values to callers other than itself.
- **`main.py`** — Orchestrates the loop per the order of operations in
  Section 4 below, for one scenario at a time. Resolves the command-line
  path argument (Section 2.4) into one or more scenario files to run.
  Assembles and writes the result JSON (Section 5) for each. Tracks running
  INR cost (bookkeeping only, per Context section above — no real
  transaction).


---
Do **not** implement the spec's combined-threshold decision rule mid-loop. That rule
is replaced entirely by the two checks below. 

### Mid-loop check

Run this after every **real** evidence update, before deciding whether to
continue the loop. It checks each of the 7 states' **own individual**
probability, one at a time — not a combined or summed score.

- If Legitimate Project's probability ALONE is ≥ 0.67 → return **PROCEED**
- Else if ANY ONE of the 5 malicious states (Liquidity Rug Pull, Token Dump Rug Pull, Honeypot, Minting Abuse, Fee/Tax Rug Pull) individually has probability ≥ 0.33 → return **BLOCK**
- Else if Something Else's probability ALONE is ≥ 0.33 → return **BLOCK**
- Else → return **CONTINUE** (keep looping if categories remain)

Important: PROCEED uses 0.67 as its bar. BLOCK (whether from a malicious state or from Something Else) uses 0.33 as its bar. These are independent single-state checks. Legitimate Project is never combined with Something Else.

This check must never fire before at least one real evidence category has
been checked: no single state in the fixed prior (Section 1) reaches its threshold alone, so the agent cannot stop on the untouched prior.

### End-of-loop check

Only reached if every evidence category has been checked and the mid-loop
check above never fired.

- Sum: (the 5 malicious states combined) + Something Else.
- If that sum is **> 0.67** → return **BLOCK**
- Else → return **ESCALATE**

This is the only place a combined/summed score is used — end-of-loop only,
never mid-loop.
---




## 4. Required order of operations (per scenario)

For each scenario file being run (one file, or each file in a folder per
Section 2.4), reset belief to the fixed prior (Section 1), then loop:

```
1. category = voi.select_best_category(belief, remaining_categories, evidence.py, likelihoods.py)
   -> simulation only; does not call evidence_input.py

2. outcome = evidence_input.get_outcome(loaded_scenario, category)
   -> ONLY NOW is the real evidence-file value for this one category read

3. belief = bayes.update(belief, category, outcome, likelihoods.py)

4. remaining_categories.remove(category)
   checked_categories.append(category)   # in order, for the output
   running_cost_spent += evidence.py[category].cost   # bookkeeping only

5. verdict = decision.check_mid_loop(belief)
   - if PROCEED or BLOCK: stop looping, go to step 6
   - if CONTINUE and remaining_categories is empty: verdict = decision.check_end_of_loop(belief), go to step 6
   - if CONTINUE and categories remain: go back to step 1

6. For each category still in remaining_categories (never checked), compute
   its expected-entropy-if-run-next via entropy.py. These, plus the final
   belief, verdict, checked_categories, and cost, are assembled into the
   result JSON (Section 5) and written to results/.
```

---

## 5. Output requirements

For every scenario run, `main.py` writes one JSON file to `results/`, named
after the input scenario (e.g. `scenario_clearly_legit.json` in →
`results/scenario_clearly_legit_result.json` out). No terminal-only output —
everything below must land in the file (printing a copy to the terminal too
is fine, but the file is the source of truth).

Each result JSON must contain:

```json
{
  "token_name": "SafeMoonClone",
  "final_answer": "PROCEED",
  "confidence_score": 0.81,
  "final_belief": {
    "Legitimate Project": 0.81,
    "Liquidity Rug Pull": 0.04,
    "Token Dump Rug Pull": 0.05,
    "Honeypot": 0.03,
    "Minting Abuse": 0.03,
    "Fee/Tax Rug Pull": 0.02,
    "Something Else": 0.02
  },
  "checked_categories": [
    {
      "category": "Static Contract Permissions",
      "observed_outcome": "Renounced",
      "cost_inr": 10,
      "belief_after": { "...": "7-state belief immediately after this category's update" }
    }
  ],
  "unchecked_categories": [
    {
      "category": "Runtime Execution Simulation",
      "cost_inr": 150,
      "expected_entropy_if_run": 1.42
    }
  ],
  "total_cost_inr": 20,
  "reasoning": [
    "Selected 'Static Contract Permissions' first: highest value-per-rupee among all 6 categories (cost 10 INR).",
    "Observed outcome 'Renounced'. Updated belief accordingly.",
    "State Legitimate Project reached 81.0% (>= 67%) — stopping loop, verdict PROCEED."
  ]
}
```

Field-by-field:

- **`token_name`** — carried through unchanged from the scenario file
  (Section 2.1). Never altered or interpreted.
- **`final_answer`** — one of `PROCEED`, `BLOCK`, `ESCALATE`, from
  `decision.py`.
- **`confidence_score`** — the belief in whichever single state or combined
  side the final answer corresponds to. For PROCEED (mid-loop), this is
  Legitimate Project's individual probability. For BLOCK from mid-loop, this
  is the individual state that reached ≥ 0.67 (a malicious state, or
  Something Else). For BLOCK or ESCALATE from end-of-loop, this is the
  combined (5 malicious states + Something Else) score.
- **`final_belief`** — the full 7-state distribution at the point the loop
  stopped.
- **`checked_categories`** — every category actually run, **in the order it
  was run**, each with its observed outcome, its cost, and the belief
  distribution immediately after that category's update. This is the
  category-by-category trace of the whole run.
- **`unchecked_categories`** — every category never run (empty list if all 6
  were checked), each with its cost and its `expected_entropy_if_run` from
  `entropy.py` (this doc, Section 3's file structure) — i.e. "if the loop had
  continued and picked this category next, roughly how much uncertainty
  would remain."
- **`total_cost_inr`** — sum of costs for checked categories only.
- **`reasoning`** — a short list of plain-language strings, one or more per
  loop step, explaining what was picked and why, and why the loop stopped
  when it did. This does not need to be exhaustive math — it should read
  like a human explaining the run, referencing the actual numbers involved
  (which category, which outcome, which threshold got crossed). Mid-loop
  stops must be phrased as "state X reached Y%" (that state's own
  probability). End-of-loop stops must be phrased as "combined
  malicious+something-else reached Y%". Continue steps should say that no
  single state reached 67%, naming the current highest state.

Running the program against a whole folder (Section 2.4) produces one such
file per scenario in `results/` — nothing needs to be aggregated across
scenarios for this prototype.

---

## 6. Explicitly out of scope for this prototype

- No real API calls, no real blockchain/contract interaction, no real payment
  of any kind.
- No persistence between runs beyond the scenario JSON files themselves.
- No UI beyond terminal output.
- The undefined ESCALATE review process (who reviews, what happens to the
  trade) remains out of scope. Implement the end-of-loop rule in this
  document's Decision policy exactly as written (combined malicious +
  Something Else > 0.67 → BLOCK, else ESCALATE). Do not silently "fix" this
  by inventing a different end-of-loop threshold.

---

## Appendix: scenario file contents

### `scenarios/scenario_clearly_legit.json`
```json
{
  "token_name": "CleanChainToken",
  "Static Contract Permissions": "Renounced",
  "Token Supply & Minting Mechanics": "Hard-Capped",
  "Fee & Tax Configuration": "Low-Immutable",
  "Runtime Execution Simulation": "Swaps-OK",
  "On-Chain Wallet Flows & Distribution": "Distributed",
  "Off-Chain & Social Viability": "Maintained"
}
```

### `scenarios/scenario_clearly_scam_honeypot.json`
```json
{
  "token_name": "MoonYieldRush",
  "Static Contract Permissions": "Weaponized",
  "Token Supply & Minting Mechanics": "Hard-Capped",
  "Fee & Tax Configuration": "Honeypot-Tax",
  "Runtime Execution Simulation": "Execution-Reverted",
  "On-Chain Wallet Flows & Distribution": "Whale-Concentrated",
  "Off-Chain & Social Viability": "Abandoned-Fraud"
}
```

### `scenarios/scenario_mixed_signals.json`
```json
{
  "token_name": "AmbiguousProtocolX",
  "Static Contract Permissions": "Renounced",
  "Token Supply & Minting Mechanics": "Hard-Capped",
  "Fee & Tax Configuration": "Low-Immutable",
  "Runtime Execution Simulation": "Swaps-OK",
  "On-Chain Wallet Flows & Distribution": "Rug-Dumping",
  "Off-Chain & Social Viability": "Maintained"
}
```
