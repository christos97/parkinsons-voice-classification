# Chapter 2: Literature Review

## 2.1 Parkinson’s Disease and Speech Impairment

Parkinson’s disease (PD) is a progressive neurodegenerative disorder primarily known for its motor symptoms such as tremor, rigidity, and bradykinesia. In addition to these well-recognized motor features, PD almost invariably affects speech and voice as the disease progresses. In fact, studies report that approximately 70–90% of individuals with PD develop measurable speech and voice impairments. This collection of speech symptoms in PD is often referred to as hypokinetic dysarthria, indicating a characteristic pattern of speech motor control impairment associated with the disease.

The speech of a person with PD typically exhibits several hallmark changes. One prominent feature is hypophonia, or reduced voice loudness – patients often speak in a much softer voice than normal. Another is a monotonic pitch: PD speakers tend to have a limited range of pitch, resulting in speech that lacks the normal ups and downs of intonation (often described as "monopitch" speech). Monoloudness (little variation in volume) often accompanies this, so the overall prosody (melody and expressiveness of speech) is markedly diminished. Patients may also exhibit articulatory imprecision, where consonants in particular are not enunciated crisply. For example, consonant sounds may blur together or be undershot due to reduced range of motion in the articulators (jaw, tongue, lips). The voice quality in PD is frequently described as breathy or hoarse, reflecting incomplete vocal fold closure and other phonatory deficits. Additionally, some individuals speak with an improperly fast rate or with short rushes of speech, which, combined with the articulation issues, can reduce intelligibility. These speech characteristics—reduced loudness, monopitch, monoloudness, hoarse/breathy voice, and imprecise articulation—are widely observed in PD and form the basis of clinical descriptions of hypokinetic dysarthria.

Crucially, speech changes in PD are of interest not just as symptoms affecting communication, but also as potential non-invasive biomarkers of the disease. Voice is relatively easy to capture (e.g., via a short recording on a phone), and vocal changes can manifest early in the disease course. Some research suggests that subtle voice abnormalities may appear even before classic motor symptoms in some patients. Because voice recording and analysis can be done inexpensively and remotely, there is considerable motivation to use speech as a way to detect or monitor PD without the need for invasive tests. Speech and voice metrics are appealing for telemedicine and longitudinal tracking of PD progression. Unlike many clinical tests that require in-person visits and specialized equipment, voice recordings can be obtained by patients at home and sent to clinicians or analyzed by algorithms, enabling more frequent monitoring.

It should be noted, however, that the speech impairments in PD can vary greatly across patients and disease stages. Not every person with PD will have all the aforementioned speech symptoms, and the severity can range from very mild to highly debilitating. There is variability in how early voice changes emerge: some patients present with noticeable hypophonia and monotony in the early stages, whereas others might have minimal speech impact until later in the disease. Moreover, the progression of speech symptoms does not always strictly parallel the progression of other motor symptoms. For example, a patient with advanced limb tremor might still be understandable in speech, while another with relatively moderate overall motor signs could have severe dysarthria. In general, as PD progresses, speech tends to worsen – volume may further decrease and articulation may become more slurred. But importantly, these changes are not uniform or perfectly correlated with disease duration. Factors such as individual patient differences, co-occurring conditions (like age-related voice changes), and even treatment effects (medications or speech therapy) can influence the speech presentation. This variability means that while speech is a promising biomarker, one must be careful in using it for diagnosis or monitoring: any voice-based assessment needs to account for the wide range of "normal" for PD speech and the overlap with speech characteristics of other populations (e.g. normal aging can also cause some reduced loudness or hoarseness). In summary, PD provides a compelling case for voice analysis – it is a neurodegenerative disorder with clear motor effects on speech production, speech changes are prevalent and can be captured non-invasively, but these changes are heterogeneous across individuals and time. This establishes why voice is relevant for PD research while cautioning that clinical diagnostic use would require careful handling of variability and uncertainty, rather than treating voice patterns as a definitive signature of the disease.

## 2.2 Acoustic Characteristics of Parkinsonian Speech

A variety of acoustic features have been explored to characterize the distinctive patterns of Parkinsonian speech. The motivation for examining these features is that they quantify specific aspects of voice and speech that are affected by PD, thus providing measurable indicators that can be used in analysis or as inputs to classification models. Broadly, these features can be grouped into categories or feature families based on what aspect of speech they describe. In this section, we organize the discussion by three major families of acoustic features: prosodic features, perturbation measures, and spectral/cepstral features. This organization will correspond to the methodologies later employed in our study, where we leverage these feature types. Each subsection below defines the feature group, gives examples of specific features in that group, and explains what changes have been observed in PD speech relative to normal speech in that feature domain.

