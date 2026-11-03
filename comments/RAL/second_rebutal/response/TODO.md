# Second rebuttal TODO

## Task index

| Task | Reviewer item | Problem | Status |
|---|---|---|---|
| Task 1 | Reviewer 31, m2 | Unify the definition and population of `Mean` in Tables II and III and document the four-object selection | Problem identified; verification and correction needed |
| Task 2 | Reviewer 31, M3 | Resolve or explain the apparent inconsistency between Figure 3 and Table III | Working explanation identified; raw-data verification needed |
| Task 3 | Reviewer 31, M1 | Make teacher-policy reward formulation reproducible | Add exact implemented equations, weights, and scales to the appendix |
| Task 4 | Reviewer 31, M2 | Resolve the unsupported RL-recipe superiority claim and unfair DextrAH/FABRICS comparison | Preferred route: withdraw the superiority claim and avoid a new embodiment-specific FABRICS port |
| Task 5 | Reviewer 31, M4; Reviewer 29, comment 8 | Determine whether the evidence sufficiently supports the distinct VLM contribution across visual contexts and unsafe scenarios | Open question; do not defend or narrow the claim until existing data are audited |

Add future review items as `Task 3`, `Task 4`, and so forth. Each task should
retain the original reviewer comment, identify the exact problem, list required
checks, and provide a response only after its factual assumptions are verified.

## Task 1 — Unify “Mean” in Tables II and III

**Reviewer item:** Reviewer 31, m2

**Status:** Problem identified; correction and selection rationale still needed.

### Reviewer 31's original comment

> **m2.** The “Mean” columns of Table II and Table III appear to average over
> different populations. Please unify the definition of “Mean” across the two
> tables. In addition, please briefly state why these four objects were selected
> from the 40-object set.

### Confirmed problem

The reviewer is correct that the two tables use `Mean` for different
populations:

- **Table II:** `Mean` is the arithmetic mean of the four displayed objects:
  WindCart, Boot, ToolBox, and Cow.
- **Table III:** `Mean` is calculated over all 40 objects, not only the four
  displayed objects.

For example, Table II's reported teacher unsafe-rate mean is:

```text
(6.5 + 13.5 + 13.5 + 13.5) / 4 = 11.75% -> 11.8%
```

This exactly matches the reported `11.8%`, confirming that Table II averages
the four displayed objects.

In contrast, Table III reports `11.9%` for ablation (e), although the four
displayed unsafe rates give:

```text
(7.5 + 15.0 + 15.5 + 12.0) / 4 = 12.5%
```

Similarly, Table III reports `9.3%` for ablation (f), while its four displayed
objects give:

```text
(6.0 + 10.5 + 11.0 + 8.5) / 4 = 9.0%
```

The Table III values may be valid all-40-object aggregates, but labeling both
tables simply as `Mean` makes their populations appear identical. A reader
cannot determine the denominator or reproduce the values from the displayed
columns.

### Four-object selection problem

The manuscript calls WindCart, Boot, ToolBox, and Cow “representative,” but it
does not state how or when they were selected. This leaves open whether the
objects were:

- selected before inspecting the comparative results;
- randomly selected;
- chosen to span different geometries, contact configurations, or difficulty;
- inherited from an earlier experimental protocol; or
- selected after observing favorable results.

The actual selection procedure must be documented. Do not invent a
representativeness criterion after the fact.

### Required checks and corrections

- [ ] Confirm from the aggregation code that Table III's final column is an
      all-40-object result.
- [ ] Determine whether the all-40 result is a macro-average of object-level
      rates or a micro/pooled rate over all episodes.
- [ ] Record how seeds are combined and report the number of episodes per
      object and per method.
- [ ] Locate or calculate the corresponding all-40-object teacher results for
      Table II.
- [ ] Preferably use the same final-column population in both tables and label
      it explicitly, for example `All-40-object mean`.
- [ ] If the populations cannot be unified, use explicit distinct labels such
      as `Mean of four displayed objects` and `All-40-object mean`, and explain
      the difference in both captions.
