DexSafeDagger evaluation counts and reported summary statistics
==============================================================

The author checked and adjusted the evaluation counts against the real counts
and confirmed this on 2026-11-19. These files store per-object and pooled
episode counts, plus the aggregate statistics reported in the manuscript and
appendix. Individual trial records, images, and training logs are not included.

Files
-----
fig3_safety_autonomy_tradeoff.json
  Plot-ready training-time safety-autonomy points digitized from Figure 3(b,c).
  Each checkpoint is stored explicitly as an [x, y] pair, where x is student
  autonomy (%) and y is the unsafe-episode rate (%). Ablations are separated
  for direct comparison; unchecked values are retained as null placeholders.

plot_fig3_safety_autonomy_tradeoff.py
  Regenerates the appendix tradeoff figure directly from the JSON file. Curves
  are drawn only for ablations whose points are complete; null-valued ablations
  appear as pending legend entries rather than fabricated curves.

real_robot_counts.json
  Covers manuscript Table IV(a-b) and Appendix Tables 5-8. The 22 per-object
  rows contain 30 trials each. Their pooled totals cover 14 seen objects
  (420 trials) and 8 unseen objects (240 trials). The comparison includes the
  author-supplied unsafe counts for the fixed-threshold policy (ablation c).

simulation_results.json
  Covers manuscript Tables II-III and Appendix Tables 3-4. Displayed object
  rows contain 200 evaluation trials each. Exact counts are included where
  supplied; aggregate percentages and five-seed means/standard deviations
  are retained as summary statistics without assigning integer counts.

teacher_table_ii_mean_aggregate.json
  Teacher counts for all 40 objects, 200 evaluation trials per object, and
  8,000 trials in total. Unsafe failure-mode counts sum to the unsafe total.

validate_counts.py
  Uses only the Python standard library. Checks count/rate agreement,
  per-object sums, unsafe-event decomposition, manuscript/appendix table
  agreement, Wilson intervals, and the pooled two-proportion comparison.
  From the paper repository root, run:

    python3 comments/RAL/second_rebutal/reference/raw_data/validate_counts.py .

Reporting conventions
---------------------
Rates are percentages rounded to one decimal place, with ties rounded up.
Counts are marginal episode outcomes: lift success and unsafe termination may
occur in the same episode. The four unsafe categories partition unsafe
terminations. Table 8 treats episodes as independent within each object group,
uses two-sided pooled two-proportion z tests, and gives unpooled normal-
approximation 95% confidence intervals for the rate differences.

The full VLM student (ablation d) has 62 unsafe episodes in 420 seen trials
(14.8%) and 94 in 240 unseen trials (39.2%). Fixed-threshold ablation c has
68/420 (16.2%) and 100/240 (41.7%). The observed reductions are 1.43 and
2.50 percentage points; both difference intervals include zero.

Source paths in JSON refer to the parent RAL_dexsafedagger repository.

Confirmed lift-success count
----------------------------
The author confirmed 350 successful episodes out of 420 seen-object trials
for ablation (c) on 2026-11-19. The pooled rate is 83.333...%, reported as
83.3% in Main Table IV(b) and Appendix Table 7. The count and rate are stored
in real_robot_counts.json; the previously open reporting issue is resolved.
