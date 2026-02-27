# **Pathological Speech Analysis and Machine Learning Foundations for Parkinsonian Dysphonia Classification**

## **The Global Clinical Landscape and Etiological Context of Parkinson’s Disease**

The escalating prevalence of Parkinson’s disease (PD) represents a primary concern for global public health, characterized by a complex intersection of neurodegenerative decline and significant socio-economic burden. According to recent assessments by the World Health Organization, Parkinson's disease is the fastest-growing neurological disorder worldwide, with a prevalence that has more than doubled over the past two decades \[who\_pd\_fact\_sheet\_2023\]. This condition is defined as a progressive neurodegenerative disorder primarily affecting the dopaminergic neurons in the substantia nigra pars compacta. The resulting dopamine depletion leads to a classic constellation of motor symptoms, including tremors, bradykinesia, postural instability, and rigidity.1 However, the clinical manifestation of the disease is highly heterogeneous, often preceded by a prodromal phase where non-motor symptoms—such as olfactory loss, sleep disturbances, and subtle changes in speech—may appear years before a definitive clinical diagnosis can be established.1

The diagnostic process for Parkinson’s disease remains fundamentally clinical, often relying on structured assessments such as the Movement Disorder Society-Unified Parkinson’s Disease Rating Scale (MDS-UPDRS).2 Despite the utility of these scales, they are inherently subjective, periodic, and dependent on the expertise of specialized neurologists. This diagnostic lag often means that by the time a patient is diagnosed based on gross motor symptoms, a significant percentage of dopaminergic neurons have already been lost. Consequently, there is an urgent research imperative to identify objective, non-invasive digital biomarkers that can facilitate early detection and continuous monitoring of disease progression.1

Voice and speech alterations, collectively termed hypokinetic dysarthria, are among the most pervasive early indicators of Parkinsonian decline, affecting nearly 90% of the patient population.3 These vocal changes arise from the impairment of the intricate neural and motor systems responsible for speech production. Specifically, the disease compromises the brain regions involved in the initiation, planning, and execution of vocal movements, resulting in a distinct signature of vocal fold dysfunction and articulatory imprecision.2

| Clinical Feature | Physiological Basis | Acoustic Manifestation |
| :---- | :---- | :---- |
| Hypophonia | Reduced subglottal pressure and glottal closure. | Decreased intensity (loudness) and dynamic range. |
| Monopitch | Rigidity of the cricothyroid and vocalis muscles. | Reduced fundamental frequency (![][image1]) variability. |
| Breathiness | Incomplete vocal fold adduction (vocal fold bowing). | Increased aspiration noise and decreased HNR. |
| Dysfluency | Impaired motor timing and cognitive-linguistic shifts. | Involuntary pauses and altered speech rate. |
| Imprecise Consonants | Reduced range of motion in tongue and lips. | Blurred formant transitions and spectral shifts. |

The potential of speech-based biomarkers lies in their accessibility; vocal data can be captured via ubiquitous mobile devices, enabling remote telediagnosis and telemonitoring.7 However, the path from experimental observation to clinical utility is fraught with methodological challenges, including the risk of data leakage, the need for robust validation frameworks, and the requirement for transparent reporting.9

## **Biomechanical Foundations of Phonation and Pathological Dysphonia**

A comprehensive understanding of voice-based classification must be rooted in the physical laws of voice production. The "source-filter" model remains the dominant paradigm for describing speech acoustics. In this framework, the larynx acts as the sound source, where the vibration of the vocal folds modulates the pulmonary airflow to create a glottal spectrum rich in harmonics.6 This glottal signal is subsequently modified by the vocal tract, which functions as a frequency-selective filter, attenuating or amplifying specific frequencies to produce formants.6

In neurotypical phonation, the vocal folds undergo symmetric and periodic oscillation, driven by the interaction of subglottal pressure and the elastic properties of the laryngeal tissues—a process often described by the myoelastic-aerodynamic theory of phonation.14 However, in Parkinson's disease, the rigidity and bradykinesia characteristic of the disorder lead to profound changes in the geometry and biomechanical properties of the vocal folds.15 These alterations frequently manifest as "vocal fold bowing," where the folds fail to meet completely at the midline during the closed phase of the glottal cycle. This incomplete adduction allows air to escape, creating turbulent noise that is perceived as breathiness or hoarseness.2

Beyond the laryngeal source, the "filter" or articulatory system is also significantly impacted. The rigidity of the tongue and facial muscles leads to "vowel centralization," where the articulatory space is reduced, and the distinctness of different vowel sounds is blurred.2 This is acoustically reflected in the compression of the formant space, particularly in the relationship between the first and second formants (![][image2] and ![][image3]), which correspond to tongue height and advancement, respectively.12

One of the landmark advancements in Parkinsonian voice analysis was the identification of nonlinear dynamics in pathological vocal signals. Traditional measures of voice quality, such as jitter (frequency perturbation) and shimmer (amplitude perturbation), often fail to capture the chaotic nature of voice in advanced neurodegeneration.7 To address this, non-standard measures like Recurrence Period Density Entropy (RPDE) and Detrended Fluctuation Analysis (DFA) were introduced. These metrics quantify the stochasticity and fractal scaling properties of the voice, providing a more robust characterization of the "dysphonia fingerprint" that differentiates PD subjects from healthy controls.7

## **Digital Signal Processing for Feature Extraction and Speech Representation**

The efficacy of any machine learning model in this domain is critically dependent on the quality of the feature extraction pipeline. In the context of Parkinson’s disease, researchers generally utilize three primary tiers of acoustic features: time-domain perturbation measures, frequency-domain spectral/cepstral features, and nonlinear dynamical features.2

### **Time-Domain and Perturbation Features**

Time-domain features focus on the cycle-to-cycle variability of the speech waveform. Jitter and shimmer represent the most classical metrics for quantifying vocal stability.4 Jitter is defined as the variation in the fundamental frequency (![][image1]) or the pitch period, while shimmer quantifies the variation in the peak-to-peak amplitude. In Parkinsonian speech, these values are typically elevated, reflecting the lack of precise neural control over the laryngeal muscles.4

![][image4]  
Where ![][image5] represents the period of the ![][image6]\-th glottal cycle. While these measures are foundational, they are highly sensitive to background noise and the specific methods used for pitch tracking, necessitating cautious interpretation in telediagnosis settings.7

### **Spectral and Cepstral Analysis**

Spectral features analyze the distribution of energy across the frequency spectrum. A key measure is the Harmonics-to-Noise Ratio (HNR), which quantifies the ratio between the periodic component (harmonics) and the stochastic component (noise) of the signal.4 A lower HNR is a hallmark of Parkinsonian dysphonia, indicating a breathy or harsh voice quality.4

The Mel-Frequency Cepstral Coefficients (MFCCs) represent a more sophisticated representation of the speech signal, bridging the gap between acoustics and human perception. Introduced by Davis and Mermelstein in 1980, MFCCs involve a transformation of the power spectrum to the Mel scale—a nonlinear frequency scale that approximates the human auditory system's pitch perception.17 The extraction process involves:

1. Short-term Fourier Transform (STFT) of the signal.  
2. Mapping the powers of the spectrum onto the Mel scale using a filter bank.  
3. Taking the log of the powers at each Mel frequency.  
4. Applying a Discrete Cosine Transform (DCT) to the logs.

The resulting coefficients capture the "envelope" of the spectrum, effectively representing the shape of the vocal tract (the filter) while being relatively independent of the glottal source (the pitch).13 In PD classification, lower-order MFCCs are often highly discriminative, as they reflect the articulatory imprecision and formant shifting characteristic of the disease.4

### **Nonlinear and Wavelet-Based Features**

Given the chaotic nature of pathological voice, nonlinear features have gained prominence. Pitch Period Entropy (PPE) was specifically developed to detect the impaired ability of PD patients to maintain a steady fundamental frequency.7 Unlike traditional jitter, PPE is robust to normal, healthy pitch variations and focuses on the frequency-modulation signatures that are physiologically specific to Parkinsonism.7

