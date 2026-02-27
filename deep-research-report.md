# Strengthening the Literature Review and Bibliography for Parkinson’s Voice Classification

## Thesis framing and bibliographic strategy

Your topic sits at the intersection of (i) clinical foundations of Parkinsonian speech changes, (ii) speech signal processing/feature engineering, and (iii) biomedical machine-learning evaluation quality (especially leakage, validation design, and claims discipline). A strong MSc thesis typically earns credibility by anchoring each of these pillars in *canonical* sources, then layering more recent systematic reviews and domain-specific papers on top. citeturn9search0turn7search3turn6search2turn2search1turn1search1

Two practical principles should guide how you strengthen Chapter 2 (and the bibliography overall):

First, separate “what is known clinically about speech/voice in PD” from “what ML papers report.” Clinical foundations (review articles in journals like *The Lancet* and *JNNP*, plus authoritative epidemiology/fact sources) let you describe speech impairment as part of PD without over-claiming diagnostic capability. citeturn9search0turn7search3turn0search0

Second, treat evaluation methodology as a first-class scientific contribution: your thesis should explicitly discuss why voice-based PD classification is vulnerable to optimistic bias (e.g., repeated measures, subject overlap, feature extraction pipelines you cannot audit), and cite the methodological literature accordingly (nested CV bias, selection bias, uncertainty estimation under CV), plus modern reporting/risk-of-bias tools (*TRIPOD+AI*, *PROBAST+AI*). citeturn2search1turn1search0turn19search4turn19search0turn1search1turn0search1

For dataset grounding in your methods chapter, it helps to cite the dataset landing pages directly (so readers can verify tasks, sampling rates, labeling, and licensing). Your “raw audio” dataset from entity["organization","Zenodo","research repository"] provides read speech (“North Wind and the Sun”) and spontaneous dialogue recorded by smartphone, and includes clinical metadata labels (e.g., Hoehn & Yahr and UPDRS items) in filenames/annotation description. citeturn5view0 The “pre-extracted features” dataset on the entity["organization","UCI Machine Learning Repository","dataset host"] describes sustained /a/ phonation with three repetitions per subject and 754 extracted features; its documentation is directly relevant when you explain why subject ID absence can inflate internal CV. citeturn2search2

## Candidate references with placement guidance

**Note on links:** URLs are provided as DOI-resolvers or publisher pages in code-form; click-through support is also provided via citations in each row.

