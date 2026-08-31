MQGT Paper Package (arXiv-ready)
================================

HISTORICAL STATUS
-----------------
This is the historical operational Born-deformation paper. It is retained for
provenance and is not the current MQGT-SCF reference statement. Part 0,
Technical Monograph, controls wherever this package conflicts with it. Do not
attribute this paper's ethically weighted Born-rule endpoint to Part 0.

This folder contains:
- main.tex            : Manuscript
- supplement.tex      : Supplementary material
- references.bib      : BibTeX database
- figures/            : Generated figures (PNG)
- results_summary.json: Key numerical outputs embedded in the manuscript figures

How to compile
--------------
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

and similarly for supplement.tex.

Notes
-----
- The CMS Higgs invisible constraint is implemented using the published best-fit and asymmetric errors (see paper and supplement).
- QRNG sensitivity is shot-noise-limited (scales as 2/sqrt(N) for DeltaE=1).
- The fifth-force figure illustrates the gravitational-strength (alpha=1) bound lambda < 38.6 um.

Generated on: 2025-12-22 00:15:04.254341