Furthermore, recent studies have utilized the Tunable Q-factor Wavelet Transform (TQWT) to decompose speech signals into different sub-bands.4 This approach is particularly effective for high-dimensional datasets like the UCI Parkinson’s Disease Classification dataset, as it allows the model to capture transient changes and high-frequency components that are often missed by traditional spectral analysis.4

| Feature Class | Key Examples | Primary Utility in PD |
| :---- | :---- | :---- |
| Perturbation | Jitter, Shimmer | Basic quantification of vocal stability. |
| Noise-related | HNR, NHR | Measures glottal efficiency and breathiness. |
| Cepstral | MFCCs, LPCCs | Captures vocal tract shape and articulation. |
| Nonlinear | PPE, RPDE, DFA | Detects chaotic vibration and neural instability. |
| Wavelet | TQWT coefficients | High-resolution multi-band analysis. |

## **Foundations of Classical Machine Learning Algorithms in Healthcare**

The selection of a classification algorithm is a pivotal decision in medical research, where the trade-off between predictive accuracy and clinical interpretability is a constant consideration. While deep learning architectures have demonstrated impressive results on large-scale datasets, classical machine learning remains the gold standard for clinical studies with limited sample sizes, providing greater transparency and resistance to overfitting.3

### **Statistical Origins: Logistic Regression**

Logistic regression is the foundational algorithm for binary classification, deeply rooted in the statistical tradition of clinical research. Originally formalized by D.R. Cox in 1958 for the analysis of binary sequences, it remains the most common method for modeling binary outcomes in epidemiology.22 Logistic regression models the probability that a given input ![][image7] belongs to a specific class (e.g., PD vs. HC) using the logistic (sigmoid) function:

![][image8]  
This function maps any real-valued number into the range $$, making it ideal for probability estimation.26 From a machine learning perspective, the model is "trained" by maximizing the log-likelihood of the training data or minimizing the cross-entropy loss.27 The primary advantage of logistic regression in Parkinson’s research is its inherent interpretability; the coefficients (or weights) assigned to each acoustic feature can be converted into odds ratios, allowing clinicians to understand exactly which vocal parameters most significantly influence the diagnosis.21

### **Structural Risk Minimization: Support Vector Machines**

Support Vector Machines (SVM), introduced by Cortes and Vapnik in 1995, represent a shift toward the principle of structural risk minimization.30 SVM seeks to find the hyperplane in a high-dimensional space that maximizes the margin between two classes. For data that is not linearly separable in the original feature space—such as complex speech features—SVM utilizes "kernel methods" to implicitly map the data into a higher-dimensional space where a linear boundary can be established.31

The Radial Basis Function (RBF) kernel is particularly popular in PD classification:

![][image9]  
This kernel allows the SVM to capture intricate, nonlinear relationships between features, such as the interaction between pitch entropy and cepstral dynamics.30 SVM-RBF models have consistently achieved high performance in PD detection tasks, often serving as a strong baseline against more complex ensemble methods.1

### **Ensemble Learning: Random Forests and Gradient Boosting**

Ensemble learning involves combining multiple individual models to improve generalization and stability. Random Forest, proposed by Leo Breiman in 2001, is an ensemble of decision trees trained using "bagging" (bootstrap aggregating).35 Each tree is trained on a random subset of the data and a random subset of the features, and the final prediction is made by majority voting. This randomness reduces the variance of the model and makes it robust to noise and outliers, which are common in real-world voice recordings.37

Boosting, on the other hand, builds trees sequentially, where each new tree aims to minimize the residual errors of the previous ones.39 Jerome Friedman’s Gradient Boosting Machine (GBM) framed this as an optimization problem where trees are added to minimize a loss function using gradient descent.39

XGBoost (Extreme Gradient Boosting), introduced by Chen and Guestrin in 2016, refined this approach by adding a regularized objective function to prevent overfitting and implementing efficient algorithms for handling sparse data.20

![][image10]  
Where ![][image11] represents the regularization term that penalizes the complexity of the trees.20 In current literature, XGBoost and Random Forest often outperform other classical models on tabular speech datasets, achieving accuracies and ROC-AUC scores exceeding 0.90 in well-validated studies.1

| Algorithm | Foundation | Optimization Goal | Key Advantage |
| :---- | :---- | :---- | :---- |
| Logistic Regression | Statistical Inference | Log-likelihood maximization. | Interpretability; odds ratios. |
| SVM (RBF) | Structural Risk | Margin maximization. | Robustness to non-linearity. |
| Random Forest | Bagging (Ensemble) | Variance reduction (Voting). | Stability; feature importance. |
| XGBoost | Boosting (Ensemble) | Gradient descent with regularization. | State-of-the-art accuracy. |

## **Methodological Rigor: Data Leakage, Validation, and Bias Mitigation**

Despite the high performance reported in many studies, the translation of machine learning models into clinical practice is hindered by a widespread lack of methodological rigor. A critical analysis by Ge et al. (2023) suggests that machine learning in healthcare has often over-promised due to "inflationary" evaluation practices, particularly in the field of Parkinson’s disease \[ge2023inflation\].

### **The Peril of Data Leakage**

The most common source of performance inflation is "data leakage," which occurs when information from the testing set "leaks" into the training process.9 In PD voice research, this frequently happens during data splitting. Many datasets, such as the UCI Parkinson’s dataset or the MDVR-KCL dataset, contain multiple recordings per subject.4 If the data is split "recording-wise"—where different recordings of the *same* subject appear in both the training and testing sets—the model may simply learn to identify the unique vocal characteristics of the individual rather than the generalizable features of the disease.9

Research has demonstrated that recording-wise splitting leads to "over-optimistic" results, with accuracies often approaching 100%, whereas proper "subject-wise" splitting reveals much lower and more realistic performance.9 To ensure clinical validity, researchers must employ **Grouped Cross-Validation**, where all samples belonging to a specific subject ID are kept within the same fold.9

### **Bias in Model Selection and Nested Cross-Validation**

A second critical issue is "selection bias" in model selection. Varma and Simon (2006) highlighted that if cross-validation is used simultaneously for both hyperparameter tuning and performance evaluation, the resulting error estimate is biased \[varma2006nestedcv\]. This is because the tuning process effectively "overfits" to the validation data by picking the best-performing model out of hundreds of trials.48

The solution is **Nested Cross-Validation**, which utilizes an "inner loop" for hyperparameter optimization and an "outer loop" for unbiased performance estimation.48 By treating model selection as an integral part of the model fitting process, researchers can ensure that their results generalize to entirely new participant cohorts.49

| Bias Type | Mechanism | Mitigation Strategy |
| :---- | :---- | :---- |
| Data Leakage | Same subject in train/test sets. | Subject-wise (Grouped) CV. |
| Model Selection Bias | Tuning and testing on same CV loop. | Nested Cross-Validation. |
| Feature Leakage | Scaling/imputation on whole dataset. | Pipeline integration (fit on train only). |
| Sampling Bias | Class imbalance (PD \>\> HC). | Stratified splitting; weighting; SMOTE. |

## **Systematic Reporting and Risk of Bias Assessment Tools**

To address the "reproducibility crisis" in healthcare AI, the scientific community has developed a series of standardized reporting guidelines. These frameworks are designed to ensure that every aspect of the machine learning pipeline—from data collection to model evaluation—is transparent and reproducible.50

### **The TRIPOD+AI Statement (2024)**

The TRIPOD+AI (Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis plus Artificial Intelligence extension) is the most significant recent development in clinical AI reporting. Published in April 2024, it updates the original 2015 TRIPOD statement to explicitly address the unique challenges of machine learning.50

Key requirements of TRIPOD+AI include:

* **Transparency of Data Sources**: Detailed description of the study population, including how participants were recruited and their clinical characteristics.51  
* **Model Specification**: Clear reporting of all preprocessing steps, feature selection methods, and hyperparameter settings.51  
* **Calibration Reporting**: Moving beyond simple accuracy to report how well the predicted probabilities align with observed results, often using calibration plots.51  
* **Evaluation on External Data**: Emphasizing the distinction between internal validation (within the same population) and external evaluation (on a different population).51

### **PROBAST+AI and Risk of Bias (2025)**

Complementing TRIPOD+AI, the PROBAST+AI (Prediction model Risk Of Bias Assessment Tool \+ Artificial Intelligence) tool provides a framework for evaluating the quality and applicability of existing models.52 Published in March 2025, it uses a series of "signaling questions" across four domains—Participants, Predictors, Outcome, and Analysis—to identify potential biases that could lead to over-optimistic performance or limited clinical utility.52

By adhering to these standards, researchers can bridge the "mismatch" between AI research and clinical epidemiology, ensuring that voice-based Parkinson’s detection tools are not only accurate in a laboratory setting but also safe and effective for real-world deployment.53

## **Dataset Context: MDVR-KCL and UCI PD Classification**

The robustness of Parkinson’s voice research is ultimately tethered to the quality of available datasets. Two primary datasets dominate the current landscape, each presenting unique opportunities and caveats.

### **The MDVR-KCL Dataset**

The Mobile Device Voice Recordings at King's College London (MDVR-KCL) dataset provides high-quality, raw audio recordings captured via a smartphone in a clinical setting.4

* **Audio Quality**: Recordings are mono, 16-bit WAV files at 44.1 kHz, captured directly from the microphone to avoid GSM compression artifacts.4  
* **Task Diversity**: It includes both "ReadText" (reading a standard passage) and "SpontaneousDialogue" tasks.4  
* **Metadata**: Includes clinical scores such as Hoehn & Yahr stages and UPDRS speech scores, facilitating more than just binary classification.4  
* **Methodological Advantage**: Because subject IDs are preserved, it allows for rigorous subject-wise grouped cross-validation.4

### **The UCI PD Classification Dataset (2018)**

The UCI Parkinson’s Disease Classification dataset is one of the most widely used benchmarks in the field, though it requires cautious handling.4

* **Content**: It consists of pre-extracted features from 188 PD subjects and 64 healthy controls performing sustained vowel phonation.4  
* **Feature Complexity**: Includes over 750 features ranging from traditional jitter/shimmer to complex TQWT and Wavelet representations.4  
* **Caveats**: The lack of raw audio means feature extraction cannot be verified, and the primary CSV distribution often lacks clear subject identifiers, making it highly susceptible to data leakage if not handled carefully.4

| Dataset | Type | Sample Rate | Key Advantage | Major Caveat |
| :---- | :---- | :---- | :---- | :---- |
| **MDVR-KCL** | Raw Audio | 44,100 Hz | Natural speech tasks; subject IDs present. | Smaller sample size. |
| **UCI PD (2018)** | Pre-extracted | 44,100 Hz | High-dimensional (TQWT); large N. | No raw audio; leakage risk. |

## **Future Outlook: Explainable AI and Trustworthy Deployment**

As the field of Parkinsonian speech analysis matures, the focus is shifting from achieving the highest possible accuracy to ensuring that AI systems are trustworthy, fair, and deployable. The FUTURE-AI guidelines (2025) represent an international consensus on these principles, emphasizing fairness across demographic subgroups (age, sex, ethnicity) and the need for clinical interpretability.56

One of the most promising avenues for increasing trust is the use of "Explainable AI" (XAI) techniques such as SHAP (SHapley Additive exPlanations). SHAP values provide a mathematically rigorous way to assign importance to each feature for an *individual* prediction.21 By visualizing which acoustic perturbations led to a specific PD diagnosis, researchers can bridge the gap between "black-box" models and clinical intuition.

Ultimately, the goal is to integrate these models into a "care pathway"—a structured plan for managing the patient’s healthcare journey.51 By providing objective, daily snapshots of a patient's vocal health, machine learning tools can help clinicians fine-tune medication dosages and intervene earlier when a decline is detected, fundamentally transforming the management of Parkinson’s disease.2

## **Integrating the "Top 20 Must-Add" Bibliography for Parkinson’s Voice Research**

To strengthen the scientific grounding of any thesis in this domain, the following high-quality, peer-reviewed sources should be integrated into the bibliography. These represent the canonical works in laryngeal physiology, machine learning foundations, and modern clinical reporting standards.

### **Foundational Algorithmic Papers**

1. **Cox, D. R. (1958)**: "The Regression Analysis of Binary Sequences," *Journal of the Royal Statistical Society: Series B*. The definitive root of Logistic Regression in clinical research.25  
2. **Cortes, C. & Vapnik, V. (1995)**: "Support-vector networks," *Machine Learning*. The original formulation of SVM and kernel methods.31  
3. **Breiman, L. (2001)**: "Random Forests," *Machine Learning*. Foundational for the most robust classical ensemble method.37  
4. **Friedman, J. H. (2001)**: "Greedy function approximation: A gradient boosting machine," *The Annals of Statistics*. Establishes the mathematical framework for boosting.39  
5. **Chen, T. & Guestrin, C. (2016)**: "XGBoost: A Scalable Tree Boosting System," *KDD*. The modern state-of-the-art for clinical tabular data.20

### **Speech Signal Processing and PD Foundations**

6. **Davis, S. & Mermelstein, P. (1980)**: "Comparison of parametric representations for monosyllabic word recognition," *IEEE TASSP*. The origin of MFCCs.17  
7. **Titze, I. R. (1994)**: *Principles of Voice Production*, Prentice Hall. The "bible" of laryngeal biomechanics and phonation physics.58  
8. **Little, M. A. et al. (2009)**: "Suitability of dysphonia measurements for telemonitoring of Parkinson's disease," *IEEE TBME*. Introduced PPE and the nonlinear framework for PD.7  
9. **Rusz, J. et al. (2011)**: "Quantitative acoustic measurements for characterization of speech and voice disorders in early untreated Parkinson’s disease," *JASA*. Defines early vocal biomarkers.4  
10. **Sakar, C. O. et al. (2019)**: "A comparative analysis of speech signal processing algorithms for Parkinson’s disease classification," *Applied Soft Computing*. Documentation for the modern UCI dataset.4

### **Methodological Rigor and Reporting Standards**

11. **Collins, G. S. et al. (2024)**: "TRIPOD+AI statement: updated guidance for reporting clinical prediction models," *BMJ*. The primary modern reporting standard.51  
12. **Moons, K. G. M. et al. (2025)**: "PROBAST+AI: an updated quality, risk of bias, and applicability assessment tool," *BMJ*. Critical for bias evaluation.52  
13. **Ge, W. et al. (2023)**: "Has machine learning over-promised in healthcare?," *Artificial Intelligence in Medicine*. A necessary critical perspective on PD research \[ge2023inflation\].  
14. **Varma, S. & Simon, R. (2006)**: "Bias in error estimation when using cross-validation for model selection," *BMC Bioinformatics*. Foundation for nested cross-validation \[varma2006nestedcv\].  
15. **Cawley, G. & Talbot, N. (2010)**: "On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation," *JMLR*. Explains why model selection must be part of the validation pipeline.48

### **Recent Systematic Reviews (2024-2025)**

