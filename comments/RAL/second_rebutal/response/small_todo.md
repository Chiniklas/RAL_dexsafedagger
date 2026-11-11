# Second rebuttal — small TODOs

This file tracks the remaining clarification, statistical-analysis, reporting,
and formatting requests from Reviewer 29 and Reviewer 31. Major scientific
issues are tracked separately in [`TODO.md`](TODO.md).

## Small-task index

| Task | Reviewer item | Action | Status |
|---|---|---|---|
| Small Task 1 | Reviewer 29, comment 1 | Maintain empirical safety language | Complete: empirical scope and absence of formal guarantees reaffirmed in the response |
| Small Task 2 | Reviewer 29, comment 2 | Emphasize the 39.2% unseen-object unsafe rate | Complete |
| Small Task 3 | Reviewer 29, comment 3 | Add uncertainty/significance analysis for physical (e) versus (f) | Open |
| Small Task 4 | Reviewer 29, comment 4 | Analyze the consequences of critic false negatives | Open |
| Small Task 5 | Reviewer 29, comment 5 | Measure how early the Bellman critic warns before unsafe termination | Open |
| Small Task 6 | Reviewer 29, comment 6 | Clarify teacher unsafe-rate aggregation | Mostly complete |
| Small Task 7 | Reviewer 29, comment 7 | Complete the final VLM reproducibility specification | Open |
| Small Task 8 | Reviewer 29, comment 9 | Separate hardware-observable and simulation-privileged unsafe signals | Open |
| Small Task 9 | Reviewer 29, comment 10 | Add a compact limitations paragraph | Paragraph and response added; highlighted screenshot pending |
| Small Task 10 | Reviewer 31, m1 | Correct inconsistent line spacing and audit formatting | Complete |
| Small Task 11 | Reviewer 31, m3 | Improve Figure 4 readability and justify the two displayed objects | Open |

## Small Task 1 — Maintain empirical safety language

**Reviewer item:** Reviewer 29, comment 1

> The revision appropriately removes formal 'safety-critical' claims. Please
> maintain this discipline throughout the manuscript and consistently describe
> the method as empirical risk reduction under task-specific unsafe-event
> definitions.

**Status:** Complete. The response to Reviewer 29, Comment 1 reaffirms the
empirical scope of the safety claims and points to the existing Methods
statement about teacher takeover.

- [x] Retain safety as empirical reduction in the four task-specific
      unsafe-event categories.
- [x] Point to the existing Methods statement that teacher takeover is
      empirically safer rather than an absolute safety guarantee.
- [x] State explicitly in the response that the framework provides no formal
      safety or constraint-satisfaction guarantees.
- [x] Replace the response drafting checklist with the finalized response.

## Small Task 2 — Prominently report the unseen-object limitation

**Reviewer item:** Reviewer 29, comment 2

> Real-world unsafe-event rates on unseen objects remain around 39%, which is
> substantial. This limitation should be emphasized prominently in the
> abstract, discussion, and conclusion to avoid implying deployment-ready
> safety.

**Status:** Complete.

- [x] Add the reported 39.2% unsafe-event rate on unseen objects to the abstract.
- [x] Retain the Results discussion of the unseen-object generalization gap.
      The Limitations paragraph also reports the 39.2% rate.
- [x] Identify contact-strategy mismatch as a future-work priority in the Conclusion.
- [x] Quote the abstract, Results, and Conclusion in the Comment 2 response.

## Small Task 3 — Quantify the physical (e) versus (f) comparison

**Reviewer item:** Reviewer 29, comment 3

> The real-robot difference between VLM-guided and fixed-threshold critic
> policies appears modest. Report confidence intervals and paired or proportion
> tests to determine whether the observed unsafe-rate reductions are
> statistically distinguishable.

- [ ] Determine whether trials for (e) and (f) were genuinely paired by object,
      seed, pose, and other initial conditions.
- [ ] Do not call the analysis paired unless those trial-level conditions match.
- [ ] Recompute lift-success and unsafe-event rates for seen and unseen objects.
- [ ] Report effect sizes for (f) minus (e), not only separate percentages.
- [ ] Add appropriate confidence intervals that account for object-level
      clustering and repeated trials.
- [ ] Use a paired test only if justified; otherwise use a suitable two-sample
      or clustered/hierarchical analysis.
- [ ] State plainly if the observed reduction is not statistically
      distinguishable.

## Small Task 4 — Analyze critic false negatives

**Reviewer item:** Reviewer 29, comment 4

> The Bellman critic achieves a 5.8% false-negative rate on unsafe episodes.
> Please discuss the consequences of these missed warnings and whether threshold
> adjustment can trade task success for lower false-negative risk.

- [ ] Verify that `5.8%` is calculated over unsafe episodes and record the exact
      numerator and denominator.
- [ ] Inspect missed-warning episodes and summarize their unsafe-event types.
- [ ] Explain that a false negative can prevent critic-triggered takeover, while
      the disagreement branch may still trigger intervention.
