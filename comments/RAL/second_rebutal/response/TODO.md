# Second rebuttal TODO

## Required final outputs

All rebuttal work must culminate in these four deliverables under the project
`output/` directory:

- [ ] `output/main.pdf` — clean revised manuscript
- [ ] `output/main_highlighted.pdf` — revision-marked manuscript compared against the
      last submitted revision (`first_rebutal/output/revision/main.pdf`), using
      yellow highlight stripes with no blue additions or red strikeouts
- [ ] `output/response.pdf` — point-by-point response to the reviewers
- [ ] `output/appendix.pdf` — standalone supplementary material

Do not consider the rebuttal complete until all four PDFs build successfully
and have been checked for content and layout.

## Task index

| Task | Reviewer item | Problem | Status |
|---|---|---|---|
| Task 1 | Reviewer 31, m2 | Unify the definition and population of `Mean` in Tables II and III and document the four-object selection | Complete: all-40 means unified and object selection explained |
| Task 2 | Reviewer 31, M3 | Resolve or explain the apparent inconsistency between Figure 3 and Table III | Complete: training/post-training scope clarified in both captions; response finalized with highlighted screenshots |
| Task 3 | Reviewer 31, M1 | Make teacher-policy reward formulation reproducible | Complete: exact equations and parameter table added to Appendix A.2; reviewer response finalized |
| Task 4 | Reviewer 31, M2 | Resolve the unsupported RL-recipe superiority claim and unfair DextrAH/FABRICS comparison | Claim audit complete; teacher-only verification retained as a follow-up experiment |
| Task 5 | Reviewer 31, M4; related Reviewer 29, comment 8 | Explain the distinct VLM contribution and the scope of visual contexts and unsafe scenarios | Complete: M4 response finalized using the ablation ladder, visual randomization, and Figure 4 decomposition; trade-off curve remains optional |

Add future review items as `Task 3`, `Task 4`, and so forth. Each task should
retain the original reviewer comment, identify the exact problem, list required
checks, and provide a response only after its factual assumptions are verified.

## Task 1 — Unify “Mean” in Tables II and III

**Reviewer item:** Reviewer 31, m2

**Status:** Complete. The all-40-object means and selection rationale are in
place, and the reviewer response is finalized.

### Reviewer 31's original comment

> **m2.** The “Mean” columns of Table II and Table III appear to average over
> different populations. Please unify the definition of “Mean” across the two
> tables. In addition, please briefly state why these four objects were selected
> from the 40-object set.

### Original confirmed problem

The reviewer was correct that the submitted tables used `Mean` for different
populations:

- **Table II:** `Mean` was the arithmetic mean of the four displayed objects:
  WindCart, Boot, ToolBox, and Cow.
- **Table III:** `Mean` was calculated over all 40 objects, not only the four
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

### Current correction

Table II now reports the verified all-40-object means: `91.7%` lift success,
`11.4%` unsafe rate, `2.1%` harmful collision, `8.0%` object escape, `1.2%`
palm flipped, and `0.1%` hand too far. The failure-mode means sum to the total
unsafe rate. Both Table II and Table III captions state that `Mean` is computed
over all 40 objects, and the four displayed objects are described as
illustrative rather than representative.

### Required checks and corrections

- [x] Confirm from the aggregation code that Table III's final column is an
      all-40-object result.
- [x] Locate or calculate the corresponding all-40-object teacher results for
      Table II.
- [x] Use the same final-column population in both tables and state explicitly
      in both captions that `Mean` is computed over all 40 objects.
- [x] Not applicable: the populations were unified, so distinct labels are not
      needed.
- [x] Document the true selection rationale for WindCart, Boot, ToolBox, and
      Cow, including whether the selection was fixed before examining results.
### Proposed response after verification

