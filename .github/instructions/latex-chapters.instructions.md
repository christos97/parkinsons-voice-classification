---
name: LaTeX Thesis Conventions
description: LaTeX coding standards for MSc thesis on Parkinson's Disease voice classification
applyTo: "thesis/**/*.tex"
---

# LaTeX Thesis Writing Standards

These instructions apply when editing thesis LaTeX files.

## Label Conventions

Use consistent prefixes for all labels:

```latex
\label{ch:introduction}      % Chapters
\label{sec:feature-extraction}  % Sections
\label{fig:roc-curve}        % Figures
\label{tab:results-summary}  % Tables
\label{eq:jitter-formula}    % Equations
```

## Cross-References

Always use non-breaking space before `\ref`:

```latex
% CORRECT
Figure~\ref{fig:name}
Table~\ref{tab:name}
Chapter~\ref{ch:name}
Section~\ref{sec:name}
Equation~\ref{eq:name}

% INCORRECT
Figure \ref{fig:name}
```

## Figure Environment

Use `[H]` placement (requires float package) and no path prefix:

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{fig_name.png}
    \caption{Descriptive caption explaining the figure content.}
    \label{fig:descriptive-name}
\end{figure}
```

## Table Environment (booktabs)

Use booktabs commands, caption above table:

```latex
\begin{table}[H]
    \centering
    \caption{Caption goes above the table.}
    \label{tab:table-name}
    \begin{tabular}{@{}lcc@{}}
        \toprule
        Header & Column 1 & Column 2 \\
        \midrule
        Row 1 & value & value \\
        Row 2 & value & value \\
        \bottomrule
    \end{tabular}
\end{table}
```

Never use `\hline` — use `\toprule`, `\midrule`, `\bottomrule`.

## Citations

```latex
\cite{key}   % Standard: [1]
\citep{key}  % Parenthetical: [1]
\citet{key}  % Textual: Author et al. [1]
```

At least one `\cite{}` command required in chapters for bibliography to build.

## Statistical Results

Always report mean ± std for cross-validation metrics:

```latex
% CORRECT
achieved an accuracy of $0.82 \pm 0.05$

% INCORRECT - single point estimate
achieved 82\% accuracy
```

## Forbidden Language

Never use these phrases in thesis text:

- "X outperforms Y" → "X achieved higher scores than Y"
- "This proves..." → "These results suggest..."
- "Clearly superior" → "Showed improvement"
- "This diagnoses..." → "This classifies..."
- "Significant" (without test) → "Notable" or "Observed"

## Required Caveats

Include when discussing results:

```latex
% Dataset A (small sample)
These results should be interpreted cautiously given the small sample size ($n=37$).

% Dataset B (unknown subjects)
Results may be optimistic due to unknown subject overlap across samples.
```

## Math Formatting

Use `amsmath` environments:

```latex
% Inline math
The jitter value $J$ is calculated as...

% Display equation
\begin{equation}
    J_{\text{local}} = \frac{1}{N-1} \sum_{i=1}^{N-1} |T_i - T_{i+1}|
    \label{eq:jitter-local}
\end{equation}
```

## Code Listings

Use the `listings` package with Python style:

```latex
\begin{lstlisting}[language=Python, caption={Feature extraction example}]
features = extract_prosodic_features(audio_signal)
\end{lstlisting}
```

## Itemize/Enumerate

Standard LaTeX lists with consistent formatting:

```latex
\begin{itemize}
    \item First point
    \item Second point
\end{itemize}

\begin{enumerate}
    \item First step
    \item Second step
\end{enumerate}
```