- [ ] If saved critic scores are available, sweep the critic threshold.
- [ ] For each threshold, report false-negative rate, detection rate,
      intervention/takeover rate, lift success, and unsafe-event rate.
- [ ] Discuss the empirical safety–task-success–autonomy tradeoff without
      implying a formal guarantee.

## Small Task 5 — Measure how early the Bellman critic warns before unsafe termination

**Reviewer item:** Reviewer 29, comment 5

> Clarify whether critic metrics are computed at the episode or time-step level
> and how early an unsafe event is detected before termination. Warning lead
> time is important for intervention usefulness.

Here, `critic` means the learned **Bellman success-value critic**
`Q_succ(s_t, a_t^S)`, not the VLM. At every control step, it estimates whether
the student's current state and proposed action are likely to lead to a safe,
successful lift. A value below the critic threshold is a `critic warning` and
requests teacher takeover.

The reviewer is asking whether the reported `5.8%` false-negative rate means:

1. `episode-level`: 5.8% of unsafe episodes received no critic warning before
   termination; or
2. `timestep-level`: 5.8% of individual unsafe timesteps were classified
   incorrectly.

Our existing description appears to use the first definition, but this must be
verified from the evaluation code and stated explicitly. The reviewer also
wants to know whether a correct warning arrives early enough for teacher
takeover to change the outcome. A warning one step before termination may count
as detection while offering almost no practical reaction time.

For every unsafe episode, identify:

- `t_warning`: the first timestep at which `Q_succ` crosses the intervention
  threshold; and
- `t_unsafe`: the timestep at which the first unsafe event causes termination.

Then calculate

`warning lead time = (t_unsafe - t_warning) / 60` seconds,

because the environment is checked at 60 Hz. Only warnings occurring before
the unsafe event count as advance warnings. Episodes with no prior threshold
crossing are false negatives.

- [ ] Verify from the evaluation code that the reported `5.8%` false-negative
      rate is episode-level, and record its exact numerator and denominator.
- [ ] Extract `t_warning` and `t_unsafe` for every unsafe episode from the saved
      timestep-level critic scores and termination logs.
- [ ] Report lead time in both control steps and seconds, including the median,
      interquartile range, and preferably the 10th--90th percentile.
- [ ] Report the fraction of unsafe episodes warned at least `0.1 s`, `0.25 s`,
      and `0.5 s` before termination, plus the fraction receiving no warning.
- [ ] Explain that this analysis measures whether the critic warning is early
      enough to be operationally useful; it does not establish a safety
      guarantee.
- [ ] If timestep-level scores or timestamps were not saved, state that lead
      time cannot be reconstructed and disclose this as a limitation.

## Small Task 6 — Clarify teacher unsafe-rate aggregation

**Reviewer item:** Reviewer 29, comment 6

> The teacher policy is implicitly treated as a safe fallback, yet teacher
> interventions can still generate unsafe contacts. Report teacher unsafe-event
> rates and explain what happens when teacher and critic recommendations
> conflict.

This concern is already substantially addressed in the previous response and
revised manuscript: teacher takeover is explicitly described as empirically
safer rather than guaranteed safe, and the method defines a conservative OR
rule under which either high teacher--student disagreement or low critic value
triggers intervention. Neither signal cancels the other.

The numerical scope is now corrected. Table II reports an `11.4%` all-40-object
unsafe-event mean, decomposed into `2.1%` harmful collision, `8.0%` object
escape, `1.2%` palm flipped, and `0.1%` hand too far. Its caption states that
the Mean column is computed over all 40 objects.

- [x] Compute or recover the aggregate teacher unsafe-event rate across all 40
      objects using the same episode-level definition and evaluation protocol.
- [x] Report the all-40-object aggregate in Table II and state its population in
      the caption; coordinate this with Major Task 1.
- [ ] In the new response, point to the existing safety-limitation and OR-rule
      text, and state that only the evaluation population/aggregation has been
      clarified.

## Small Task 7 — Complete VLM reproducibility details

**Reviewer item:** Reviewer 29, comment 7

> Provide the final exact VLM identifier, prompt, decoding settings,
> visual-sample selection rules, update interval, latency distribution, failure
> handling, and cost in the main paper or permanent supplementary material.

- [ ] Record the exact provider and immutable model/version identifier used in
      the reported experiments.
- [ ] Include the complete system and user prompt without omissions.
- [ ] Report temperature, top-p, token limits, seed if supported, image detail or
      resolution settings, and all other decoding parameters.
- [ ] Define exactly which frames/views are selected and how they are
      preprocessed.
- [ ] State the threshold-update interval and total number of calls per run.
- [ ] Document output parsing, validation, clipping, smoothing, and application
      of updated thresholds.
- [ ] Report latency as a distribution rather than only one representative
      value.
- [ ] Report failure, timeout, retry, and fallback behavior.
- [ ] Report measured or reconstructed API cost and the date/price basis used.
- [ ] Ensure these details appear in a permanent supplement, not only an
      ephemeral service or external link.