16. **Xavier, R. et al. (2025)**: "Voice analysis in Parkinson's disease—a systematic literature review," *Artificial Intelligence in Medicine*. The most recent comprehensive survey.4  
17. **Wright, L. & Aharonson, V. (2025)**: "Vocal Feature Changes for Monitoring Parkinson's Disease Progression—A Systematic Review," *Brain Sciences*. Focuses on longitudinal monitoring.4  
18. **Cao, H. et al. (2025)**: "Speech and language biomarkers for Parkinson's disease prediction," *npj Parkinson's Disease*. High-impact review on the "biomarker" status of voice.4  
19. **Sedigh Malekroodi, A. et al. (2025)**: "Voice-Based Detection of Parkinson's Disease Using Machine and Deep Learning Approaches," *Bioengineering*. Compares classical vs. modern DL techniques.4  
20. **Solana-Lavalle, G. & Rosas-Romero, R. (2021)**: "Analysis of voice as an assisting tool for detection of Parkinson's disease," *BSPC*. Provides a rigorous evaluation of the UCI benchmark.4

## **Synthesis of Insight and Methodological Recommendations**

To conclude, the path toward a scientifically robust and clinically useful Parkinson’s voice classification system requires a shift away from "accuracy chasing" toward a more nuanced, evidence-based approach. The synthesis of this analysis leads to several critical recommendations for improving the grounding of such research.

First, the integration of biomechanical context—specifically the source-filter theory and the nonlinear dynamics of the larynx—is essential for interpreting *why* specific features like MFCCs or PPE are effective. Without this grounding, the models remain "black boxes" that lack clinical credibility. Second, the strict adoption of subject-wise, grouped cross-validation is a non-negotiable requirement to prevent data leakage and provide realistic estimates of performance. Models that fail this test should be viewed with skepticism.

Third, the pursuit of "nested cross-validation" must become standard practice to avoid the subtle selection biases that occur during hyperparameter tuning. Finally, the use of transparent reporting frameworks like TRIPOD+AI and the risk-of-bias assessments of PROBAST+AI will elevate the research from a computational experiment to a valid clinical study. By centering these principles, the research community can fulfill the promise of voice-based digital biomarkers, offering a non-invasive, objective, and transformative tool for the millions affected by Parkinson's disease.

#### **Πηγές αναφοράς**