- [ ] Document the true selection rationale for WindCart, Boot, ToolBox, and
      Cow, including whether the selection was fixed before examining results.
- [ ] Consider providing results for all 40 objects in the supplement to remove
      any appearance of selective reporting.

### Proposed response after verification

> We thank the reviewer for identifying the ambiguous use of “Mean.” In the
> submitted manuscript, Table II averaged the four displayed objects, whereas
> Table III reported an aggregate over all 40 objects. We have corrected this
> inconsistency by using the same [macro/pooled] all-40-object definition in
> both tables and by renaming the column “All-40-object mean.” We have also
> specified the episode and seed aggregation procedure in the captions. The
> four displayed objects were selected [insert the verified, factual selection
> rationale], and the complete object-level results are provided in the
> supplementary material.

Do not finalize this response until the aggregation method and object-selection
rationale have been verified.

## Task 2 — Resolve Figure 3 versus Table III

**Reviewer item:** Reviewer 31, M3

**Status:** Unresolved pending verification of the source logs and aggregation
scripts.

### Reviewer 31's original comment

> **M3.** The unsafe rates in Fig. 3 and Table III are inconsistent. In the
> “Comparison Unsafe Episode Rate” panel of Fig. 3, (c) is the highest, (b) and
> (e) are nearly indistinguishable, and (f) is the lowest. In contrast, Table III
> reports (b) 17.4 > (c) 16.7 > (e) 11.9 > (f) 9.3, which differs in both values
> and ordering. Please revise so that the two results are consistent with each
> other.

### What the figure actually shows

The curve-to-method mapping in the Figure 3 caption is:

| Color | Method | Ablation |
|---|---|---|
| Blue | Vanilla DAgger | (b) |
| Orange | Vanilla SafeDAgger | (c) |
| Green | DexSafeDagger | (e) |
| Red | VLM-DexSafeDagger | (f) |

At the end of the plotted training trajectory, the visible ordering is
approximately:

```text
orange > blue > green > red
   (c) >  (b) >  (e) > (f)
```

Table III reports:

```text
(b) 17.4% > (c) 16.7% > (e) 11.9% > (f) 9.3%
```

Thus, Figure 3 is not internally inconsistent. The apparent conflict is that
the ordering of (b) and (c) differs between Figure 3 and Table III. The figure
also makes (b) and (e) look relatively close, whereas Table III separates them
by 5.5 percentage points.

### Working explanation to verify

Figure 3 and Table III appear to report different experimental measurements:

- **Figure 3:** unsafe-event rates observed during online student distillation,
  plotted over training iterations and possibly smoothed or averaged over a
  training window.
- **Table III:** a separate post-training evaluation of frozen student policies,
  using 200 evaluation episodes per displayed object. Its `Mean` column may be
  aggregated over all 40 objects rather than only the four displayed objects.

Different rollout phases, checkpoints, populations, and aggregation rules can
legitimately produce different values and even a different ordering. If this is
confirmed, the issue is primarily insufficient labeling and explanation, not a
requirement that the two results be numerically identical.

### Required checks

- [ ] Locate the raw data and plotting script used for Figure 3.
- [ ] Record the Figure 3 objects, seeds, episode denominator, smoothing method,
      checkpoint/window, and whether unsafe rates are measured during active
      online training.
- [ ] Locate the raw evaluation data and aggregation script used for Table III.
- [ ] Record the Table III objects, seeds, checkpoint, number of evaluation
      episodes, and whether the policy is frozen and intervention is disabled.
- [ ] Verify whether Table III's `Mean` is calculated over the four displayed
      objects or all 40 objects.
- [ ] Recompute both outputs from the raw logs without manually altering their
      ordering.
- [ ] Confirm that the color-to-ablation mapping in Figure 3 is correct.
- [ ] If both outputs are correct but measure different phases, revise the
      Figure 3 and Table III captions to state those differences explicitly.
- [ ] If they were intended to report the same measurement, identify and fix
      the plotting, transcription, or aggregation error and regenerate both
      outputs from one source of truth.

### Proposed response if the working explanation is confirmed