| Priority | Theme Bucket (A/B/C/D/E) | Full Title | Authors | Year | Venue | DOI | Official URL (publisher page) | Why relevant (1–2 lines, thesis-specific) | Suggested chapter placement |
|---|---|---|---|---:|---|---|---|---|---|
| High | E | TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods | entity["people","Gary S Collins","clinical prediction models"] et al. | 2024 | BMJ | 10.1136/bmj-2023-078378 | `https://doi.org/10.1136/bmj-2023-078378` citeturn1search1 | Directly supports transparent reporting (data splits, intended use, participants, predictors, evaluation) for ML-based diagnostic classifiers. | 04_methodology |
| High | E | PROBAST+AI: an updated quality, risk of bias, and applicability assessment tool for prediction models using regression or artificial intelligence methods | entity["people","Karel G M Moons","prediction model methodology"] et al. | 2025 | BMJ | 10.1136/bmj-2024-082505 | `https://doi.org/10.1136/bmj-2024-082505` citeturn0search1 | Gives a structured way to discuss risk-of-bias/applicability for PD voice classifiers (participants, predictors, outcomes, analysis). | 07_discussion |
| High | B | Has machine learning over-promised in healthcare?: A critical analysis and a proposal for improved evaluation, with evidence from Parkinson’s disease | entity["people","Wenbo Ge","ai in medicine evaluation"] et al. | 2023 | Artificial Intelligence in Medicine (Elsevier) | 10.1016/j.artmed.2023.102524 | `https://doi.org/10.1016/j.artmed.2023.102524` citeturn2search1 | Highly on-topic critique of inflated PD phonation results; ideal to justify cautious tone, leakage concerns, and stronger evaluation design. | 02_literature_review |
| High | B | Bias in error estimation when using cross-validation for model selection | entity["people","Sudhir Varma","biostatistics"] and entity["people","Richard Simon","biostatistics"] | 2006 | BMC Bioinformatics (Springer Nature) | 10.1186/1471-2105-7-91 | `https://doi.org/10.1186/1471-2105-7-91` citeturn1search0 | Classic citation for why naive CV error estimates are biased when CV is used for model selection without proper nesting. | 05_experimental_design |
| High | B | On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation | entity["people","Gavin C Cawley","machine learning evaluation"] et al. | 2010 | JMLR | N/A (JMLR) | `https://www.jmlr.org/papers/v11/cawley10a.html` citeturn19search4 | Supports the thesis argument that hyperparameter tuning can “overfit the evaluation” unless carefully designed. | 05_experimental_design |
| High | B | No Unbiased Estimator of the Variance of K-Fold Cross-Validation | entity["people","Yoshua Bengio","machine learning"] et al. | 2004 | JMLR | N/A (JMLR) | `https://jmlr.org/papers/v5/grandvalet04a.html` citeturn19search0 | Excellent for explaining why uncertainty reporting under CV is subtle; motivates reporting mean±std and careful interpretation. | 05_experimental_design |
| High | B | The relationship between Precision-Recall and ROC curves | entity["people","Jesse Davis","machine learning evaluation"] et al. | 2006 | ICML ’06 (ACM) | 10.1145/1143844.1143874 | `https://doi.org/10.1145/1143844.1143874` citeturn17search2 | Grounding for when PR curves are more informative than ROC under imbalance—relevant if PD/HC ratio is skewed. | 05_experimental_design |
| High | B | An introduction to ROC analysis | entity["people","Tom Fawcett","roc analysis"] | 2006 | Pattern Recognition Letters (Elsevier) | 10.1016/j.patrec.2005.10.010 | `https://doi.org/10.1016/j.patrec.2005.10.010` citeturn17search3 | Canonical paper for ROC interpretation/pitfalls; supports correct metric discussion and figure choices in Methods/Results. | 04_methodology |
| Medium | B | Comparing the Areas under Two or More Correlated ROC Curves: A Nonparametric Approach | entity["people","Elizabeth R DeLong","biostatistics"] et al. | 1988 | Biometrics (Wiley) | 10.2307/2531595 | `https://doi.org/10.2307/2531595` citeturn18search0 | Standard method citation when you justify statistical comparison of AUCs (even if you do not run tests, it anchors discussion). | 05_experimental_design |
| High | A | Parkinson’s disease | entity["people","Lorraine V Kalia","neurology"] et al. | 2015 | The Lancet (Elsevier) | 10.1016/S0140-6736(14)61393-3 | `https://doi.org/10.1016/S0140-6736(14)61393-3` citeturn9search0 | High-impact clinical review to ground PD heterogeneity, diagnosis limits, and rationale for biomarkers (incl. speech). | 02_literature_review |
| High | A | Parkinson’s disease: clinical features and diagnosis | entity["people","Joseph Jankovic","parkinson specialist"] | 2008 | Journal of Neurology, Neurosurgery & Psychiatry (BMJ) | 10.1136/jnnp.2007.131045 | `https://doi.org/10.1136/jnnp.2007.131045` citeturn7search3 | Strong clinical anchor for motor/non-motor presentation and diagnostic nature—useful to avoid “diagnostic certainty” language. | 02_literature_review |
| Medium | A | Parkinson disease | World Health Organization | 2023 | WHO Fact Sheet | N/A | `https://www.who.int/en/news-room/fact-sheets/detail/parkinson-disease` citeturn0search0 | Authoritative, accessible overview (burden, symptoms incl. speech difficulty) for intro/context (not a peer-reviewed study). | 02_literature_review |
| Medium | A | The prevalence of Parkinson's disease: a systematic review and meta-analysis | entity["people","Tamara Pringsheim","neurology epidemiology"] et al. | 2014 | Movement Disorders (Wiley) | 10.1002/mds.25945 | `https://doi.org/10.1002/mds.25945` citeturn8search3 | Gives epidemiological context and helps justify clinical/public-health relevance in intro/background. | 02_literature_review |
| High | A | Suitability of dysphonia measurements for telemonitoring of Parkinson's disease | entity["people","Max A Little","speech biomarkers"] et al. | 2009 | IEEE Transactions on Biomedical Engineering | 10.1109/TBME.2008.2005954 | `https://doi.org/10.1109/TBME.2008.2005954` citeturn3search2 | Seminal PD voice/dysphonia ML paper; good for features, early telemonitoring framing, and contrast to modern evaluation concerns. | 02_literature_review |
| Medium | A | Telediagnosis of Parkinson's disease using measurements of dysphonia | entity["people","C Okan Sakar","parkinson speech ml"] et al. | 2010 | Journal of Medical Systems (Springer) | 10.1007/s10916-009-9272-y | `https://doi.org/10.1007/s10916-009-9272-y` citeturn24search1 | Directly relevant to dysphonia feature-based PD/HC classification and validation choices (leave-one-individual-out discussion). | 02_literature_review |
| Medium | A | Speech and language biomarkers for Parkinson’s disease prediction, early diagnosis and progression | entity["people","Fangyuan Cao","speech biomarkers"] et al. | 2025 | npj Parkinson’s Disease (Nature Portfolio) | 10.1038/s41531-025-00913-4 | `https://doi.org/10.1038/s41531-025-00913-4` citeturn6search2 | Recent high-quality review; helps you contextualize sustained phonation vs read vs spontaneous speech tasks and biomarker taxonomy. | 02_literature_review |
| Medium | A | Digital speech biomarkers can measure acute effects of levodopa in Parkinson’s disease | entity["people","Maria A Kopylova","digital biomarkers"] et al. | 2025 | npj Parkinson’s Disease (Nature Portfolio) | 10.1038/s41531-025-01045-5 | `https://doi.org/10.1038/s41531-025-01045-5` citeturn6search7 | Useful in Discussion: speech changes can be medication-state dependent; motivates careful interpretation and covariate reporting. | 07_discussion |
| Medium | A | Voice biomarkers as prognostic indicators for Parkinson’s disease using machine learning techniques | entity["people","Ifrah Naeem","ml in parkinson"] et al. | 2025 | Scientific Reports (Nature Portfolio) | 10.1038/s41598-025-96950-3 | `https://doi.org/10.1038/s41598-025-96950-3` citeturn6search11 | Recent example of “voice biomarkers” framing; can be used to compare your “classification vs prognosis” scope and tone down claims. | 02_literature_review |
| Medium | A | Voice-Based Detection of Parkinson’s Disease Using Machine and Deep Learning Approaches: A Systematic Review | entity["people","Hadi Sedigh Malekroodi","pd voice review"] et al. | 2025 | Bioengineering (MDPI) | 10.3390/bioengineering12111279 | `https://doi.org/10.3390/bioengineering12111279` citeturn6search6 | Systematic review focused on voice; use for dataset landscape, common features, and recurring methodological issues (good for lit review). | 02_literature_review |
| Medium | A | Speech Markers of Parkinson’s Disease: Phonological Features and Acoustic Measures | entity["people","Ratree Wayland","pd speech markers"] et al. | 2025 | Brain Sciences (MDPI) | 10.3390/brainsci15111162 | `https://doi.org/10.3390/brainsci15111162` citeturn6search0 | Helpful to ground feature families (phonation, articulation, prosody) and bridge “speech science” and ML feature sets. | 02_literature_review |
| Medium | A | Innovative Speech-Based Deep Learning Approaches for Parkinson’s Disease Classification: A Systematic Review | entity["people","Lisanne van Gelderen","pd speech review"] et al. | 2024 | Applied Sciences (MDPI) | 10.3390/app14177873 | `https://doi.org/10.3390/app14177873` citeturn6search8 | Even if you use classical ML, this review often catalogs datasets/tasks and highlights evaluation gaps; cite selectively for “field context.” | 02_literature_review |
| Medium | A | An algorithm for Parkinson’s disease speech classification based on isolated words analysis | entity["people","Federica Amato","speech classification"] et al. | 2021 | Health Information Science and Systems (Springer) | 10.1007/s13755-021-00162-8 | `https://doi.org/10.1007/s13755-021-00162-8` citeturn6search10 | Example of PD speech classification with clearer speech unit design (isolated words); good comparator for “task choice matters.” | 02_literature_review |
| Medium | A | Acoustic characteristics of Parkinsonian speech: a potential biomarker of early disease progression and treatment | entity["people","Julie Rusz","parkinson speech acoustics"] et al. | 2004 | Journal of Neurolinguistics (Elsevier) | 10.1016/j.jneuroling.2004.06.001 | `https://doi.org/10.1016/j.jneuroling.2004.06.001` citeturn6search3 | Supports the claim that acoustic measures can change early and longitudinally; helps motivate read/spontaneous speech tasks. | 02_literature_review |
| Medium | A | Distinctive acoustic changes in speech in Parkinson's disease | entity["people","Yongjun Wang","parkinson speech acoustics"] et al. | 2022 | Computer Speech & Language (Elsevier) | 10.1016/j.csl.2022.101384 | `https://doi.org/10.1016/j.csl.2022.101384` citeturn6search9 | Modern speech-science/ASR-adjacent work; use it to update the “which acoustic domains change” narrative. | 02_literature_review |
| Medium | B | A comparative analysis of speech signal processing algorithms for Parkinson’s disease classification and the use of the tunable Q-factor wavelet transform | C. Okan Sakar et al. | 2019 | Applied Soft Computing (Elsevier) | 10.1016/j.asoc.2018.10.022 | `https://doi.org/10.1016/j.asoc.2018.10.022` citeturn24search3 | Strong match to your “classical ML + engineered features” scope; also directly ties to TQWT-style feature families. | 02_literature_review |
| High | C | Generalized Linear Models | entity["people","J A Nelder","glm"] et al. | 1972 | JRSS Series A (Oxford Academic) | 10.2307/2344614 | `https://doi.org/10.2307/2344614` citeturn16search0 | Canonical theoretical grounding for logistic regression via GLMs; use for rigorous Methodology Chapter ML foundations. | 04_methodology |
| High | C | Applied Logistic Regression | entity["people","David W Hosmer","biostatistics"] et al. | 2013 | Wiley Series in Probability and Statistics | 10.1002/9781118548387 | `https://doi.org/10.1002/9781118548387` citeturn16search3 | Practical, authoritative book to justify LR modeling choices, interpretation, and common pitfalls. | 04_methodology |
| High | C | Support-vector networks | entity["people","Corinna Cortes","support vector machines"] et al. | 1995 | Machine Learning (Springer) | 10.1007/BF00994018 | `https://doi.org/10.1007/BF00994018` citeturn12search0 | Definitive SVM theory reference; valuable for explaining RBF kernels and margin-based generalization. | 04_methodology |
| High | C | Random Forests | entity["people","Leo Breiman","random forests"] | 2001 | Machine Learning (Springer) | 10.1023/A:1010933404324 | `https://doi.org/10.1023/A:1010933404324` citeturn13search4 | Canonical foundation for RF; cite for ensemble intuition, variable importance discussion, and generalization. | 04_methodology |
| High | C | Greedy function approximation: A gradient boosting machine | entity["people","Jerome H Friedman","boosting"] | 2001 | The Annals of Statistics | 10.1214/aos/1013203451 | `https://doi.org/10.1214/aos/1013203451` citeturn12search4 | Foundational gradient boosting reference; key to justify GB vs RF and additive model perspective. | 04_methodology |
| High | C | XGBoost: A Scalable Tree Boosting System | entity["people","Tianqi Chen","xgboost"] et al. | 2016 | KDD ’16 (ACM) | 10.1145/2939672.2939785 | `https://doi.org/10.1145/2939672.2939785` citeturn15search4 | Core citation for XGBoost (shrinkage, regularization, sparsity-aware splits); also has widely reproduced tree-ensemble diagrams. | 04_methodology |
| Medium | C | The Elements of Statistical Learning: Data Mining, Inference, and Prediction (2nd ed.) | entity["people","Trevor Hastie","statistics and ml"] et al. | 2009 | Springer | 10.1007/978-0-387-84858-7 | `https://doi.org/10.1007/978-0-387-84858-7` citeturn19search1 | Broad, canonical ML reference; ideal to cite for bias–variance, regularization, trees/forests/boosting overview. | 04_methodology |
| Medium | C | Scikit-learn: Machine Learning in Python | entity["people","Fabian Pedregosa","scikit-learn"] et al. | 2011 | JMLR | N/A (JMLR) | `https://www.jmlr.org/papers/v12/pedregosa11a.html` citeturn19search5 | Cite for implementation grounding (standard algorithms, evaluation utilities) without citing non-peer-reviewed docs. | 04_methodology |
| High | D | Comparison of parametric representations for monosyllabic word recognition in continuously spoken sentences | entity["people","Steven B Davis","mfcc"] et al. | 1980 | IEEE Trans. Acoustics, Speech, and Signal Processing | 10.1109/TASSP.1980.1163420 | `https://doi.org/10.1109/TASSP.1980.1163420` citeturn20search9 | Classic MFCC reference. Useful if you describe MFCCs and cepstral-domain features in Dataset A/B feature sets. | 02_literature_review |
| High | D | Wavelet Transform With Tunable Q-Factor | entity["people","Ivan W Selesnick","wavelets"] | 2011 | IEEE Transactions on Signal Processing | 10.1109/TSP.2011.2143711 | `https://doi.org/10.1109/TSP.2011.2143711` citeturn20search3 | Primary source behind TQWT features in PD speech datasets; strengthens credibility of wavelet-based feature discussion. | 02_literature_review |
| Medium | D | On the use of autocorrelation analysis for pitch detection | entity["people","Lawrence R Rabiner","speech processing"] | 1977 | IEEE Trans. Acoustics, Speech, and Signal Processing | 10.1109/TASSP.1977.1162905 | `https://doi.org/10.1109/TASSP.1977.1162905` citeturn23search2 | Good citation if you explain F0 extraction fundamentals (autocorrelation and preprocessing), relevant to prosody/phonation features. | 04_methodology |
| Medium | D | On the use of autocorrelation for pitch extraction: Some statistical considerations and their application to the SIFT algorithm | entity["people","Michel Moulines","pitch extraction"] et al. | 1984 | Speech Communication (Elsevier) | 10.1016/0167-6393(84)90026-8 | `https://doi.org/10.1016/0167-6393(84)90026-8` citeturn23search7 | Strengthens your “pitch extraction isn’t trivial” narrative and can motivate smoothing/robust preprocessing choices. | 04_methodology |
| Medium | D | Extraction and representation of prosodic features for language and speaker recognition | entity["people","Sibylle Burger","prosody features"] et al. | 2008 | Speech Communication (Elsevier) | 10.1016/j.specom.2008.04.010 | `https://doi.org/10.1016/j.specom.2008.04.010` citeturn22search5 | Useful methods anchor for prosody features (F0, energy, duration contours), which overlap with PD speech impairment markers. | 02_literature_review |
| Medium | D | Improvements in estimating the harmonics-to-noise ratio of the voice | entity["people","S N Awan","voice acoustics"] et al. | 1994 | Journal of Voice (Elsevier) | 10.1016/S0892-1997(05)80297-8 | `https://doi.org/10.1016/S0892-1997(05)80297-8` citeturn21search2 | Peer-reviewed grounding for HNR computation—helps legitimize HNR-related features in your feature set description. | 04_methodology |
| Medium | D | Comparisons of jitter, shimmer, and signal-to-noise ratio from directly digitized versus taped voice samples | entity["people","M P Gelfer","voice quality"] et al. | 1995 | Journal of Voice (Elsevier) | 10.1016/S0892-1997(05)80199-7 | `https://doi.org/10.1016/S0892-1997(05)80199-7` citeturn21search4 | Supports a key “measurement caveat”: jitter/shimmer/SNR depend on recording conditions—relevant to smartphone audio. | 07_discussion |
| Medium | E | Mobile Device Voice Recordings at King’s College London (MDVR-KCL) from both early and advanced Parkinson's disease patients and healthy controls | Hagen Jaeger et al. | 2019 | Dataset (Zenodo) | 10.5281/zenodo.2867216 | `https://doi.org/10.5281/zenodo.2867216` citeturn5view0 | Official dataset citation for the raw-audio dataset; cite in Methods and Data sections for transparency/reproducibility. | 04_methodology |
| Medium | E | Parkinson's Disease Classification (Dataset) | C. Sakar et al. | 2018 | Dataset (UCI) | 10.24432/C5MS4X | `https://doi.org/10.24432/C5MS4X` citeturn2search2 | Official dataset citation for the pre-extracted-feature dataset; cite with explicit caveats re: subject IDs and leakage risk. | 04_methodology |
| Medium | A | Acoustic analysis of the voice in patients with Parkinson's disease and hypokinetic dysarthria | Sara Fernández-García et al. | 2020 | Revista de Logopedia, Foniatría y Audiología (Elsevier) | 10.1016/j.rlfa.2020.04.002 | `https://doi.org/10.1016/j.rlfa.2020.04.002` citeturn4search9 | Clinical-acoustic evidence linking PD to changes in F0, intensity, jitter/shimmer—useful to justify your feature families. | 02_literature_review |