1. Detection of Parkinson's disease based on voice patterns ranking and optimized support vector machine | Request PDF \- ResearchGate, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.researchgate.net/publication/331443172\_Detection\_of\_Parkinson's\_disease\_based\_on\_voice\_patterns\_ranking\_and\_optimized\_support\_vector\_machine](https://www.researchgate.net/publication/331443172_Detection_of_Parkinson's_disease_based_on_voice_patterns_ranking_and_optimized_support_vector_machine)  
2. Overview of Automatic Speech Analysis and Technologies for Neurodegenerative Disorders: Diagnosis and Assistive Applications \- arXiv, πρόσβαση Φεβρουαρίου 27, 2026, [https://arxiv.org/html/2501.03536v2](https://arxiv.org/html/2501.03536v2)  
3. Voice classification in Parkinson's disease \- Lirias, πρόσβαση Φεβρουαρίου 27, 2026, [https://lirias.kuleuven.be/retrieve/3b88b7b3-cde2-4a11-8ba9-7273d7f5359f](https://lirias.kuleuven.be/retrieve/3b88b7b3-cde2-4a11-8ba9-7273d7f5359f)  
4. references.bib  
5. (PDF) Time Series Classification of Raw Voice Waveforms for Parkinson's Disease Detection Using Generative Adversarial Network-Driven Data Augmentation \- ResearchGate, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.researchgate.net/publication/386060788\_Time\_Series\_Classification\_of\_Raw\_Voice\_Waveforms\_for\_Parkinson's\_Disease\_Detection\_Using\_Generative\_Adversarial\_Network-Driven\_Data\_Augmentation](https://www.researchgate.net/publication/386060788_Time_Series_Classification_of_Raw_Voice_Waveforms_for_Parkinson's_Disease_Detection_Using_Generative_Adversarial_Network-Driven_Data_Augmentation)  
6. Mechanics of human voice production and control \- PMC \- NIH, πρόσβαση Φεβρουαρίου 27, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC5412481/](https://pmc.ncbi.nlm.nih.gov/articles/PMC5412481/)  
7. Suitability of dysphonia measurements for telemonitoring of Parkinson's disease., πρόσβαση Φεβρουαρίου 27, 2026, [http://publications.aston.ac.uk/18328/](http://publications.aston.ac.uk/18328/)  
8. Suitability of dysphonia measurements for telemonitoring of Parkinson's disease \- PubMed, πρόσβαση Φεβρουαρίου 27, 2026, [https://pubmed.ncbi.nlm.nih.gov/21399744/](https://pubmed.ncbi.nlm.nih.gov/21399744/)  
9. (PDF) Data Complexity-Aware Feature Selection with Symmetric Splitting for Robust Parkinson's Disease Detection \- ResearchGate, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.researchgate.net/publication/399000940\_Data\_Complexity-Aware\_Feature\_Selection\_with\_Symmetric\_Splitting\_for\_Robust\_Parkinson's\_Disease\_Detection](https://www.researchgate.net/publication/399000940_Data_Complexity-Aware_Feature_Selection_with_Symmetric_Splitting_for_Robust_Parkinson's_Disease_Detection)  
10. Parkinson's Disease Detection from Speech Data Using Higher Order Dynamical Mode Decomposition \- ResearchGate, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.researchgate.net/publication/400331800\_Parkinson's\_Disease\_Detection\_from\_Speech\_Data\_Using\_Higher\_Order\_Dynamical\_Mode\_Decomposition](https://www.researchgate.net/publication/400331800_Parkinson's_Disease_Detection_from_Speech_Data_Using_Higher_Order_Dynamical_Mode_Decomposition)  
11. National Center for Voice and Speech, πρόσβαση Φεβρουαρίου 27, 2026, [https://nationalcenterforvoiceandspeech.myshopify.com/](https://nationalcenterforvoiceandspeech.myshopify.com/)  
12. principles of voice production-ingo titze \- VoiceScienceWorks, πρόσβαση Φεβρουαρίου 27, 2026, [http://www.voicescienceworks.org/old-book-reviews-page/principles-of-voice-production-ingo-titze](http://www.voicescienceworks.org/old-book-reviews-page/principles-of-voice-production-ingo-titze)  
13. Exploring the Articulatory Perspective of Mel-Frequency Cepstral Coefficients: Unravelling the Link between MFCCs and Vocal Tract Features \- ResearchGate, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.researchgate.net/profile/Bruce-Xiao-Wang/publication/372240974\_Exploring\_the\_Articulatory\_Perspective\_of\_Mel-Frequency\_Cepstral\_Coefficients\_Unravelling\_the\_Link\_between\_MFCCs\_and\_Vocal\_Tract\_Features/links/64ac118eb9ed6874a50b5f4e/Exploring-the-Articulatory-Perspective-of-Mel-Frequency-Cepstral-Coefficients-Unravelling-the-Link-between-MFCCs-and-Vocal-Tract-Features.pdf](https://www.researchgate.net/profile/Bruce-Xiao-Wang/publication/372240974_Exploring_the_Articulatory_Perspective_of_Mel-Frequency_Cepstral_Coefficients_Unravelling_the_Link_between_MFCCs_and_Vocal_Tract_Features/links/64ac118eb9ed6874a50b5f4e/Exploring-the-Articulatory-Perspective-of-Mel-Frequency-Cepstral-Coefficients-Unravelling-the-Link-between-MFCCs-and-Vocal-Tract-Features.pdf)  
14. Principles of Voice Production \- Ncvs.org, πρόσβαση Φεβρουαρίου 27, 2026, [https://ncvs.org/archive/products\_books.html](https://ncvs.org/archive/products_books.html)  
15. Characteristics of phonation onset in a two-layer vocal fold model \- PMC, πρόσβαση Φεβρουαρίου 27, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC2677361/](https://pmc.ncbi.nlm.nih.gov/articles/PMC2677361/)  
16. Suitability of dysphonia measurements for telemonitoring of Parkinson's disease \- PMC, πρόσβαση Φεβρουαρίου 27, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC3051371/](https://pmc.ncbi.nlm.nih.gov/articles/PMC3051371/)  
17. Comparison of parametric representations for monosyllabic word recognition in continuously spoken sentences \- ScienceOpen, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.scienceopen.com/document?vid=475b4ae7-df7c-4ead-8e68-e4a307cd7a40](https://www.scienceopen.com/document?vid=475b4ae7-df7c-4ead-8e68-e4a307cd7a40)  
18. Automatic Speaker Recognition Using Mel-Frequency Cepstral Coefficients Through Machine Learning \- Tech Science Press, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.techscience.com/cmc/v71n3/46499/html](https://www.techscience.com/cmc/v71n3/46499/html)  
19. Exploring the Articulatory Perspective of Mel-Frequency Cepstral Coefficients: Unravelling the Link between MFCCs and Vocal Tract Features \- ResearchGate, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.researchgate.net/publication/372240974\_Exploring\_the\_Articulatory\_Perspective\_of\_Mel-Frequency\_Cepstral\_Coefficients\_Unravelling\_the\_Link\_between\_MFCCs\_and\_Vocal\_Tract\_Features](https://www.researchgate.net/publication/372240974_Exploring_the_Articulatory_Perspective_of_Mel-Frequency_Cepstral_Coefficients_Unravelling_the_Link_between_MFCCs_and_Vocal_Tract_Features)  
20. XGBoost: A Scalable Tree Boosting System, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.kdd.org/kdd2016/papers/files/rfp0697-chenAemb.pdf](https://www.kdd.org/kdd2016/papers/files/rfp0697-chenAemb.pdf)  
21. Don't dismiss logistic regression: the case for sensible extraction of interactions in the era of machine learning \- PMC, πρόσβαση Φεβρουαρίου 27, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC7325087/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7325087/)  
22. Logistic regression in data analysis: An overview \- ResearchGate, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.researchgate.net/publication/227441142\_Logistic\_regression\_in\_data\_analysis\_An\_overview](https://www.researchgate.net/publication/227441142_Logistic_regression_in_data_analysis_An_overview)  
23. Cox, D.R. (1958) The Regression Analysis of Binary Sequences. Journal of the Royal Statistical Society. Series B, 20, 215-242. \- References \- Scientific Research Publishing, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.scirp.org/reference/referencespapers?referenceid=2361262](https://www.scirp.org/reference/referencespapers?referenceid=2361262)  
24. Regression Analysis of Binary Sequences | Journal of the Royal Statistical Society Series B \- Oxford Academic, πρόσβαση Φεβρουαρίου 27, 2026, [https://academic.oup.com/jrsssb/article/21/1/238/7035243](https://academic.oup.com/jrsssb/article/21/1/238/7035243)  
25. Regression Analysis of Binary Sequences | Journal of the Royal Statistical Society Series B \- Oxford Academic, πρόσβαση Φεβρουαρίου 27, 2026, [https://academic.oup.com/jrsssb/article/20/2/215/7027376](https://academic.oup.com/jrsssb/article/20/2/215/7027376)  
26. Logistic Regression for Machine Learning \- MachineLearningMastery.com, πρόσβαση Φεβρουαρίου 27, 2026, [https://machinelearningmastery.com/logistic-regression-for-machine-learning/](https://machinelearningmastery.com/logistic-regression-for-machine-learning/)  
27. Logistic Regression and Text Classification \- Stanford University, πρόσβαση Φεβρουαρίου 27, 2026, [https://web.stanford.edu/\~jurafsky/slp3/4.pdf](https://web.stanford.edu/~jurafsky/slp3/4.pdf)  
28. 7 Logistic Regression – Interpretable Machine Learning, πρόσβαση Φεβρουαρίου 27, 2026, [https://christophm.github.io/interpretable-ml-book/logistic.html](https://christophm.github.io/interpretable-ml-book/logistic.html)  
29. Enhancing Logistic Regression Using Neural Networks for Classification in Actuarial Learning \- MDPI, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.mdpi.com/1999-4893/16/2/99](https://www.mdpi.com/1999-4893/16/2/99)  
30. C. Cortes and V. Vapnik, “Support-vector networks,” *Machine learning,* vol. 20, no. 3, pp. 273-297, 1995\. \- Science and Education Publishing, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.sciepub.com/reference/429359](https://www.sciepub.com/reference/429359)  
31. support-vector networks, πρόσβαση Φεβρουαρίου 27, 2026, [https://web.engr.oregonstate.edu/\~huanlian/teaching/ML/2019spring/extra/svn-1995.pdf](https://web.engr.oregonstate.edu/~huanlian/teaching/ML/2019spring/extra/svn-1995.pdf)  
32. Support-Vector Networks \- Google Research, πρόσβαση Φεβρουαρίου 27, 2026, [https://research.google/pubs/support-vector-networks/](https://research.google/pubs/support-vector-networks/)  
33. Pattern Recognition and Machine Learning \- Microsoft, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf](https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf)  
34. Cortes, C. and Vapnik, V. (1995) Support-Vector Networks. Machine Learning, 20, 273-297. \- References \- Scientific Research Publishing, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.scirp.org/reference/referencespapers?referenceid=1150668](https://www.scirp.org/reference/referencespapers?referenceid=1150668)  
35. Random Forests \- BibBase, πρόσβαση Φεβρουαρίου 27, 2026, [https://bibbase.org/network/publication/breiman-randomforests](https://bibbase.org/network/publication/breiman-randomforests)  
36. (PDF) Random Forests \- ResearchGate, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.researchgate.net/publication/236952762\_Random\_Forests](https://www.researchgate.net/publication/236952762_Random_Forests)  
37. Random Forests | BibSonomy, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.bibsonomy.org/bibtex/14450d2e56555e7cb8f3817578e1dd4da/kdepublication](https://www.bibsonomy.org/bibtex/14450d2e56555e7cb8f3817578e1dd4da/kdepublication)  
38. Enhanced diagnostic interpretation of the MoCA using machine learning \- Frontiers, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2026.1679649/full](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2026.1679649/full)  
39. Greedy function approximation: A gradient boosting machine. \- Project Euclid, πρόσβαση Φεβρουαρίου 27, 2026, [https://projecteuclid.org/journals/annals-of-statistics/volume-29/issue-5/Greedy-function-approximation-A-gradient-boosting-machine/10.1214/aos/1013203451.full](https://projecteuclid.org/journals/annals-of-statistics/volume-29/issue-5/Greedy-function-approximation-A-gradient-boosting-machine/10.1214/aos/1013203451.full)  
40. XGBoost Paper, πρόσβαση Φεβρουαρίου 27, 2026, [https://xgboosting.com/xgboost-paper/](https://xgboosting.com/xgboost-paper/)  
41. Greedy Function Approximation: A Gradient Boosting Machine \- CUHK CSE, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.cse.cuhk.edu.hk/irwin.king/\_media/presentations/2001\_greedy\_function\_approximation\_a\_gradient\_boosting\_machine.pdf](https://www.cse.cuhk.edu.hk/irwin.king/_media/presentations/2001_greedy_function_approximation_a_gradient_boosting_machine.pdf)  
42. Greedy function approximation: A gradient boosting machine. \- Project Euclid, πρόσβαση Φεβρουαρίου 27, 2026, [https://projecteuclid.org/journals/annals-of-statistics/volume-29/issue-5/Greedy-function-approximation-A-gradient-boostingmachine/10.1214/aos/1013203451.full?tab=ArticleFirstPage](https://projecteuclid.org/journals/annals-of-statistics/volume-29/issue-5/Greedy-function-approximation-A-gradient-boostingmachine/10.1214/aos/1013203451.full?tab=ArticleFirstPage)  
43. XGBoost: A Scalable Tree Boosting System \- BibBase, πρόσβαση Φεβρουαρίου 27, 2026, [https://bibbase.org/network/publication/chen-guestrin-xgboostascalabletreeboostingsystem-2016](https://bibbase.org/network/publication/chen-guestrin-xgboostascalabletreeboostingsystem-2016)  
44. Risk Stratification for In-Hospital Mortality in Alzheimer's Disease Using Interpretable Regression and Explainable AI \- MDPI, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.mdpi.com/2308-3417/11/2/23](https://www.mdpi.com/2308-3417/11/2/23)  
45. Machine learning-based early detection of Parkinson's disease using handwriting and vocal features \- ResearchGate, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.researchgate.net/publication/395552034\_Machine\_learning-based\_early\_detection\_of\_Parkinson's\_disease\_using\_handwriting\_and\_vocal\_features](https://www.researchgate.net/publication/395552034_Machine_learning-based_early_detection_of_Parkinson's_disease_using_handwriting_and_vocal_features)  
46. Exploring Machine Learning Models to Uncover Pathways in ALS Pathogenesis Using Immunohistochemical Features \- medRxiv, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.medrxiv.org/content/10.64898/2025.12.19.25342356v1.full.pdf](https://www.medrxiv.org/content/10.64898/2025.12.19.25342356v1.full.pdf)  
47. Full article: AI-Based Ocular Age Estimation from Combined OCT and OCTA Metrics: Decade-Stratified Normative Modelling in Healthy Eyes – a Pilot Study \- Taylor & Francis, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.tandfonline.com/doi/full/10.2147/OPTH.S542219](https://www.tandfonline.com/doi/full/10.2147/OPTH.S542219)  
48. On over-fitting in model selection and subsequent selection bias in performance evaluation, πρόσβαση Φεβρουαρίου 27, 2026, [https://research-portal.uea.ac.uk/en/publications/on-over-fitting-in-model-selection-and-subsequent-selection-bias-](https://research-portal.uea.ac.uk/en/publications/on-over-fitting-in-model-selection-and-subsequent-selection-bias-)  
49. On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation \- Journal of Machine Learning Research, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.jmlr.org/papers/volume11/cawley10a/cawley10a.pdf](https://www.jmlr.org/papers/volume11/cawley10a/cawley10a.pdf)  
50. Effect of TRIPOD+AI Guidelines on the Reporting Quality of Artificial Intelligence Prediction Models in Orthopaedic Surgery: An 18-Month Bibliometric Study \- PMC, πρόσβαση Φεβρουαρίου 27, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12627258/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12627258/)  
51. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods | The BMJ, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.bmj.com/content/385/bmj-2023-078378](https://www.bmj.com/content/385/bmj-2023-078378)  
52. PROBAST+AI: an updated quality, risk of bias, and applicability assessment tool for prediction models using regression or artificial intelligence methods | The BMJ, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.bmj.com/content/388/bmj-2024-082505](https://www.bmj.com/content/388/bmj-2024-082505)  
53. Enhancing Transparency and Reporting Standards in Diabetes Prediction Modeling: The Significance of the TRIPOD+AI 2024 Statement \- PMC, πρόσβαση Φεβρουαρίου 27, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11307208/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11307208/)  
54. Critical Appraisal Tools for Evaluating Artificial Intelligence in Clinical Studies: Scoping Review \- Journal of Medical Internet Research, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.jmir.org/2025/1/e77110](https://www.jmir.org/2025/1/e77110)  
55. Data pipeline quality: development and validation of a quality assessment tool for data-driven algorithms and artificial intelligence in healthcare \- PMC, πρόσβαση Φεβρουαρίου 27, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12878310/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12878310/)  
56. FUTURE-AI: international consensus guideline for trustworthy and deployable artificial intelligence in healthcare | The BMJ, πρόσβαση Φεβρουαρίου 27, 2026, [https://www.bmj.com/content/388/bmj-2024-081554](https://www.bmj.com/content/388/bmj-2024-081554)  
57. Personalized Text-to-Speech Solutions for Parkinson's Patients through Generative AI | Nilashi | Journal of Soft Computing and Decision Support Systems, πρόσβαση Φεβρουαρίου 27, 2026, [https://jscdss.com/index.php/files/article/view/282](https://jscdss.com/index.php/files/article/view/282)  
58. Principles of Voice Production \- Ingo R. Titze \- Google Books, πρόσβαση Φεβρουαρίου 27, 2026, [https://books.google.com/books/about/Principles\_of\_Voice\_Production.html?id=m48JAQAAMAAJ](https://books.google.com/books/about/Principles_of_Voice_Production.html?id=m48JAQAAMAAJ)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAYCAYAAAAcYhYyAAABJklEQVR4Xu2TvSvGURTHT94LA/JSUkoUVht6xGAwGeQvsBj9DcpClEQ2o8UkkX9AMZCyiVUpyiSJz+0c171H8nsWC5/61D3ne+7zu8/vReSfX6cOV/EEz3Ewj4uxjFe4hE84nsc/U4t3uGLrzjwuxgS+4ZQPijCJx3gt+iNhHSz7rwR28MY3y+US912vC/dwDdexIY9zQvgq+lRSjrBk62ncSrIvjIjej9mk12K9Rqt78AEr44RjXnRDb9Ibsl611R1Wt8cJxzbeu96w6KYqq1ut7osTjlPRG5gyILqpxuqPk7TFiYRw3Becc/16fMZmq8MJHrEiToi+ZBs4KnqFcCXPIY7ZegZ3PyPlFi9wUb5/dN14gJuib3F/lsKC6Cd/hk0u+2u8AzTTNCj4hUBgAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAYCAYAAAD6S912AAABCUlEQVR4XmNgGAWDHlgB8Ukg/g3E/4H4MhDvBuIjQPwMKgbDklA9RAGQISBNsugSQBAKxF+BmAldAhfgAuJvQHwcXQIKWID4HLogPuDOAHFdNZKYNBBXQNncQDwbSY4g6GSAGGgE5TMC8UwgzoarIBEcY0ANfBjWRlZELBBkgMTwZiQxkEFPkPgwwAbEkUAsgi6BDAIZIK4pQxJTB+IFSHwQiAXi6QwQtSpocihgMgNEkSWSGA8QCyPxkQFBA68B8QcGSNIgBuA1UJMBomATugQegNVAJwZIzrjAgIjR2wyY4YYNgNSqogtSAkAGqqELUgJABoJSAcXAF4jbGSAGzgDieFTpUUAJAADZAzcI5Ja52AAAAABJRU5ErkJggg==>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAYCAYAAAD6S912AAABL0lEQVR4XmNgGAWDHlgB8Ukg/g3E/4H4MhDvBuIjQPwMKgbDklA9RAGQISBNsugSQBAKxF+BmAldAhfgAuJvQHwcXQIKWID4HLogPuDOAHFdNZKYNBBXQNncQDwbSY4g6GSAGGgE5TMC8UwgzoarIBEcY0ANfBjWRlZELBBkgMTwZiQxkEFPkPggoAPEy4H4ChBPB2JeVGkECGSAuKYMSUwdiBcg8UFgPwMk2bAC8TogXogqjQCTGSAGWiKJ8QCxMBIflAreALEPlB/PANGDNRldA+IPDJCkQSyoBeLb6IIgoMkAsWkTugQewAHED4A4GVnQiQGSMy4wIGIUZOMCJDW4ACg95qMLkgvSGCDZEARAjqIIgCKtH4gdoBiUdMgGoDQHSpfIiX4HiopRQBEAACp/PSRfP4DNAAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAA2CAYAAAB6H8WdAAAG5klEQVR4Xu3de6hVRRTH8alQiuxtopVppUIWEmRUUHnQDHoIib3JjIz6p7cglRbRA7MoijLNHmhBD6zIoKQnSRaYEKZQVKRSWdE/QUH+EVLza8/mrrPOPvuec8/D7rnfDyzOzJp751oKdzF7z0wIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAID22xzjjtReHWNvM+adHuPbGNf4AQAAgKHk/hjbfLJDpsY4KMYfqT/ajNXzfqBgAwAA6FrBdkv6XFaVLVdWsA3ziUHmUJ8AAACoZyAF28IY/8QY7geSWTE+jPGoyd1r2h+bdhkVbNf6ZFLxiUFG/20AAAAN2eETDRoX4y+fdNamz5tibDL59aZdz5QYO2Os8wNJxbR/DH0rbn+a/HWm3Qo///bU1vxfpHazKNgAAEDDfvCJJmiV7WCfNI7ziTaqmPZi09afKTfZtFvh5382tTX/S2asGRRsAACgK7SJQAXMAj/QBRWfSGzBNsq020XzH5bamn+MGWsGBRsAAOiaB0JWxHR7E0DFJ6JzYzzicm/EmO1yA1U0v/Q3v971G+lyFGwAAOA/KqTaEWX2jfFZjPP9QIdVfCJ6OGRFlTUnFK+0qWAqiiftFzlF80vR/Lm5MZbHmODyFGwAAKBrZoTGig+tdPXncp8oUXF9FU2+uDwpxhqXG6h68y91uXp8wfae6wMAAIRVMfZP7UaKjNd9ooAe803yyRb4gqhMxbRVMO4K2fdvNfmxofpokYHy87+S8pp/UWrrBoe7XExLYzLRtIWCDQCANnnNJzrgTZ/oEL0oPz+1V9qBOio+UaC/lbUr02e+0nVUqC1qFLmBFmxlTglZYdUpW0Jj8/vCloINANDT9Et9v9TWC+B2h+LFpt2qFaatwsQWFq3Q/Zm/udztrt9u+pmyO8aJMS41Y/VUfMK52iec6TE2pnajK13tLthUJD0eY4QfaBPNvyGUz69DhJeE6n9PQsEGAOhpZb/UX3b9c1y/Gc+Zth4ltqtgkwddf3uMG1yunW5On/r/YQ+WLVPxCeP3ULsxoShOSF9/cowjU7tM2d+t164z1vaU+3wCAIBe4n+p54+jjg/VBdsBofp0/WZdYtraCdnOgk1HYVirQnaVU6fk76ztFeNrO1Ci4hMtyFe6ymglSn+38/wAAAAYfGzBdkaoLqT8CpvvXxWyK5VE82jlZ2bIrh46NeVE52rZE/xtwXZs6HscqFx+ifdDMU5L7XwePfY6IsaFIXtpPecLtrNCbSEqF4XaVSsbZY/iAAAA9hhb2KhgaaZg8wXPJynvd0T6k/ttweYLKz0eFJ/P6R5NFXN23BdsR4f63w8AADDo2MLGP6r0BZrv1yuKVrv+ja5fVrCpr/ezfF5U+OmwVT2KLCvYtHuy6PsHyhemxP87AADoCfqlpnsr83bObwZ4NX3enT5fTJ/vpk+thuU7JrXTNC/U8su8c+eF7B24nP05+VyiQuyd1LZ/rikhewya5w5Pbb38f0Go3XSgR7v84gYAAIOazvFaH7LjNY4x+V9i/B3j+dTfGeP70FeUqej6Ncbo1JefQ3asRn6VUr2VjutNWz9H4/nGgLdjbA6155CtS7lxqa9301TgXRGy+e6JsU/I5vop9J3sr+uQ3kptlNPuSh1SK3ok7ldHAQDAELLWJzro8xiX+SQKLY6xLWRF+dmhsTPlAABAj8qvH+qGeT4xyGlFc1nIjitpN93YoLn199PfUSEAAGAIyN+J66QPfKKHrPIJZ2GMT30yOSRkj6Dto+r8UbfoETmrkgAAAC1a5ROO3z3raVwbNPTen+hdxpzuKR1j+o3Qz9odsvcM1db7jyr81D7TfB0AAMCQ8YJPFJgb45tQfVCx18oVY7kDTVvHtHxn+ltNGwAAYEhQcaRjUL6KMb56qJB29pattLXDRNPWOXi6RSKna80AAABQQteC6fGkLao6Se/Nla3oAQAA9DR7rp2PMnpM2d/XtEvRz5nqEwAAAKg2I8Ywnyww2yec4TFG+qSzy/V1GO9HLgcAANDT7HEc2lSgAunWvuEak2Ns9Mk6RvmEszzGBJ80xofaGyq0urfD5QAAAHqaijMdcDs/9VeaMU9Hdsz0See2kB3psTT1dTWVNjXYmJbGpKxgK/JEjAU+CQAA0Mv0iFF05pkuti+7PuppnzCmx/gytcfGWGTGyjS7eWFTjMd8EgAAoJfNSZ9rQnb3p66qKqK7QBUVF7NiPBNqNytsCVnhdmeoXWFTcZebZNoAAAAooZsKnvLJAVIRtiHGCD/gLImxIvTe/awAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAuuJfN/mwCro4NiYAAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAYCAYAAAAcYhYyAAABEklEQVR4Xu2SsUtCURTGvxBMB8tBcRJEaGioSdp0qtHNqc2tNZydJBw1ov9EEAwChyA0cHARhHBpcBZqkKjvep50PD3hKbj5gx88vu/dw73vPmDPTinRH/pNR/SJzrxsTl9p1+tdlpdlq7RolR6rrANZcKKyc/pJEypbcETbJotAXh6b3DG0gaNMr012BdnFo8mjkKP+w2330GR3kCHuW2nC9NRka3mBDInbIigxyI30bKG4pQ0baoqQXdRtocjRCxtq7iFDLm2xCQP6BblmiztqjT7D519ZkoHswvcayQ1k+IRmdZGELHJ+QIY4370s/ffq4rlA31S2FQ+0gtXhGxGiU5qiTdMF5oD2IQPOTLdH8QtkQjKi8EXKiQAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAcAAAAXCAYAAADHhFVIAAAAa0lEQVR4XmNgGOQgEIifA3EAugQIxALxRSDWQJcgD6QA8T4oNkOWUAXidVD2CSBehiTHUA3E1kCsCMT/GSCmoAAWIL4LxIvQJUAgjAGiyxKIZYC4DlmyD4ivI7F1keTAnt7JAHGMH7LEMAEAhkkREHK1PNMAAAAASUVORK5CYII=>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAYCAYAAAAs7gcTAAAAoElEQVR4XmNgGAWDGiQA8XEgPg/Ei4HYHIhXAvEKIPZGKIMorAJiZiDmBOL/QHwOiIWB+CADxBA42ATEjFC2BgNEcS4DRCPIZHuoHAbIZIAoVkKXwAaWAfEtdEEYYAHiViAOAWI2IH4DxHOR5AOAOBHGcWKAWJsDxBlQdhtUThSIdwIxL5TPwMcA8QTI1yAJFyA+BsSrgbiRARIio4AyAAAvThsHOE7i1wAAAABJRU5ErkJggg==>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAsCAYAAADYUuRgAAAFgklEQVR4Xu3deeh0UxzH8WMnkbVkCdnLkqwRnkSWFCFLKfEHQiFLEbL+IdmyZPeULVGyZVdKCCEhuychWxRJSHw/zjnPnPnOnbn3N7+5s/R7v+rbvfd77m/MHE/Nt3PuORMCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsDAs5xMAAACYDitaXGKxs8sDAABgipwXKNgAAACmGgUbAADAlKNgAwAAmHIq2HbxSQAAAEwPFWy7+iQAAMCw7rN43uK3dPyzuxlDUMG2m08CALDQPOITE7CWT1TQF/dxPjkGN/tEH4eFzrNWZ6TjFek4TpPoo7YstvjX4i+Ll7ubAABYOG71iZYtY7GFxYcuf5HFIperspnFaj7Zom8sDvTJGvtbLO+TQ1jsEw2Nu48AAMA8vBDi6MRrIU7PvWVxscWyqX1ri9/T+d7pHt3/Sogblsr7Kfdmup6vh0J8fb1mqWnBJuf4RIs+C7HInItLfWJIz/hEBf3/+ccnw3j7CAAAzIMKMl8Y6fqrdP61xVFFm/xisW5x/aK7HhX/vuZSsPm/bdPpPtHAHz4xJBXQdQ4N1f2h3L4+CQAAps/joffLXNeassvnaxRtslfoPCv0ZNlQYb0QX6NfDOLby4JNr/uAxRsWV4c4KrdKapNni/PSO6H3PTR5P99bXGvxboif+ewQf7tyhxBHHrOtQixgT0zXeu5uT4urLD7NNw1wQYifQ+9l7RBHPgdpUrB9ZPGqxesWOxV59dFNxXU2bB8BAICWaLrzy3S+SYhTdccsba2eShN9cW9rsb1vGCFfHJQF21MWG1tcaXGKxeEWh6Q2UQE3KitY3JPOVaTdX7Rp76/timsVkWuGODIpx4dYxJ0Vej9PFU2t5lFPFW77dDf/zxdQdcWU8m+nc03f6vOI+ujBdA4AAKaYvsxP8snCDz6R6O8u88kR8wVI1ZTot+46G+VCCT+KeEtxvlHoHmGTA0Kn6F1S5Js+46ei7xOf7KPJCNvHxbn6NK+2VR+9VLQBAIAppS/wDX2y8LdPJPq73X2yQltTopm/J+s3cjTMdF85lanPrBG9bNXQPbInN1isbLFN6LzmlhZ3LL2jmlaNHmnxk8VdKXdCp7lSk4Itbzmi0TtNj2bqo0eL62yYPgIAAC1RMXCNTzr6gt7R5VTgVX3Rj5ovDsqC7fMQ30e+59x0zJqOUDVxaoirZvVc2o+uTbQRbum2dFRBlN/fdek4yOohPhu4X4jPnDVZSdqkYMv/ba0WLamPyuJz1h1scaFPFu4NcURRx3KUdBjn+wQAAJN0t8VjPjkhVSNs/XzgEy36LvSupB2X+fzg+Tj7aByaFMVaNCJNNmHOW9tk17trVtgCAKbGHqH/tOi4zaVgO9MnWnRa6H3ObRa00UfajPdOnxyTvDJ3kDzV3ITf2PgId+1HdQEAmKh1LDbwyQloUrBpVORpnxwDrehc3yenWJt99IRP9NH0vqby6ldt/PxeOteUsRbV6LlC/fu5McRVuJlGzbRwZPMQf9u1VBZsi0J8XlHynoNfpCMAAMDMaVqINb2vKe1bly1Kx4MsjrXYtNPUIz/HqQUypbJgezgdtcAkT5X+mo4AAAAzp2kh1uQ+LSTQNidauVpHe+Jl+q1U7ZmnPfL6Ld5Q4aWROO1Rp3N/X1mw5alUbTSdadNmAACAmTSoEPNbhJRxeXGfaJ+4POp1ctnQR7mh8Sj4RQeeplEBAABm0qCCrVR3n9/Wpc5KFrf7ZAu0n52ehQMAAJhZdYVYVnffXAs2AAAA1NDeZtr4V4XWz6F+U9+6gk2/U7vE4jmLo7ubAAAAMA7z2fQXAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGI3/AEORC+xnZtahAAAAAElFTkSuQmCC>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAiCAYAAADiWIUQAAAEXUlEQVR4Xu3cW8hlcxjH8SeDxrGJQiZMyumCZIiJkHBBRONwY0aU5MLUNLlRLpAy4xBJUQ6vHCKnyDiMU5qLqTFyIyYKSRLKKS5M4vn5/5f938+71vvuNXvt/e7N91O/1lrP2qu937Wm5un/X2uZAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQvevZzfNC3AEAAMbruVgYsZlYmEBdnZP9GtanwZ6eH/L6lZ5d8vpMXgIAgDF5IBbGZGMsTJAuz8mbDevTZLHny1Cb5OsHAMDUWOv5K9Te8Fwbag+H7XF51PNMLE6AO63bc/JfaNgujQVL1w8AAAxJU3plw3aRpXuRostiYUyu9uyIxQnwtXV7Tqa9YVvhOTOnpOtX9+8JAAC0oGbtIc9hnmPCvsrFniWhtsXzoedkz9Oe8/t3z6ntsXUN20GWfntTzu19tM9qS3+r6HPLPYvy+oWeBz3HWWoyzvH85DnLs4fnF88J/xyZPh/PyXw0cvmB52fP2Z4jPM/nfU0Nmxohbb/tecTzZLGvKzqXW3Pu8Nxv6e/tyuWxAAAA2lHjMeO5xPNU/65/rQvbL+fl0Z7rLTVdZ+SanhJUg9dkrmNFjUy0PRaGEBu7zbmupkzbWpaeLdY/8fyW178t6oPau1j/1FITVmlq2A7Ny6/yckO1w9J0dhc0qiqPe3b13GX9DdvrxfrOuCkWAADA4A601Agcb+nJvj+tN/pUUmNV5zrP4aG20nNAqNWpO1aqBqX0cSwMQU1ZE90rd1SolQ3bO9Y7/ruiLvtaarTqckrxucoTnmuK7aaGrVL3u0+MBXeazf7+Kq8Wn6vzTSxkV8RCSzfHAgAAGJxGVE4vtjVVpynA6DzPPsX2bZ7drfcqB43QXGWp8SsbHI2iXVBsS9Oxspf1jzpV1Eh25UfrvXZCo0iP5XX97lNtdmNUjQiK9r1YrJfnpK01YXtTw/oteflZXi7Ly1stNZBd0FTrDdb728t3qVVTpMOoexgBAADMQ+/5es/Sf9AaeammPHfk2luW7uMqlU+NahpT92Np+lKNzv65fojn7upDlr7jj2Jbmo6VZZ5txbbo/ic1WV3SSJJGyKp756rpUd3DV06Xis6PmrbvrX9E8Aub/SRtG2UjKE0Nm6YjP/K8ZunJ1GNzXY12PFc7S9+xynOf556ifrCl6e3y97Sl61c1yAAAYMReioUGJ1lq3CptR1d+D9u6n2rYEZ5hlCOGJY1KDXpO6sQp1aaGrYmaq3hv4Sist+GmNHX9AADAmGhkbD5Heu613s31Sz2v9HYP5PawrSdYF4puwJ/rhvtBzkmT2AS1bdjet/7RsFH51foflmhrIa8fAAD/S6N8ga3up9PrJcpXZQzTEI1LV+dE96TVrS8kvebkxlhsYRquHwAAaOFzS+8Bw+TQ9dA76gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADA/Q2Bi8v+yeS3HAAAAABJRU5ErkJggg==>

[image10]: <data:image/png;base64,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>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAXCAYAAAA7kX6CAAABBUlEQVR4Xu2SP0tCURjG35IIx7agP4KDYptTH0Bo8BvkGNJio4gI4a7gV3BUZ6VouyA0KIYOgqNLLYGLQ2M9733PpeceaHOzH/zg8Dzv/XuOyP6RgyP4AecwgK+wBhO/Y3FK8As+wzTlGbiCE3hJecgN/BZ7wmG8CjkT69/gEReBK8oceizFZu443LiwyKFHX2ymxeHChfqdf/EkNlPnsO3CDocea7GZKw4v4BbOOCR0m/SigV8oD2LluV+ABvyEpxwmYRYewDGscOmYwnu3zkfhMRy69bXYT2BSYvun+6tv0+VSj1UTPsJ3sadH3MIX1/VglbrwLvp9kSfU6TnlrkDdPzvlBwF9N0nC+zBzAAAAAElFTkSuQmCC>