### 2.2.1 Prosodic Features

Prosodic features relate to the pitch (fundamental frequency) and loudness (intensity) patterns in speech, as well as timing/rhythm to some extent. The fundamental frequency of the voice (notated as F0) corresponds to the perceived pitch. Prosodic analysis often looks at statistics of F0, such as the mean pitch, range (difference between highest and lowest pitch), and the standard deviation of pitch across an utterance, to gauge how much variation in pitch a speaker uses. Loudness can be quantified through overall intensity level (in decibels) and its variability or emphasis patterns (e.g., how much a speaker modulates volume for stress). In typical expressive speech, healthy speakers vary both pitch and loudness to convey emphasis, emotion, or sentence modality (question vs. statement, etc.).

In Parkinson’s disease, a well-documented phenomenon is the reduction of prosodic variability. PD patients often speak in a monotone – their pitch remains relatively flat and at a narrow range, lacking the normal ups and downs. Objectively, one finds a lower standard deviation of F0 and a smaller pitch range in PD speech compared to healthy age-matched controls. This is sometimes described clinically as monopitch. Likewise, PD speakers exhibit monoloudness: their volume tends to be more constant and generally softer than normal. They may not employ the usual loudness increases to stress important words or to express emotion. The term hypophonia specifically refers to the reduced overall loudness (soft voice) that is common in PD. Together, monopitch and monoloudness make PD speech sound flat or expressionless. For instance, where a healthy speaker might vary pitch and loudness dynamically within a single sentence ("Really? I can’t believe it!"), a person with PD might deliver the same sentence in a relatively uniform tone and volume, which can be perceived as lacking affect.

Empirical studies support these observations. One study noted that most PD patients have significantly lower pitch variability and reduced intensity modulation, resulting in perceptually monotonic and weak speech. These prosodic deficits can be quantified: for example, computing the pitch range in a reading passage might show only a few semitones of variation for a PD speaker versus perhaps an octave for a healthy speaker. Similarly, intensity traces from PD speech often appear "flatter." Prosodic features like F0 range, F0 variability (e.g., variance or interquartile range of F0), intensity range, and intensity standard deviation are therefore commonly included in acoustic analyses. They capture the diminished expressivity in PD speech that comes from rigidity and bradykinesia affecting the vocal apparatus (including respiratory support and laryngeal control). In summary, prosodic measures in PD typically indicate reduced pitch and loudness variability, aligning with the clinical description of hypokinetic dysarthria where speech has a monotone, soft character. These features are important later when designing classifiers, because they directly reflect how PD impacts one’s control over voice dynamics.

### 2.2.2 Perturbation Measures

Perturbation measures are acoustic features that capture the cycle-to-cycle variations in the voice signal, reflecting stability (or instability) of vocal fold vibration. The two primary perturbation measures are jitter and shimmer. Jitter quantifies the minute fluctuations in pitch period from one glottal cycle to the next – essentially, variability in the fundamental frequency. Shimmer quantifies the variability in amplitude (loudness) across successive glottal cycles. In a perfectly steady, clear voice, one would expect nearly constant pitch period and amplitude for each cycle of vocal fold vibration (especially during sustained phonation of a vowel). However, human voices always have some natural jitter and shimmer. Pathologies that affect vocal fold control tend to increase these perturbations.

In Parkinson’s disease, due to factors like reduced vocal fold adduction, tremor, and inconsistent breath support, jitter and shimmer are often elevated compared to age-matched healthy controls. That is, PD voices typically show more frequent, irregular fluctuations in frequency and amplitude. This corresponds to the perceptual observation of a hoarse or unsteady voice quality. For example, when sustaining a vowel sound like "ah," a healthy voice might sound steady, whereas a PD voice might quaver slightly in pitch and/or volume. These micro-instabilities are precisely what jitter and shimmer measure. Harmonics-to-Noise Ratio (HNR) is another related metric, which compares the level of periodic (harmonic) energy in the voice to the level of aperiodic or noise energy. A high HNR means the voice signal is very harmonic (clean tone), whereas a low HNR indicates a noisier, breathier voice. PD voices tend to have lower HNR values, indicating a higher proportion of noise (breathiness, roughness) in the voice.

