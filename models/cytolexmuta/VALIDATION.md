# Runtime validation, 2026-09-06

The author GEMME/JET2 runtime was executed from the pinned image filesystem
without modifying its source. Python 2.7, R, Java and JET2 completed the
prediction path, including fresh conservation and combination-mutation output.

The technical smoke uses GRB2_HUMAN_Faure_2021: 217 residues, the first 128
aligned MSA sequences, WT and five variants selected without target access.
The reduced MSA depth is for smoke testing only, not benchmark evaluation.

| Variant | Fresh GEMME score |
| --- | ---: |
| WT | 0 (defined reference baseline) |
| T159M:D166V | -4.6452142726407 |
| T159F:G203C | -4.78223070986054 |
| T159F:G203A | -4.78223070986054 |
| T159F:G200V | -4.86126482255229 |
| T159F:G200T | -4.58612836097824 |

The 11 lightweight regression tests pass; `uv lock --check`, `uv build` and
`git diff --check` pass. These tests cover subprocess isolation, finite output,
coordinates, fixed fusion, and the ESM-IF1 compatibility imports/reductions.

The three neural experts' GPU smoke is still pending accelerator allocation.
Neither complete four-expert execution nor Full217 runtime parity is claimed.