## Top 20 must-add references

1. TRIPOD+AI statement (BMJ, 2024), DOI `10.1136/bmj-2023-078378`. citeturn1search1  
2. PROBAST+AI (BMJ, 2025), DOI `10.1136/bmj-2024-082505`. citeturn0search1  
3. Ge et al. (Artificial Intelligence in Medicine, 2023), DOI `10.1016/j.artmed.2023.102524`. citeturn2search1  
4. Varma & Simon (BMC Bioinformatics, 2006), DOI `10.1186/1471-2105-7-91`. citeturn1search0  
5. Cawley & Talbot (JMLR, 2010), URL `https://www.jmlr.org/papers/v11/cawley10a.html`. citeturn19search4  
6. Bengio & Grandvalet (JMLR, 2004), URL `https://jmlr.org/papers/v5/grandvalet04a.html`. citeturn19search0  
7. Davis & Goadrich (ICML/ACM, 2006), DOI `10.1145/1143844.1143874`. citeturn17search2  
8. Fawcett (Pattern Recognition Letters, 2006), DOI `10.1016/j.patrec.2005.10.010`. citeturn17search3  
9. Kalia & Lang (The Lancet, 2015), DOI `10.1016/S0140-6736(14)61393-3`. citeturn9search0  
10. Jankovic (JNNP, 2008), DOI `10.1136/jnnp.2007.131045`. citeturn7search3  
11. Little et al. (IEEE TBME, 2009), DOI `10.1109/TBME.2008.2005954`. citeturn3search2  
12. Cao et al. (npj Parkinson’s Disease, 2025), DOI `10.1038/s41531-025-00913-4`. citeturn6search2  
13. Sedigh Malekroodi et al. (MDPI Bioengineering, 2025), DOI `10.3390/bioengineering12111279`. citeturn6search6  
14. Davis & Mermelstein (IEEE TASSP, 1980), DOI `10.1109/TASSP.1980.1163420`. citeturn20search9  
15. Selesnick (IEEE TSP, 2011), DOI `10.1109/TSP.2011.2143711`. citeturn20search3  
16. Hosmer et al. (Wiley book, 2013), DOI `10.1002/9781118548387`. citeturn16search3  
17. Cortes & Vapnik (Springer Machine Learning, 1995), DOI `10.1007/BF00994018`. citeturn12search0  
18. Breiman (Springer Machine Learning, 2001), DOI `10.1023/A:1010933404324`. citeturn13search4  
19. Friedman (Annals of Statistics, 2001), DOI `10.1214/aos/1013203451`. citeturn12search4  
20. Chen & Guestrin (KDD/ACM, 2016), DOI `10.1145/2939672.2939785`. citeturn15search4  

