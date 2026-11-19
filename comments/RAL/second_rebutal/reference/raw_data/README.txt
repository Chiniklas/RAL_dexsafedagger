DexSafeDagger evaluation counts and reported summary statistics
==============================================================

The author checked and adjusted the evaluation counts against the real counts
and confirmed this on 2026-11-19. These files store per-object and pooled
episode counts, plus the aggregate statistics reported in the manuscript and
appendix. Individual trial records, images, and training logs are not included.

Files
-----
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

Open reporting issue
--------------------
Main Table IV(b) and Appendix Table 7 report 83.4% seen-object lift success
for ablation (c). No integer count out of the stated 420 trials rounds to
83.4%. The percentage is retained as reported, with no assigned success count,
pending author confirmation of its numerator or aggregation rule. The audit
currently reports this one unresolved issue and exits with a nonzero status.
