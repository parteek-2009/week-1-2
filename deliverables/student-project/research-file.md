## Problem Statement : 
Some e-commerce sellers buy fake reviews either positive ones for their own 
listings, or negative ones to target competitors. This misleads shoppers, who 
end up paying for something other than what they expected. These fake accounts 
are cheap to create and appear in large numbers, making manual human review too 
slow and too expensive to keep up with.

The agent observes a review's text and metadata (verified purchase status, 
account age, review frequency, and for unclear cases similarity to the 
user's past reviews and how concentrated their reviews are on one seller). it 
must decide to approve the review, flag it for high-priority human ban review, 
or send it to a human review list if agent is not sure.

## Project Objective

Design and test an agent that decides whether an e-commerce review is likely 
genuine or fake, using cheap signals first and only escalating to deeper 
checks or a human when the evidence is genuinely unclear. The goal is not a 
perfect classifier it is a system that knows when it doesn't know, and 
routes those cases to a human instead of guessing, so a false accusation 
never happens without a person checking first.

## Technical Terms

* Hidden State: The true nature of a review (genuine or fake) that the agent 
cannot directly observe only from signals.
* Bayesian Update: The math the agent uses to revise its belief about a review 
being genuine, each time new evidence comes in.
* Prior Probability: The agent's belief before looking at a new piece of 
evidence.
* Posterior Probability: The updated belief after a Bayesian update.
* Base Rate: The historical frequency used as a starting point like how often 
new account + very short review has turned out to be fake in the past.
* Gray Zone: The 20-60% P(Genuine) range where the agent is not confident enough 
to approve or flag, and needs more evidence or a human.
* HITL (Human  in the Loop): A human makes the final call instead 
of the agent used for high-priority bans and gray zone review.
* Cross Review Similarity: How closely a user's recent reviews match his each other 
in wording used to catch copy-paste reviews.
* Brand Concentration Ratio: What percent of a user's reviews target one seller.

## Search Queries

**Platform Detection Methods**
- "does platforms like amazon have fake review finders?"
- "how did these platforms catch fake reviews"
- "which platforms use review detection"
- "are the models used in platforms are probabilistic mostly"

**Bot Review Patterns**
- "common patterns of a bot review in ecommerce platforms"
- "examples of bot messages which obviously look fake and are easy to find"

**Hard-to-Catch Cases**
- "how to find a fake review which looks real like it is long and all"
- "examples of bot messages which are fake but looks genuine"
- "how did real reviews can be seemed fake"

## Possible Types of Reviews

- Review appears genuine, is genuine
- Review appears fake, is fake
- Review appears genuine, is fake
- Review appears fake, is genuine

## Signals (Evidence the Agent Checks)

**Level 1, checked on every review**
- Structure check (very short[with use case if given] / short[with use case if given] / moderate / long)
- Verified purchase (true / false)
- Account age (new / moderate / old)
- Review frequency (low / high / very high)