> We thank the reviewer for identifying this ambiguity. Figure 3 and Table III
> report two distinct evaluations. Figure 3 shows unsafe-event rates observed
> during online distillation as a function of training iteration, whereas Table
> III reports a separate post-training evaluation of frozen student policies
> over 200 episodes per object. Consequently, the two measurements use different
> rollout phases and aggregation populations and are not expected to have
> identical values or ordering. We have revised the figure and table captions,
> as well as the surrounding text, to state the evaluation phase, population,
> checkpoint/window, and aggregation procedure explicitly.

Do not use this proposed response until the raw logs and scripts confirm every
technical statement in it.

## Task 3 — Document the exact teacher-training reward

**Reviewer item:** Reviewer 31, M1

**Status:** Resolution selected; appendix equations still need to be written and
verified against the implementation.

### Reviewer 31's original comment

> **M1.** The reward for teacher-policy training is described only verbally.
> Table I lists only the purpose of each reward term; the exact formulation,
> weights, and scales of the terms are not given in the manuscript. Since
> teacher training is the starting point of every subsequent stage, the work
> does not appear reproducible in its current form. Please provide the exact
> formulation and weights of each reward term.

### Confirmed problem

Table I currently lists the names and qualitative purposes of the teacher reward
terms, but it does not give sufficient mathematical detail to reproduce the
implemented reward:

```text
r_dist, r_curl, r_align, r_contact,
r_near, r_goal, r_lift, r_action
```

The missing information includes the exact expression for each term and its
numerical coefficient. Where applicable, the description must also identify
normalization, clipping, sign conventions, activation conditions, thresholds,
and the timestep at which the term is evaluated. A verbal description such as
“rewards stable contact” is not independently reproducible.

### Selected resolution

Add a reward-formulation subsection or table to the appendix containing:

1. the complete mathematical equation for the total teacher reward;
2. the exact equation for every individual reward term;
3. every numerical weight and scale;
4. all constants, thresholds, clipping ranges, and normalization rules;
5. the condition under which each sparse or staged term becomes active; and
6. the implemented treatment of unsafe termination, timeout, and return
   bootstrapping where it affects the reward or target return.

Keep the compact qualitative reward table in the main manuscript, but add an
explicit pointer from Table I or the teacher-training paragraph to the detailed
appendix equations.

### Required checks and edits

- [ ] Locate the reward implementation and its associated configuration file.
- [ ] Extract the implemented equation for each of the eight named reward
      terms; do not reconstruct equations from memory.
- [ ] Record the exact coefficient, scale, sign, unit, clipping behavior, and
      activation condition for every term.
- [ ] Write the total reward as an explicit weighted sum and define every
      variable used in the equations.
- [ ] Verify whether rewards are calculated before or after the state
      transition and whether any term is applied only at termination.
- [ ] State how unsafe termination and timeout affect the return, including
      whether truncated transitions are bootstrapped.
- [ ] Cross-check every appendix equation and value against the exact code and
      configuration used to train the submitted teacher policies.
- [ ] Add a cross-reference from the main-paper teacher-training description
      and Table I to the new appendix subsection.
- [ ] Rebuild the manuscript and supplement and verify that all equations,
      symbols, and cross-references render correctly.

### Proposed response after implementation verification

> We thank the reviewer for identifying this reproducibility gap. We have added
> the exact mathematical formulation of the teacher-training reward to
> Supplementary Section [X]. The new section defines all eight reward terms,
> their numerical coefficients and scales, activation conditions,
> normalization and clipping rules, and the treatment of unsafe termination
> and timeout. We have also added an explicit cross-reference from Table I and
> the teacher-training description in the main manuscript. All equations and
> values were verified against the implementation and configuration used to
> train the reported teacher policies.

Do not finalize this response until every appendix equation and coefficient has
been checked against the actual training code and configuration.

## Task 4 — Withdraw the unsupported RL-recipe superiority claim

**Reviewer item:** Reviewer 31, M2

**Status:** Analysis completed; preferred resolution is to withdraw the
intrinsic RL-superiority claim, subject to final author/supervisor approval.

### Reviewer 31's original comment