## Nice-to-add references and rejected candidates

### Nice-to-add

- DeLong et al. (Biometrics, 1988) for AUC comparison methodology, DOI `10.2307/2531595`. citeturn18search0  
- Nelder & Wedderburn (JRSS A, 1972) for GLM foundations, DOI `10.2307/2344614`. citeturn16search0  
- Hastie, Tibshirani & Friedman (Springer, 2009) as a canonical ML textbook reference, DOI `10.1007/978-0-387-84858-7`. citeturn19search1  
- Pedregosa et al. (JMLR, 2011) to justify implementation-level choices in a peer-reviewed way, URL `https://www.jmlr.org/papers/v12/pedregosa11a.html`. citeturn19search5  
- Sakar & Kursun (Journal of Medical Systems, 2010) for dysphonia-based telediagnosis, DOI `10.1007/s10916-009-9272-y`. citeturn24search1  
- Sakar et al. (Applied Soft Computing, 2019) for TQWT-heavy engineered-feature PD classification, DOI `10.1016/j.asoc.2018.10.022`. citeturn24search3  
- Amato et al. (Health Information Science and Systems, 2021) for isolated-word PD speech classification, DOI `10.1007/s13755-021-00162-8`. citeturn6search10  
- “Digital speech biomarkers…” (npj Parkinson’s Disease, 2025) to discuss medication-state effects, DOI `10.1038/s41531-025-01045-5`. citeturn6search7  
- “Acoustic analysis of the voice…” (Elsevier, 2020) for clinical-acoustic correlates of hypokinetic dysarthria, DOI `10.1016/j.rlfa.2020.04.002`. citeturn4search9  

