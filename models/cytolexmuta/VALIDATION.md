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

## Completed GPU continuation

On 2026-09-06, ESM-C, ProSST (including structure quantization), and ESM-IF1
each generated six finite scores on an NVIDIA H200. The GEMME component above
was reused from this same smoke, not recomputed or obtained from the Full217
prediction release. Fixed fusion produced:

| Variant | Fused score |
| --- | ---: |
| WT | 11.791774043239156 |
| T159M:D166V | -0.0615508597479411 |
| T159F:G203C | -1.1270169224390616 |
| T159F:G203A | -0.3828088092165065 |
| T159F:G200V | -0.148117985549912 |
| T159F:G200T | 0.8924221208948302 |

An independent artifact check verified four finite six-row component arrays,
six unique variant keys, and agreement with the fixed fusion to 1e-12 absolute
tolerance. Target access and optimizer updates were both zero.

The run used NGC PyTorch 25.02 with an isolated offline dependency overlay
(torch 2.7.0a0+ecf3bae40a.nv25.02, transformers 4.57.6). Its initial Job command
failed before inference because an account-private path was not mounted;
the smoke then completed in the same retained GPU container via the project's
shared directory. Platform Job status is not the business-success evidence.
This validates live runtime execution, not a clean Docker rebuild, Full217
numerical parity, or a new benchmark score. The upstream KMeans pickle emitted
a scikit-learn version warning (saved with 1.2.2, loaded with 1.5.2).