> **M2. The claimed superiority of the authors' RL recipe is not supported.**
>
> (1) The authors explain the performance gap between ablations (a) and (b) by
> stating that the FABRICS controller was tuned for the original platform and
> transfers poorly to the new hardware. This implies that the DexTrAH baseline
> was not tuned for the authors' hardware, and therefore the comparison cannot
> serve as evidence that the authors' recipe produces more effective teacher
> policies. A comparison against a DexTrAH baseline re-tuned for the authors'
> platform, or additional experiments and analysis that can demonstrate the
> superiority of the recipe, is required.
>
> (2) The difference between the “DexTrAH-RGB-style RL recipe” and “our RL
> recipe” is not defined in the manuscript. Please state explicitly how the two
> recipes differ.
>
> (3) The second contribution claims “a safety-aware RL reward design that
> explicitly accounts for risky events.” However, the reward terms in Table I
> are generic shaped-reward terms, and no term explicitly penalizes the unsafe
> events defined by the authors, such as collisions or object escape. Early
> termination does penalize unsafe events implicitly by truncating the future
> return, but it is indistinguishable from a timeout unless truncation is
> bootstrapped. The manuscript does not specify any of these. Please either add
> an ablation of the reward terms or of the termination conditions, or moderate
> the contribution statement.

### Confirmed problem

The submitted manuscript compares a DextrAH-RGB-style teacher-training setup
against the customized teacher-training setup and interprets the difference as
evidence that the customized RL recipe is superior. However, the manuscript
also states that the DextrAH/FABRICS controller was specialized for its original
robot and transfers poorly to the Tiangong-2 Pro and InspireHand platform.

This creates a confound:

```text
observed performance difference
    = RL-recipe difference
    + controller/embodiment adaptation difference
    + possibly other implementation differences
```

The current comparison therefore cannot isolate the quality of the two RL
recipes. Ablations (a) versus (b), or (d) versus (e), do not establish intrinsic
RL-recipe superiority when the underlying controller is not equally adapted to
the target hardware.

### Reproducibility and feasibility analysis

The public DextrAH and FABRICS releases provide a Kuka--Allegro-specific
implementation, including an Allegro PCA action space, collision model,
controller gains, dynamic limits, and deployment scaffolding. DextrAH-G derives
the Allegro action manifold by retargeting human grasp sequences from the public
DexYCB dataset and applying PCA. The underlying data are therefore not properly
described as closed-source teleoperation data.

Nevertheless, a fair Tiangong--InspireHand port is not a simple hyperparameter
retuning exercise. It would require a new embodiment-specific fabric and
validation effort, including:

- a Tiangong--InspireHand robot and simulator integration;
- an InspireHand-specific action manifold or PCA map;
- collision spheres and self-collision pairs;
- posture, attraction, damping, and collision parameters;
- joint, acceleration, jerk, and low-level control limits;
- hardware and simulator interfaces; and
- matched RL tuning and evaluation under a controlled compute budget.

An inadequately ported fabric would not provide a fairer baseline. A complete
port would be a substantial separate robotics engineering project and is not
necessary to evaluate the paper's central intervention-policy contribution.

### Preferred resolution

Withdraw the claim that the customized RL teacher-training recipe is
intrinsically superior to DextrAH. Treat the teacher-training recipe as a fully
specified implementation choice rather than an independent contribution.

This route avoids a large new FABRICS port while making the scientific claim
match what the current experiment can establish.

The current DextrAH-based results may be retained only if they are clearly
described as an embodiment-mismatched or DextrAH-inspired transferred
implementation. They must not be used as evidence of general RL-recipe
superiority. If that qualification makes the comparison confusing or
unhelpful, remove ablations (a) and (d) from the primary contribution argument.

The intervention-policy comparisons should instead emphasize methods that use
the same teacher setup, so that the intervention mechanism is isolated:

```text
(c) disagreement-only SafeDAgger
(e) disagreement + Bellman critic
(f) full VLM-guided adaptation
(g) LLM-only adaptation
(h) non-VLM adaptive curriculum
```

### Required claim and manuscript audit