> We thank the reviewer for identifying the ambiguous use of “Mean.” In the
> submitted manuscript, Table II averaged the four displayed objects, whereas
> Table III reported an aggregate over all 40 objects. We have corrected this
> inconsistency by using the same all-40-object definition in
> both tables; both captions now state that `Mean` is computed over all 40
> objects. The four displayed objects are only a compact illustrative subset
> and were not selected using a statistical, difficulty-based, or
> performance-based criterion.

## Task 2 — Resolve Figure 3 versus Table III

**Reviewer item:** Reviewer 31, M3

**Status:** Complete. The training/post-training distinction is clarified in
both captions, and the M3 response is finalized with screenshots from the
highlighted manuscript.

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

### Resolution

- [x] Clarify that the unsafe-episode-rate panel in Figure 3 records online
      distillation rollouts, whereas Table III reports standalone evaluation
      of the resulting student-policy checkpoints after training.
- [x] Update the Figure 3 caption to describe evolution during online
      distillation and the Table III caption to specify 200 post-training
      evaluation episodes per object. The Mean columns cover all 40 objects.
- [x] Finalize the response to Reviewer 31 M3 in `response.tex` and include
      screenshots of both captions from the highlighted manuscript.

The figure supports reduced unsafe exploration during early distillation;
the table supports lower unsafe-event rates for the resulting student
policies in post-training evaluation. Their values and rankings need not
coincide because they assess different phases under different conditions.
The plotted curves and table values remain unchanged.

### Final response

See the finalized response to Reviewer 31 M3 in `response.tex` and the
highlighted caption screenshots embedded immediately after it.

## Task 3 — Document the exact teacher-training reward

**Reviewer item:** Reviewer 31, M1

**Status:** Complete.  Appendix A.2 now contains the verified reward equations
and parameter table, and the point-by-point response to Reviewer 31 M1 is
finalized.  The main manuscript remains unchanged by author decision.

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

- [x] Locate the reward implementation and its associated configuration file.
- [x] Extract the implemented equation for each of the eight named reward
      terms; do not reconstruct equations from memory.
- [x] Record the exact coefficient, scale, sign, unit, clipping behavior, and
      activation condition for every term.
- [x] Write the total reward as an explicit weighted sum and define every
      variable used in the equations.
- [x] Cross-check every appendix equation and value against the exact code and
      configuration used to train the submitted teacher policies.
- [x] Keep the compact main-paper presentation unchanged and point to the new
      appendix subsection from the finalized reviewer response.
- [x] Rebuild the response and supplement and verify that all equations,
      symbols, tables, and references render correctly.

### Final response

See the finalized response to Reviewer 31 M1 in `response.tex`.  It points to
Supplementary Section A.2 and Table 2, summarizes the eight exact reward terms
and their implementation parameters, and records that every equation and value
was verified against the submitted teacher-training implementation.

## Task 4 — Withdraw the unsupported RL-recipe superiority claim

**Reviewer item:** Reviewer 31, M2

**Status:** Claim and manuscript audit completed. The teacher-only verification
remains as the follow-up experiment below.

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

- [x] Obtain final author/supervisor approval to withdraw the RL-superiority
      claim rather than implement a new Tiangong--InspireHand FABRICS baseline.
- [x] Remove the research question asking whether the customized RL recipe
      produces stronger teachers than the DextrAH-RGB-style recipe.
- [x] Remove statements that the experiments demonstrate intrinsic superiority
      of the customized RL recipe.
- [x] Remove teacher-recipe superiority from the contribution list, abstract,
      introduction, results, discussion, conclusion, cover letter, and response.
- [x] Decide whether to retain ablations (a) and (d) as qualified implementation
      references or remove them from the main comparison.
- [x] If retained, relabel them accurately as a `DextrAH-inspired transferred
      implementation` or equivalent wording, and state the embodiment mismatch.
      **Not applicable:** both ablations were removed from the main comparison.
- [x] Add a compact factual description of the implementation differences
      between the transferred DextrAH-inspired setup and the customized teacher
      setup, without interpreting the difference as superiority. This is stated
      in response M2(1)--(2) and Supplementary Section D.1; a separate table is
      not required.