## Small Task 8 — Separate hardware-observable and privileged unsafe signals

**Reviewer item:** Reviewer 29, comment 9

> The current unsafe-event taxonomy is task-specific. Clarify which events are
> directly sensor-observable on hardware and which depend on privileged
> simulation signals during training or evaluation.

- [ ] Create a table with one row per unsafe event: harmful collision, object
      escape, palm flip, and hand-too-far.
- [ ] For simulation, list the exact privileged state/contact quantities and
      thresholds used to detect each event.
- [ ] For hardware, list the sensor, estimator, or annotation used to detect each
      event.
- [ ] State whether hardware outcomes are detected online or labeled offline.
- [ ] Identify events whose simulation and hardware definitions are only
      approximations rather than equivalent measurements.
- [ ] Clarify which privileged signals are available only during teacher
      training/distillation and are absent from the deployed RGB student.

## Small Task 9 — Add a compact limitations paragraph

**Reviewer item:** Reviewer 29, comment 10

> Please add a compact limitations paragraph covering the remaining sim-to-real
> contact-strategy mismatch, external VLM dependence, task-specific safety
> definitions, and absence of formal constraint guarantees. No major
> methodological restructuring appears necessary.

- [x] Cover the contact-rich sim-to-real mismatch, especially on unseen objects.
- [x] State the dependence on an external proprietary VLM, including possible
      model/version drift, latency, availability, and cost.
- [x] State that the unsafe-event definitions are task-specific and incomplete
      as a general robot-safety specification.
- [x] State that the method provides empirical intervention, not formal
      constraint satisfaction or safety guarantees.
- [x] Mention that the VLM, teacher, and critic are used during simulation
      distillation and are not runtime physical safety monitors.
- [x] Keep the paragraph visible in the main paper rather than placing all
      limitations only in the supplement.

- [ ] Attach a screenshot of the Limitations paragraph from the highlighted
      manuscript to the response; a red TODO remains under Comment 10.

## Small Task 10 — Correct manuscript formatting

**Reviewer item:** Reviewer 31, m1

> One paragraph in Sec. III-A has a line spacing that differs from the rest of
> the text. Please check the formatting of the entire manuscript.

- [x] Inspect every paragraph in Section III-A in the current rendered PDF.
- [x] Check local spacing, font-size, manual line-break, and environment
      commands: no body-text spacing override was found; the local `\small`
      command is scoped to the displayed objective equation.
- [x] Confirm no accidental local paragraph-formatting override requires removal.
- [x] Visually inspect every page of the current manuscript for inconsistent
      line spacing, font size, margins, table scaling, and caption formatting.
- [x] Add the formatting-audit response under Reviewer 31, Minor Comment m1.

The current eight-page manuscript passed the visual audit. Repeat the final
submission check on both clean and highlighted PDFs after all remaining edits.

## Small Task 11 — Improve Figure 4 and justify its object subset

**Reviewer item:** Reviewer 31, m3

> Fig. 4 is difficult to read at print quality. Please also explain why only two
> objects (windcart and cow) are shown.

- [ ] Improve Figure 4 quality from the original plotting source: enlarge the
      legend and fonts, export at publication quality, and avoid
      quality-reducing image compression.
- [ ] Regenerate Figure 4 with print-readable fonts, line widths, markers,
      colors, and panel labels at the final column/page size.
- [ ] Prefer vector output where practical and verify readability in a printed or
      100%-zoom PDF view.
- [ ] Reduce visual density or move detailed panels to the supplement if needed.
- [x] Document the selection rationale in the m3 response: WindCart and Cow are
      illustrative examples; more objects would make the plots too dense.
      Point to Table III for the aggregate comparison over all 40 objects.
- [x] State that the two objects are illustrative examples of failure-mode
      dynamics during training.
- [ ] Consider adding all-object or additional-object failure-mode results to
      the supplement.

## Reviewer items tracked in the major TODO

The following comments are intentionally not duplicated here:

- Reviewer 29, comment 8 and Reviewer 31, M4: VLM contribution and novel scene
  semantics — [`TODO.md`, Task 5](TODO.md#task-5--assess-the-evidence-for-the-distinct-vlm-contribution).
- Reviewer 31, m2: inconsistent `Mean` populations and four-object selection —
  [`TODO.md`, Task 1](TODO.md#task-1--unify-mean-in-tables-ii-and-iii).
- Reviewer 31, M3: Figure 3 versus Table III —
  [`TODO.md`, Task 2](TODO.md#task-2--resolve-figure-3-versus-table-iii).
- Reviewer 31, M1: exact teacher reward formulation —
  [`TODO.md`, Task 3](TODO.md#task-3--document-the-exact-teacher-training-reward).
- Reviewer 31, M2: RL-recipe superiority, DextrAH/FABRICS fairness, and the
  follow-up teacher-only verification experiment —
  [`TODO.md`, Task 4](TODO.md#task-4--withdraw-the-unsupported-rl-recipe-superiority-claim).