- [ ] Obtain final author/supervisor approval to withdraw the RL-superiority
      claim rather than implement a new Tiangong--InspireHand FABRICS baseline.
- [ ] Remove the research question asking whether the customized RL recipe
      produces stronger teachers than the DextrAH-RGB-style recipe.
- [ ] Remove statements that the experiments demonstrate intrinsic superiority
      of the customized RL recipe.
- [ ] Remove teacher-recipe superiority from the contribution list, abstract,
      introduction, results, discussion, conclusion, cover letter, and response.
- [ ] Decide whether to retain ablations (a) and (d) as qualified implementation
      references or remove them from the main comparison.
- [ ] If retained, relabel them accurately as a `DextrAH-inspired transferred
      implementation` or equivalent wording, and state the embodiment mismatch.
- [ ] Add a compact table describing the factual implementation differences
      between the transferred DextrAH-inspired setup and the customized teacher
      setup, without interpreting the difference as superiority.
- [ ] Keep teacher policies and all teacher-training settings fixed across the
      intervention comparisons used to support the central contribution.
- [ ] Audit the separate “safety-aware RL reward” claim. Unless an explicit
      unsafe-event reward or a supporting reward/termination ablation exists,
      moderate or remove this contribution claim as Reviewer 31 requests.
- [ ] Ensure Task 3 still provides the exact teacher reward equations and
      weights for reproducibility even after the superiority claim is removed.

### Proposed response if the preferred resolution is approved

> We agree with the reviewer that the submitted comparison does not isolate the
> intrinsic quality of the two RL training recipes. The publicly released
> DextrAH/FABRICS controller is designed and parameterized for the
> Kuka--Allegro embodiment. Our transferred implementation on the
> Tiangong-2 Pro and InspireHand therefore confounds the RL recipe with
> embodiment-specific controller adaptation. A faithful comparison would
> require constructing and validating a new InspireHand-specific fabric rather
> than merely retuning RL hyperparameters. We have consequently removed the
> claim that our RL recipe is superior and no longer present the teacher recipe
> as an independent contribution. We now describe it as the implementation used
> to produce the teacher policies and focus the controlled analysis on
> intervention methods that share the same teacher setup. We also explicitly
> document the recipe and reward formulation for reproducibility.

The response must not claim that DextrAH depends on unavailable closed-source
teleoperation data. Its Allegro PCA space is derived from the publicly available
DexYCB human-grasp dataset, although a fair InspireHand-specific port would
still require substantial embodiment-specific design and validation.

## Task 5 — Assess the evidence for the distinct VLM contribution

**Reviewer items:** Reviewer 31, M4; Reviewer 29, comment 8

**Status:** Open question. No final decision has been made about defending,
narrowing, or removing the visual-context contribution claim.

### Reviewer 31's original comment

> **M4.** The contribution of the VLM is not established by the (e) vs. (f)
> comparison alone. In particular, the third contribution claims effectiveness
> “across different visual contexts and unsafe scenarios,” but the results
> currently presented do not clearly verify this claim. Please either moderate
> the corresponding contribution statement or provide additional analysis.

### Reviewer 29's related comment

> The ablations convincingly motivate visual-semantic adaptation on
> representative training objects. Please state more explicitly whether the VLM
> adaptation itself was evaluated on novel scene semantics, rather than only
> novel object geometries.

### Author's intended meaning

The phrase “across different visual contexts and unsafe scenarios” was intended
to refer to:

- **Visual contexts:** randomized object geometries, textures, materials, and
  lighting conditions.
- **Unsafe scenarios:** the four predefined task-specific unsafe-event
  categories: harmful collision, object escape, palm flip, and hand-too-far.

The intended claim is therefore not that the VLM has been evaluated on every
possible real-world semantic context. It is that the method is trained and/or
evaluated under varied simulated visual conditions and is assessed using four
unsafe-event definitions.

### Current analysis

The intended meaning can be stated more explicitly, but the reviewer's concern
appears to be evidentiary rather than purely terminological. Randomizing visual
conditions demonstrates exposure to a diverse distribution; it does not, by
itself, demonstrate that visual input causes the VLM's improvement within each
context. Similarly, defining four unsafe-event categories does not establish
that the VLM improves every category.