**Level 2, checked only if review lands in gray zone (20-60%)**
- Cross review similarity (compares last 5 to 10 reviews for to find copy paste patterns)
- Brand concentration ratio (percentage of user's reviews on that one seller)

## Observations

The table below is my own prediction, based on the architecture's signals means it's not confirmed by real data. Testing will show whether these patterns actually hold.

| Observation | What it might suggest |
|-------------|------------------------|
| Very short review, verified purchase, old account | Likely 4th (real, blunt) |
| Long review, new account, high review frequency | Likely 3rd (paid fake, high effort) |
| Short review, unverified, very high frequency | Likely 2nd (bot spam) |
| High cross-review similarity across last 5-10 reviews | Shifts belief toward 2nd and 3rd |
| High brand concentration (most reviews target one seller) | Shifts belief toward 2nd and 3rd |
| Long review, verified purchase, moderate account age | Likely 1sr (genuine) |

## Prior, Likelihood, Posterior

Prior: The agent's belief about a review before looking at new evidence 
(for Level 2, this is Level 1's output).

Likelihood: How likely a given signal (for eg. a verified purchase = false) would be 
to appear, if a specific state (looks genuine, is genuine) were actually true.

Posterior: The updated belief after combining the prior with new evidence
becomes the new P(Genuine).

Real probability values are not assigned yet. Priors and likelihoods will be 
estimated from historical review data. A uniform-prior baseline 
(treating all states as equally likely at the start) will also be tested for 
comparison.

## Likelihood Table

This table is my own assumption, based on the architecture's logic not  
measured from real data yet. High/Medium/Low estimates for now, not real 
probability numbers.

| Signal | 1st (real, looks real) | 2nd (fake, looks fake) | 3rd (fake, looks real) |4th (real, looks fake) |
|---|---|---|---|---|
| Verified purchase = true | High | Low | Medium | High |
| Very short review | Low | High | Low | High |
| New account | Low | High | Medium | Low |
| Very high review frequency | Low | High | Low | Low |
| High cross-review similarity | Low | High | Medium | Low |
| High brand concentration | Low | Medium | High | Low |

## Signal Costs

Verified purchase check = Cost: Low because it is already stored as platform data, no extra 
compute needed.

Account age check = Cost: Low,Same as above.

Review frequency check = Cost: Low as simple count from existing account history.

Structure check (micro-LLM) = Cost: Low to Medium as it Runs on every review, so 
volume adds up, but each call is cheap and fast.

Cross review similarity = Cost: Medium, Only runs in the gray zone but needs 
to pull the last 5 to 10 reviews and compute embeddings so more compute 
than Level 1 checks.

Brand concentration ratio = Cost: Low to Medium. Needs the user's review 
history across sellers, but the calculation itself is simple..

Human review (HITL) = Cost: High. Slowest and most expensive as a person has 
to actually read the case and decide.

# Target Communities & Research Outreach

## Target Reddit Communities

| Community | Focus & Project Relevance | URL | Status |
| :--- | :--- | :--- | :--- |
| **r/trustandsafetypros** | Trust & Safety Operations, HITL Queue Design, Moderator Burnout | https://www.reddit.com/r/trustandsafetypros/ | Verified |
| **r/productreview** | Review Dynamics, Consumer Sentiment & E-commerce Review Fraud | https://www.reddit.com/r/productreview/ | Verified |
| **r/softwarearchitecture** | 2-Tier Pipeline Design, Latency Limits, Queue & Fallback Systems | https://www.reddit.com/r/softwarearchitecture/ | Verified |
| **r/learnmachinelearning** | Bayesian Prior Adjustments, Embedding Similarity, Sparse Data | https://www.reddit.com/r/learnmachinelearning/ | Verified |
| **r/ecommerce** | Store Owner Perspectives, False Positive Customer Ban Trade-offs | https://www.reddit.com/r/ecommerce/ | Verified |

---

## Research Objectives by Community

1. **r/trustandsafetypros**
   * **Focus:** Operational workflows for Human-In-The-Loop (HITL) moderation.
   * **Key Insight Sought:** Best practices for separating "High-Priority Ban" queues from "Unclear Review" queues to reduce reviewer fatigue and prevent feedback loop corruption.

2. **r/productreview**
   * **Focus:** E-commerce user behavior and review authenticators.
   * **Key Insight Sought:** Real-world patterns in user review length, rating distributions, and signals distinguishing organic blunt reviews from paid promotional reviews.

3. **r/softwarearchitecture**
   * **Focus:** Low-latency pipeline design and fallback mechanisms.
   * **Key Insight Sought:** Evaluating the 2-tier cascade architecture (<50ms Level 1 metadata check with async Level 2 vector processing) during high-throughput traffic spikes.

4. **r/learnmachinelearning**
   * **Focus:** Probabilistic models and sparse data handling.
   * **Key Insight Sought:** Handling cold-start issues for brand-new reviewer accounts, smoothing priors, and resolving conditional dependence between metadata signals in Naive Bayes.

5. **r/ecommerce**
   * **Focus:** Financial and brand impact of moderation errors.
   * **Key Insight Sought:** How online retailers evaluate the cost of false positives (banning genuine customers) versus false negatives (allowing fake review leakage).

## Relevant Domain Experts & Researchers (X / Twitter)

### Trust & Safety & Platform Integrity
* **Alex Stamos** (`@alexstamos`) - Former Director at Stanford Internet Observatory & Facebook CSO. Expertise in platform security, abuse handling, and bot mitigation.
* **Yoel Roth** (`@yroth`) - UC Berkeley Fellow, Former Head of Trust & Safety at Twitter. Expertise in HITL moderation queue workflows and anti-spam heuristics.
* **Arvind Narayanan** (`@random_walker`) - Professor at Princeton University. Expertise in platform transparency, machine learning auditability, and algorithm fairness.

### NLP & Deceptive Review Research
* **Bing Liu** (UIC) - Pioneer in opinion spam, deceptive review detection, and sentiment analysis algorithms.
* **Yejin Choi** (`@YejinChoinka`) - Stanford University / NVIDIA. Leading researcher in NLP deception detection and reasoning.
* **Margaret Mitchell** (`@mmitchell_ai`) - Hugging Face. Focuses on dataset quality, ML evaluation, and model safety auditing.

### Bayesian & Probabilistic Machine Learning
* **David Blei** (`@bleilab`) - Columbia University. Leading authority on Bayesian inference and probabilistic topic models.
* **Shakir Mohamed** (`@shakir_za`) - Google DeepMind. Expert in probabilistic machine learning and statistical AI systems.
* **David Duvenaud** (`@duvenaud`) - University of Toronto. Focuses on uncertainty quantification and probabilistic models.

## Key Research Resources & Technical References

| Resource Name & Reference | Type & Source | Core Focus & Data Provided | Project Relevance & Use Case |
| :--- | :--- | :--- | :--- |
| **Finding Deceptive Opinion Spam by Any Stretch of Imagination** <br>*(Ott et al., ACL 2011)* | Landmark Research Paper | Linguistic and psychological deception cues (pronoun usage, spatial specificity, exaggerated sentiment) | Establishes linguistic feature weights and rules to seed the Level 2 Deep Pass prompt and text evaluation logic. |
| **YelpCHI Dataset** <br>*(Rayana & Akoglu / Mukherjee et al., SIGKDD)* | Production Metadata Dataset | 67,000+ real Yelp reviews with ground-truth filtered/recommended flags, account age, rating variance, and posting frequency | Provides empirical distributions to calibrate baseline likelihood ratios and priors for the Level 1 Naive Bayes fast pass. |
| **Prompt-Based Synthetic Review Detection** <br>*(GitHub: `fake-review-detection`)* | LLM Synthetic Benchmark | Thousands of AI-generated product reviews across multiple modern LLMs (GPT-4, Claude, Llama) | Tests Level 2 vector similarity checks against modern, non-templated AI spam that bypasses simple n-gram/TF-IDF filters. |
| **Deceptive Review Detection Pipelines** <br>*(GitHub: PyTorch / Scikit-learn)* | Reference Code Repository | End-to-end Python implementations contrasting Naive Bayes baselines against BERT/Transformer text embeddings | Provides tested reference code for extracting metadata signals, computing embeddings, and outputting posterior probabilities. |
| **Cascaded Moderation Pipelines: Fast Gates vs. Deep Queues** | System Architecture Guide | Industry practices for low-latency UGC moderation, queue management, and async worker design | Validates the 2-tier cascade architecture (<50ms L1 gate + async L2 queue) and Human-In-The-Loop (HITL) queue separation. |