- [x] Keep teacher policies and all teacher-training settings fixed across the
      intervention comparisons used to support the central contribution.
- [x] Audit the separate “safety-aware RL reward” claim. Unless an explicit
      unsafe-event reward or a supporting reward/termination ablation exists,
      moderate or remove this contribution claim as Reviewer 31 requests.
- [x] Ensure Task 3 still provides the exact teacher reward equations and
      weights for reproducibility even after the superiority claim is removed.

### Follow-up experiment — Verify the retuned DextrAH transfer with a teacher-only comparison

**Status:** Planned. A figure placeholder has been added to Supplementary
Section D.1 and a matching evidence placeholder has been added to response item
M2(1). No numerical claim should replace those placeholders until the protocol,
raw data, and uncertainty analysis below have been verified.

#### Purpose and claim boundary

The revised manuscript withdraws the claim that the direct-control teacher
implementation is intrinsically superior to DextrAH. Nevertheless, the response
must demonstrate that the submitted DextrAH/FABRICS comparison was based on a
real target-platform adaptation and that selecting the direct joint-target
teacher did not sacrifice teacher performance.

The experiment may support only the following scoped conclusion:

> On the Tiangong 2 Pro--InspireHand platform, the direct joint-target teacher
> achieves performance equivalent to, or at least comparable with, the retuned
> DextrAH/FABRICS teacher under a matched evaluation protocol. We therefore use
> direct control as an embodiment-native implementation choice that avoids
> human-motion retargeting, PCA action-manifold construction, and additional
> FABRICS tuning. This is not evidence of general RL-algorithm superiority.

#### Baseline identity and transfer audit

- [ ] Record the exact source commit, configuration, checkpoint, and training
      logs for the DextrAH/FABRICS teacher.
- [ ] Document every target-platform adaptation: robot geometry, collision
      model, joint and dynamic limits, action interface, PCA or hand-action
      manifold, controller gains, low-level command mapping, and RL parameters.
- [ ] Verify whether the implementation is sufficiently faithful to be called a
      `retuned DextrAH/FABRICS teacher`. If any essential DextrAH component was
      not reproduced, label it `DextrAH-inspired adapted FABRICS teacher`
      instead.
- [ ] Record the corresponding source commit, configuration, checkpoints, and
      logs for the direct joint-target teacher.
- [ ] Confirm that the two implementations differ only in the intended
      teacher action/control interface and associated reward or controller
      requirements; list all remaining differences explicitly.

#### Matched teacher-only experiment

- [ ] Evaluate the teachers directly, before DAgger, student distillation,
      Bellman-critic intervention, or VLM adaptation.
- [ ] Use the same 40 objects, initial-state distribution, object sampling,
      episode horizon ($T_{\max}=10\,\mathrm{s}$), success definition, unsafe-event
      definitions, evaluation episodes per object, simulator version, and
      hardware allocation.
- [ ] Match the PPO interaction budget, environment count, checkpoint cadence,
      and random seeds. Report any unavoidable mismatch rather than silently
      normalizing it away.
- [ ] Plot evaluation lift-success against environment interaction steps, not
      raw training reward, because the two reward formulations or scales may
      differ.
- [ ] Use at least three matched seeds, preferably five. Plot the seed mean and
      a 95\% confidence interval without hiding the individual seed traces.
- [ ] Add teacher unsafe-termination rate against environment steps so that
      comparable task success is not achieved by accepting substantially more
      unsafe rollouts.
- [ ] If wall-clock or sample-efficiency statements are made, report both
      environment steps and measured wall-clock time under the same compute
      setup.

#### Final-performance and equivalence analysis

- [ ] Evaluate the selected final checkpoint from each matched seed on all 40
      objects using paired evaluation conditions where possible.
- [ ] Plot the per-object paired difference
      $\Delta_i=S_i^{\mathrm{direct}}-S_i^{\mathrm{FABRICS}}$ and report its
      mean with a bootstrap or otherwise justified 95\% confidence interval.