### Rejected candidates

- **Frontiers in Human Neuroscience** PD prosody model paper (publisher not in your allowed list). citeturn6search1  
- **JASA / Acoustical Society of America** papers on HNR and formants (high quality but not on your specified publisher list; also would expand scope unnecessarily). citeturn21search5turn21search10turn22search6  
- **Scientific.Net / Trans Tech** formant estimation papers (venue quality is unclear for your constraints; not recommended for an MSc thesis bibliography under “official publishers only”). citeturn22search1turn23search5  
- **IJERT** formant estimation (not on your allowed list; journal quality concerns). citeturn22search4  
- **Nature Precedings** version of the dysphonia telemonitoring work (preprint-era platform; prefer the IEEE TBME journal version). citeturn3search0turn3search2  

## BibTeX draft for Top 20 must-add papers

```bibtex
@article{collins2024tripod_ai,
  author  = {Collins, Gary S. and Moons, Karel G. M. and Dhiman, Paula and Riley, Richard D. and Beam, Andrew L. and Van Calster, Ben and Ghassemi, Marzyeh and Liu, Xiaoxuan and others},
  title   = {TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods},
  journal = {BMJ},
  year    = {2024},
  volume  = {385},
  pages   = {e078378},
  doi     = {10.1136/bmj-2023-078378},
  url     = {https://doi.org/10.1136/bmj-2023-078378}
}

@article{moons2025probast_ai,
  author  = {Moons, Karel G. M. and Damen, Johanna A. A. and Kaul, Tabea and Hooft, Lotty and Andaur Navarro, Constanza and Dhiman, Paula and Beam, Andrew L. and Van Calster, Ben and Celi, Leo Anthony and Denaxas, Spiros and Denniston, Alastair K. and Ghassemi, Marzyeh and Heinze, Georg and Kengne, Andre Pascal and Maier-Hein, Lena and Liu, Xiaoxuan and Logullo, Patricia and others},
  title   = {PROBAST+AI: an updated quality, risk of bias, and applicability assessment tool for prediction models using regression or artificial intelligence methods},
  journal = {BMJ},
  year    = {2025},
  volume  = {388},
  pages   = {e082505},
  doi     = {10.1136/bmj-2024-082505},
  url     = {https://doi.org/10.1136/bmj-2024-082505}
}

@article{ge2023overpromised,
  author  = {Ge, Wenbo and Lueck, Christian and Suominen, Hanna and Apthorp, Deborah},
  title   = {Has machine learning over-promised in healthcare?: A critical analysis and a proposal for improved evaluation, with evidence from Parkinson’s disease},
  journal = {Artificial Intelligence in Medicine},
  year    = {2023},
  volume  = {139},
  pages   = {102524},
  doi     = {10.1016/j.artmed.2023.102524},
  url     = {https://doi.org/10.1016/j.artmed.2023.102524}
}

@article{varma2006nestedcv,
  author  = {Varma, Sudhir and Simon, Richard},
  title   = {Bias in error estimation when using cross-validation for model selection},
  journal = {BMC Bioinformatics},
  year    = {2006},
  volume  = {7},
  pages   = {91},
  doi     = {10.1186/1471-2105-7-91},
  url     = {https://doi.org/10.1186/1471-2105-7-91}
}

@article{cawley2010selectionbias,
  author  = {Cawley, Gavin C. and Talbot, Nicola L. C.},
  title   = {On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation},
  journal = {Journal of Machine Learning Research},
  year    = {2010},
  volume  = {11},
  number  = {70},
  pages   = {2079--2107},
  url     = {https://www.jmlr.org/papers/v11/cawley10a.html}
}

@article{bengio2004no_unbiased_cv_variance,
  author  = {Bengio, Yoshua and Grandvalet, Yves},
  title   = {No Unbiased Estimator of the Variance of K-Fold Cross-Validation},
  journal = {Journal of Machine Learning Research},
  year    = {2004},
  volume  = {5},
  pages   = {1089--1105},
  url     = {https://jmlr.org/papers/v5/grandvalet04a.html}
}

@inproceedings{davis2006pr_roc,
  author    = {Davis, Jesse and Goadrich, Mark},
  title     = {The relationship between Precision-Recall and ROC curves},
  booktitle = {Proceedings of the 23rd International Conference on Machine Learning (ICML '06)},
  year      = {2006},
  pages     = {233--240},
  publisher = {ACM},
  doi       = {10.1145/1143844.1143874},
  url       = {https://doi.org/10.1145/1143844.1143874}
}

@article{fawcett2006roc,
  author  = {Fawcett, Tom},
  title   = {An introduction to ROC analysis},
  journal = {Pattern Recognition Letters},
  year    = {2006},
  volume  = {27},
  number  = {8},
  pages   = {861--874},
  doi     = {10.1016/j.patrec.2005.10.010},
  url     = {https://doi.org/10.1016/j.patrec.2005.10.010}
}

@article{kalia2015parkinsons_lancet,
  author  = {Kalia, Lorraine V. and Lang, Anthony E.},
  title   = {Parkinson's disease},
  journal = {The Lancet},
  year    = {2015},
  volume  = {386},
  number  = {9996},
  pages   = {896--912},
  doi     = {10.1016/S0140-6736(14)61393-3},
  url     = {https://doi.org/10.1016/S0140-6736(14)61393-3}
}

@article{jankovic2008clinical_features,
  author  = {Jankovic, Joseph},
  title   = {Parkinson’s disease: clinical features and diagnosis},
  journal = {Journal of Neurology, Neurosurgery \& Psychiatry},
  year    = {2008},
  volume  = {79},
  number  = {4},
  pages   = {368--376},
  doi     = {10.1136/jnnp.2007.131045},
  url     = {https://doi.org/10.1136/jnnp.2007.131045}
}

@article{little2009telemonitoring_dysphonia,
  author  = {Little, Max A. and McSharry, Patrick E. and Hunter, Eric J. and Spielman, Jennifer and Ramig, Lorraine O.},
  title   = {Suitability of dysphonia measurements for telemonitoring of Parkinson's disease},
  journal = {IEEE Transactions on Biomedical Engineering},
  year    = {2009},
  volume  = {56},
  number  = {4},
  pages   = {1015--1022},
  doi     = {10.1109/TBME.2008.2005954},
  url     = {https://doi.org/10.1109/TBME.2008.2005954}
}

@article{cao2025npj_speech_biomarkers,
  author  = {Cao, Fangyuan and Vogel, Adam P. and Gharahkhani, Puya and Renteria, Miguel E. and others},
  title   = {Speech and language biomarkers for Parkinson’s disease prediction, early diagnosis and progression},
  journal = {npj Parkinson's Disease},
  year    = {2025},
  volume  = {11},
  pages   = {57},
  doi     = {10.1038/s41531-025-00913-4},
  url     = {https://doi.org/10.1038/s41531-025-00913-4}
}

@article{malekroodi2025voice_systematic_review,
  author  = {Sedigh Malekroodi, Hadi and Lee, Byeong-il and Yi, Myunggi},
  title   = {Voice-Based Detection of Parkinson’s Disease Using Machine and Deep Learning Approaches: A Systematic Review},
  journal = {Bioengineering},
  year    = {2025},
  volume  = {12},
  number  = {11},
  pages   = {1279},
  doi     = {10.3390/bioengineering12111279},
  url     = {https://doi.org/10.3390/bioengineering12111279}
}

@article{davis1980mfcc,
  author  = {Davis, Steven B. and Mermelstein, Paul},
  title   = {Comparison of parametric representations for monosyllabic word recognition in continuously spoken sentences},
  journal = {IEEE Transactions on Acoustics, Speech, and Signal Processing},
  year    = {1980},
  volume  = {28},
  number  = {4},
  pages   = {357--366},
  doi     = {10.1109/TASSP.1980.1163420},
  url     = {https://doi.org/10.1109/TASSP.1980.1163420}
}

@article{selesnick2011tqwt,
  author  = {Selesnick, Ivan W.},
  title   = {Wavelet Transform With Tunable Q-Factor},
  journal = {IEEE Transactions on Signal Processing},
  year    = {2011},
  volume  = {59},
  number  = {8},
  pages   = {3560--3575},
  doi     = {10.1109/TSP.2011.2143711},
  url     = {https://doi.org/10.1109/TSP.2011.2143711}
}

@book{hosmer2013applied_logistic_regression,
  author    = {Hosmer, David W. and Lemeshow, Stanley and Sturdivant, Rodney X.},
  title     = {Applied Logistic Regression},
  publisher = {Wiley},
  year      = {2013},
  doi       = {10.1002/9781118548387},
  url       = {https://doi.org/10.1002/9781118548387}
}

@article{cortes1995svm,
  author  = {Cortes, Corinna and Vapnik, Vladimir},
  title   = {Support-vector networks},
  journal = {Machine Learning},
  year    = {1995},
  volume  = {20},
  pages   = {273--297},
  doi     = {10.1007/BF00994018},
  url     = {https://doi.org/10.1007/BF00994018}
}

@article{breiman2001random_forests,
  author  = {Breiman, Leo},
  title   = {Random Forests},
  journal = {Machine Learning},
  year    = {2001},
  volume  = {45},
  number  = {1},
  pages   = {5--32},
  doi     = {10.1023/A:1010933404324},
  url     = {https://doi.org/10.1023/A:1010933404324}
}

@article{friedman2001gbm,
  author  = {Friedman, Jerome H.},
  title   = {Greedy function approximation: A gradient boosting machine},
  journal = {The Annals of Statistics},
  year    = {2001},
  volume  = {29},
  number  = {5},
  pages   = {1189--1232},
  doi     = {10.1214/aos/1013203451},
  url     = {https://doi.org/10.1214/aos/1013203451}
}

@inproceedings{chen2016xgboost,
  author    = {Chen, Tianqi and Guestrin, Carlos},
  title     = {XGBoost: A Scalable Tree Boosting System},
  booktitle = {Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '16)},
  year      = {2016},
  pages     = {785--794},
  publisher = {ACM},
  doi       = {10.1145/2939672.2939785},
  url       = {https://doi.org/10.1145/2939672.2939785}
}
```