To put some numbers for illustration: a healthy sustained vowel might have a jitter on the order of 0.5% (very small period fluctuations) and shimmer around 3–4%, with an HNR of, say, 20 dB or more. In a PD voice, jitter might be several times higher (reports of jitter in PD can be, for instance, 1%–2% or more) and shimmer likewise elevated, while HNR might drop to, say, 10–15 dB. Many studies corroborate that PD causes increased frequency and amplitude perturbation in the voice and a corresponding increase in spectral noise. These measures provide objective evidence of the vocal instability and glottal insufficiency that are characteristic of Parkinsonian dysarthria (often described as a "breathy and hoarse" voice quality).

### 2.2.3 Spectral and Cepstral Features

The disease also manifests in spectral characteristics:

- **Altered formant frequencies** (F1, F2, F3)
- **Changes in Mel-Frequency Cepstral Coefficients (MFCCs)**
- **Modified spectral envelope** characteristics

## 2.3 Feature Extraction Approaches

### 2.3.1 Traditional Acoustic Features

Early studies relied on clinically-motivated features:

| Feature Category | Examples | Physiological Basis |
|-----------------|----------|---------------------|
| Fundamental Frequency | F0 mean, F0 std | Vocal fold tension |
| Perturbation | Jitter, Shimmer | Neuromuscular control |
| Noise | HNR, NHR | Incomplete glottal closure |
| Formants | F1, F2, F3 | Vocal tract configuration |

### 2.3.2 Spectral Features

Modern approaches incorporate signal processing features:

- **MFCCs** (Mel-Frequency Cepstral Coefficients) — compact spectral representation
- **Delta and Delta-Delta MFCCs** — temporal dynamics
- **Spectral shape features** — centroid, bandwidth, rolloff, flatness

### 2.3.3 Deep Learning Features

Recent work has explored end-to-end learning from spectrograms. However, these approaches require large datasets and lack interpretability—both significant limitations for clinical applications.

## 2.4 Machine Learning Approaches

### 2.4.1 Classical Methods

Classical ML remains dominant in clinical applications due to interpretability:

| Method | Strengths | Limitations |
|--------|-----------|-------------|
| Logistic Regression | Interpretable coefficients | Linear decision boundary |
| SVM | Effective in high dimensions | Kernel selection critical |
| Random Forest | Handles non-linearity, feature importance | Less interpretable than linear models |

### 2.4.2 Deep Learning

CNNs and RNNs have been applied to PD detection but face challenges:
- Require large labeled datasets
- Prone to overfitting on small samples
- Limited interpretability for clinical validation

## 2.5 Methodological Concerns in Literature

### 2.5.1 Data Leakage

Many published studies fail to account for subject identity when splitting data:

> "When multiple recordings exist per subject, random train/test splits can place recordings from the same subject in both sets, leading to optimistic performance estimates."

This thesis addresses this through **grouped stratified cross-validation**.

### 2.5.2 Class Imbalance

Imbalanced class distributions are common but often unaddressed:

- Simple accuracy can be misleading
- Class weighting or resampling strategies needed
- This thesis investigates `class_weight="balanced"` as a mitigation

### 2.5.3 Reproducibility

Many studies lack sufficient detail for reproduction:
- Feature extraction parameters unspecified
- Random seeds not fixed
- Cross-validation strategy unclear

## 2.6 Benchmark Datasets

### 2.6.1 UCI Parkinson's Dataset

The most widely used benchmark, containing 195 samples with pre-extracted features. Limitations include lack of subject identifiers and dated feature set.

### 2.6.2 MDVR-KCL Dataset

Mobile device recordings from King's College London, providing raw audio with subject identifiers. Used as Dataset A in this thesis.

### 2.6.3 PD Speech Features Dataset

Kaggle-hosted dataset with 752 pre-extracted features. Used as Dataset B for comparison.

## 2.7 Research Gap

While numerous studies report high classification accuracies, few address:

1. **Grouped cross-validation** for multi-recording datasets
2. **Controlled feature ablation** studies
3. **Systematic class weighting** analysis
4. **Transparent limitations** acknowledgment

This thesis aims to fill these gaps through rigorous experimental design prioritizing methodological validity over performance optimization.

## 2.8 Summary

The literature demonstrates that voice-based PD detection is feasible, with classical ML achieving competitive results. However, methodological rigor varies significantly across studies. This thesis adopts a conservative approach, prioritizing reproducibility and valid comparison over state-of-the-art claims.
