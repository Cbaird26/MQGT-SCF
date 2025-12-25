# Compiling LaTeX Papers

## Option A: Local Compilation (if pdflatex installed)

```bash
cd papers/no-go-theorems

# Compile main paper (no-go theorems)
pdflatex main.tex
pdflatex main.tex  # Run twice for references

# Compile QRNG protocol
pdflatex protocol_qrng.tex
pdflatex protocol_qrng.tex  # Run twice for references

# Rename outputs
mv main.pdf paper_no-go-theorems.pdf
mv protocol_qrng.pdf paper_qrng_protocol.pdf
```

## Option B: Overleaf (Recommended)

1. Go to https://www.overleaf.com
2. Create new project
3. Upload:
   - `main.tex`
   - `protocol_qrng.tex`
   - `figures/` folder (all 6 PNG files)
4. Click "Recompile"
5. Download PDFs

## Required Files

- `main.tex` - No-go theorems paper
- `protocol_qrng.tex` - QRNG preregistered protocol
- `figures/` - All 6 PNG files must be in this folder

## Verification

After compilation, verify:
- ✅ Figures appear in `main.pdf`
- ✅ All 6 figures are visible
- ✅ No LaTeX errors
- ✅ PDF is complete

## Notes

The LaTeX files reference figures in the `figures/` subdirectory. Make sure all PNG files are present before compiling.