The current argument may appear to a reader as:

```text
visual conditions were randomized
+ four unsafe-event categories were defined
+ the full VLM has the best aggregate mean
= the VLM is effective across visual contexts and unsafe scenarios
```

The missing evidentiary link is a result that connects the full VLM's visual
input to improvements within the relevant visual conditions or unsafe-event
categories.

The existing ablation ladder is conceptually useful:

```text
(e) fixed critic-based intervention
(h) adaptive non-VLM curriculum
(g) LLM-only adaptation without images
(f) full VLM adaptation with images
```

However, the reported aggregate unsafe rates are:

```text
(e) 11.9%
(h) 11.7%
(g) 10.2%
(f)  9.3%
```

The direct image-specific comparison is therefore (f) versus (g), with a
reported difference of only 0.9 percentage points. The existing five-seed
analysis covers (b), (c), (e), and (f), but not (g) or (h). The current material
does not establish whether the 0.9-point difference is repeatable or within
run-to-run variation.

### Distinctions that must be made explicit

The revision must distinguish among three levels of evidence:

1. **Exposure:** the policy was trained under randomized visual conditions.
2. **Aggregate performance:** the full method achieved the best aggregate mean
   under a specified training or evaluation distribution.
3. **VLM-specific contextual benefit:** visual input produced a reliable
   improvement within or across particular visual-context groups.

The existing paper appears to support the first two more directly than the
third. It must also distinguish novel object geometry from novel scene
semantics and clarify that the VLM is used during simulation distillation, not
as a runtime physical-robot safety monitor.

### Open factual questions

- [ ] Were textures, materials, lighting, and object conditions randomized only
      during training, or also during the evaluation that produced Table III?
- [ ] What exact ranges and distributions were used for each visual
      randomization variable?
- [ ] Were all ablations evaluated under identical sampled visual contexts,
      objects, seeds, checkpoints, and rollout budgets?
- [ ] Do the stored logs identify lighting, texture, material, object, or other
      visual-condition groups well enough for stratified reanalysis?
- [ ] Can the existing results be grouped by the four unsafe-event categories
      for methods (e), (f), and (g), rather than only reported as an aggregate?
- [ ] Were (g) and (h) run with the same independent seeds as (f)?
- [ ] Is the reported 0.9-point (f) versus (g) difference larger than matched
      run-to-run uncertainty?
- [ ] Does the VLM receive information that is meaningfully different across
      the randomized visual conditions, and do its threshold updates respond to
      those differences?
- [ ] Does any existing experiment test novel scene semantics, or only novel
      object geometry?

### Candidate resolution paths — decision still open

**Path A: Defend the claim using existing data.** If the logs permit it,
reanalyze existing runs by visual-condition group, object/object family, and
unsafe-event category. Report matched (f) versus (g) differences and
uncertainty. This may resolve the concern without new training.

**Path B: Add stronger controlled experiments.** Run (f), (g), and (h) with
matched seeds and protocols. Consider a correct-image versus shuffled- or
irrelevant-image control and report confidence intervals and intervention
budgets.

**Path C: Narrow the wording.** If contextual or matched-seed evidence is not
available, replace the broad causal claim with a directly measurable statement,
for example:

> Under randomized object geometry, texture, material, and lighting conditions,
> VLM-DexSafeDagger achieves the lowest aggregate unsafe-event rate among the
> evaluated intervention strategies. Unsafe events are evaluated using four
> task-specific categories: harmful collision, object escape, palm flip, and
> hand-too-far.

This wording is valid only if the reported evaluation itself uses the stated
randomized conditions. If randomization was applied only during training, use
“trained under randomized visual conditions” instead of claiming evaluation
across those contexts.

### Decision gate

Leave this task open until the raw logs, randomization configuration, seed
coverage, and unsafe-mode breakdown have been inspected. Do not yet assert that
the reviewer overlooked existing evidence, and do not prematurely remove the
VLM contribution. The final response should be chosen based on what the stored
data can actually demonstrate.
