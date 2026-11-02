# RA-L manuscript and review file map

This directory contains the latest RA-L decision materials for
**VLM-DexSafeDagger**. The paper was submitted as manuscript **26-3841**.

> Repository note: the directory name uses `rebutal` (one `t`). The spelling is
> retained to avoid breaking paths.

## Submission timeline

| Stage | Manuscript ID | Main manuscript | Response/revision material | Reviews and decision |
|---|---|---|---|---|
| Initial RA-L submission | `26-3841v1` | [Initial submitted manuscript](../../first_rebutal/output/revision/vlm_dexsafedagger_compressed.pdf) | None | [AE report](../../first_rebutal/comments/ReportOn26-3841v1.txt), [Reviewer 14](../../first_rebutal/comments/Review538875(Reviewer14)Of26-3841v1.txt), and [Reviewer 22](../../first_rebutal/comments/Review539395(Reviewer22)Of26-3841v1.txt) |
| First major revision / Version 2 | `26-3841v2` | [Revised manuscript](../../first_rebutal/output/revision/main.pdf) | [Complete response, supplement, and highlighted manuscript](../../first_rebutal/output/revision/response_and_diff.pdf) | The latest reports stored in this directory |
| Planned new submission after Version 2 rejection | New manuscript ID not assigned | Not created yet | Not created yet | Use the Version 2 AE report and Reviewer 29/31 reports below |

## Latest review round: Version 2

These are the newest official review files:

- [Associate Editor report](ReportOn26-3841v2.txt)
- [Reviewer 29 report](Review553287(Reviewer29)Of26-3841v2.txt)
- [Reviewer 31 report](Review556087(Reviewer31)Of26-3841v2.txt)
- [Consolidated resubmission and Codex action plan](VLM_DexSafeDagger_RAL_Resubmission_Codex_Plan.pdf)

The consolidated plan describes the outcome as a **Version 2 rejection** and
recommends preparing a substantially revised **new submission**. The four main
unresolved areas are:

1. complete specification of the RL teacher-training procedure;
2. fairness of the DexTrAH baseline comparison;
3. inconsistencies among figures, tables, means, and textual claims; and
4. stronger evidence for the incremental contribution of VLM-guided adaptation.

## Version 2 submission package

The following files are the latest materials that were submitted before the
current review round:

- [Clean Version 2 manuscript](../../first_rebutal/output/revision/main.pdf) —
  8 pages; corresponds to `26-3841_02_MS.pdf` in the consolidated plan.
- [Complete author-response package](../../first_rebutal/output/revision/response_and_diff.pdf) —
  29 pages; corresponds to `26-3841_02_AR.pdf` in the consolidated plan.
- [Standalone point-by-point response](../../first_rebutal/response/response.pdf) —
  13 pages.
- [Standalone supplementary material](../../first_rebutal/response/appendix.pdf) —
  6 pages.
- [Standalone highlighted manuscript](../../../../main_highlighted.pdf) —
  10 pages. It is also included in the complete 29-page response package.
- [First-revision cover letter](../../first_rebutal/response/cover_letter.txt).

### Editable Version 2 sources

- [Main manuscript source](../../../../main.tex)
- [Point-by-point response source](../../first_rebutal/response/response.tex)
- [Supplement source](../../first_rebutal/response/appendix.tex)
- [Supplement content](../../first_rebutal/response/06_appendix.tex)
- [Paper build instructions](../../../../README.md)

The root manuscript sources currently represent the last revised paper. Preserve
this state as the Version 2 baseline before making changes for the next
submission.

## Initial submission and first review round

### Initial manuscript files

- [Initial submitted manuscript](../../first_rebutal/output/revision/vlm_dexsafedagger_compressed.pdf) —
  8 pages, created 3 July 2026.
- [Initial submission source archive](../../first_rebutal/output/vlm_dexsafedagger.zip).

### First-round reviews (`26-3841v1`)

- [Associate Editor report](../../first_rebutal/comments/ReportOn26-3841v1.txt)
- [Reviewer 14 report](../../first_rebutal/comments/Review538875(Reviewer14)Of26-3841v1.txt)
- [Reviewer 22 report](../../first_rebutal/comments/Review539395(Reviewer22)Of26-3841v1.txt)

### Other first-revision material

- [RA-L rebuttal reference PDF](../../first_rebutal/reference/_RAL_Rebuttal_.pdf)
- Figures and supporting assets used by the first response are under
  [`../../first_rebutal/response/figures/`](../../first_rebutal/response/figures/).

## Mapping to the consolidated plan

The source labels used in
[the consolidated plan](VLM_DexSafeDagger_RAL_Resubmission_Codex_Plan.pdf)
map to repository files as follows:

| Plan label | Repository file |
|---|---|
| `[S1] 26-3841_02_MS.pdf` | [Version 2 manuscript](../../first_rebutal/output/revision/main.pdf) |
| `[S2] 26-3841_02_AR.pdf` | [Version 2 response package](../../first_rebutal/output/revision/response_and_diff.pdf) |
| `[S3] Latest reviews` | [AE report](ReportOn26-3841v2.txt), [Reviewer 29](Review553287(Reviewer29)Of26-3841v2.txt), and [Reviewer 31](Review556087(Reviewer31)Of26-3841v2.txt) |
| `[S4] RA-L author information` | External IEEE RA-L policy page cited in the plan; no local snapshot is currently stored |

## Files still to be created for the next submission

No Version 3/new-submission manuscript or response package exists yet. To keep
the review history auditable, place new work in a separate revision directory
instead of overwriting the Version 2 files. The eventual package should include:

- a clean revised manuscript;
- a highlighted manuscript relative to Version 2;
- a self-contained response to the AE, Reviewer 29, and Reviewer 31;
- updated supplementary material;
- a combined response-plus-highlighted-manuscript upload PDF; and
- a record mapping all reported results to scripts, configurations, and raw logs.