## How to weave these citations into your chapters

In `02_literature_review`, a robust structure is: clinical PD overview → speech/voice manifestations and “speech as biomarker” framing → specific voice/dysphonia feature families → what prior ML papers did and why results can inflate. Use the clinical reviews to define PD heterogeneity and diagnostic limitations, then pivot to dysphonia telemonitoring and modern reviews that catalog speech biomarkers across tasks (phonation, read speech, spontaneous speech). citeturn9search0turn7search3turn6search2turn3search2

In `04_methodology`, treat feature families and model families as *methods with citations*: MFCCs (IEEE classic), pitch/prosody extraction (IEEE/Speech Communication), HNR/jitter/shimmer (Journal of Voice), and any wavelet/TQWT mention anchored to the IEEE TSP paper. citeturn20search9turn23search2turn22search5turn21search2turn20search3

In `05_experimental_design`, explicitly justify your validation choice and your reporting style (mean±std, cautious comparisons). This is where the “CV bias / selection bias / uncertainty” cluster belongs: Varma–Simon for CV-with-model-selection bias, Cawley–Talbot for selection bias, Bengio–Grandvalet for variance/uncertainty caveats, and Davis–Goadrich plus Fawcett for metric selection. citeturn1search0turn19search4turn19search0turn17search2turn17search3

In `07_discussion`, frame limitations using *PROBAST+AI* and the PD-specific “inflationary effects” critique by Ge et al.—this gives you a principled way to say “these results are promising but not clinically deployable without external validation and bias control,” without sounding ad hoc. citeturn0search1turn2search1

Quality gate confirmation: the Top 20 listed above are drawn from peer-reviewed venues and/or official scientific sources across the allowed publisher set (BMJ, Elsevier, Springer, IEEE, Nature Portfolio, MDPI, JMLR, Oxford Academic, ACM), include multiple generic methodological/foundational references beyond PD-specific papers, and do not cite your thesis/repository as prior literature. citeturn1search1turn0search1turn2search1turn12search0turn13search4turn20search9turn6search2