- [ ] Define the practically meaningful equivalence margin before inspecting
      the final comparison. Document the scientific justification for the
      chosen margin.
- [ ] Use an equivalence or non-inferiority analysis appropriate to the claim.
      Failure to reject a difference is not evidence that the implementations
      match.
- [ ] Report the final lift-success and unsafe-termination denominators, effect
      sizes, intervals, and seed/object aggregation rule.
- [ ] Use the words `matches`, `equivalent`, or `comparable` only if the verified
      interval and pre-specified margin support that wording.

#### Missing-log fallback

If historical checkpoint traces cannot be recovered, do not reconstruct or
smooth a synthetic training curve. Instead:

- [ ] evaluate the available final teacher checkpoints under the matched
      40-object protocol;
- [ ] present a paired per-object dot/difference plot with uncertainty; and
- [ ] state explicitly that the evidence concerns final teacher performance,
      not learning speed or convergence behavior.

#### UniDexGrasp++ scope

- [ ] Cite UniDexGrasp++ only as precedent for a normalized direct
      motor-command interface.
- [ ] Do not add UniDexGrasp++ as a separate performance baseline unless its
      complete relevant training method is faithfully ported and evaluated.
- [ ] Do not call the direct teacher the `UniDexGrasp++ recipe`: its reward,
      observations, task distribution, PPO configuration, and lack of the full
      GeoCurriculum/GiGSL pipeline must remain explicit.

#### Required deliverables

- [ ] Preserve the raw scalar exports and a manifest mapping every plotted line
      to its source run, seed, checkpoint, and metric tag.
- [ ] Replace the boxed placeholder in Supplementary Section D.1 with the
      verified teacher-only figure and final caption.
- [ ] Replace the red placeholder in response M2(1) with the exact sample sizes,
      final values, effect/interval, and scoped conclusion.
- [ ] Add a compact implementation table listing the action interface,
      intermediate controller, human-motion/PCA requirement, and
      embodiment-specific tuning for both teachers.
- [ ] Check that the main manuscript, highlighted manuscript, response, and
      appendix use the same baseline name and the same level of claim.

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

**Reviewer item:** Reviewer 31, M4

**Related item:** Reviewer 29, comment 8 (tracked separately in `response.tex`).

**Status:** Complete. The M4 response explains the existing ablation ladder,
visual randomization during distillation and evaluation, and the Figure 4
unsafe-event decomposition. The safety--autonomy curve remains an optional
nice-to-have.

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

### Completed resolution

- [x] Explain the ablation ladder using the current manuscript labels:
      (c) fixed critic-based intervention, (f) adaptive non-VLM curriculum,
      (e) LLM-only adaptation without images, and (d) full VLM adaptation.
      Identify the LLM-only versus VLM comparison as the comparison addressing
      the contribution of visual input.
- [x] Clarify that visual contexts refer to DexTrAH-RGB-style randomization
      of lighting intensity and direction, background textures, object
      materials, and table appearance during both distillation and
      post-training evaluation. Table III reports aggregate performance
      across these randomized visual conditions.
- [x] Explain that unsafe scenarios refer to harmful collision, object escape,
      palm flip, and hand-too-far. Point to Figure 4 and the Results discussion
      for the failure-mode decomposition and early-training behavior on two
      illustrative objects.
- [x] Add the closing sentence offering to consider more cautious and precise
      contribution wording if the reviewer still finds it misleading.
- [x] Remove the remaining M4 drafting checklist and rebuild and visually
      check the response PDF.

### Final response

See the completed response to Reviewer 31 M4 in `response.tex`. The adopted
response explains the existing experimental design and evidence; additional
experiments are not required by this task's completion criteria. Reviewer 29's
separate question about novel scene semantics remains tracked in its own
response item.

### Optional follow-up

- [ ] **Nice to have for M4:** add a safety--autonomy trade-off curve, plotting
      unsafe-event rate against autonomy (or, equivalently, intervention
      burden) across the relevant methods or operating points.
