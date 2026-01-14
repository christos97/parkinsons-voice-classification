#!/bin/bash
# Clean build script for thesis

cd "$(dirname "$0")"

echo "Cleaning auxiliary files..."
rm -f main.aux main.bbl main.blg main.log main.out main.toc main.lof main.lot main.fls main.fdb_latexmk
rm -f chapters/*.aux frontmatter/*.aux appendices/*.aux

echo "Step 1: First pdflatex pass..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

echo "Step 2: Running bibtex..."
bibtex main > /dev/null 2>&1

echo "Step 3: Second pdflatex pass..."
pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1

echo "Step 4: Third pdflatex pass..."
pdflatex -interaction=nonstopmode main.tex

echo ""
echo "Build complete!"
pdfinfo main.pdf | grep "Pages:"
