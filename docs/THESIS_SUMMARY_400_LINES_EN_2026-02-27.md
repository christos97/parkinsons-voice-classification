# Thesis Summary (Approx. 400 Lines, English)

Source basis: Chapters 01–09 in thesis/ and validated result notes in docs/.

001. Section: Chapter 1 — Introduction
002. This thesis studies binary voice-based classification between Parkinson’s Disease (PD) and Healthy Controls (HC).
003. The motivation is early, low-cost, non-invasive support for research screening pipelines.
004. Speech changes are treated as measurable biomarkers rather than clinical diagnoses.
005. The work explicitly avoids clinical decision claims and remains a research study.
006. A central concern is methodological rigor over headline performance numbers.
007. The thesis emphasizes reproducibility through fixed seeds and documented workflows.
008. The problem context includes hypokinetic dysarthria and reduced vocal control in PD.
009. Speech manifestations include monotony, hypophonia, and articulation variability.
010. The literature suggests voice changes may emerge before obvious motor symptoms.
011. This motivates computational analysis of acoustic patterns from recorded speech.
012. The study highlights practical feasibility using accessible recording environments.
013. Two data pipelines are intentionally separated to avoid methodological confusion.
014. Pipeline A starts from raw WAV audio and performs feature extraction.
015. Pipeline B starts from pre-extracted CSV features without raw signal processing.
016. The thesis states that machine-learning models consume feature tables, not WAV files directly.
017. A key risk addressed is subject leakage when multiple recordings exist per participant.
018. Another risk is class imbalance and its impact on model behavior.
019. Feature representation is treated as a first-order determinant of classification quality.
020. Validation strategy is identified as a major source of literature heterogeneity.
021. The introduction frames generalization gaps as a recurring problem in voice PD studies.
022. Research Question 1 asks how classical models perform on PD vs HC voice classification.
023. Research Question 2 asks whether extending features from 47 to 78 helps.
024. Research Question 3 asks whether class weighting improves outcomes under imbalance.
025. Research Question 4 compares outcomes across two datasets with different constraints.
026. Research Question 5 examines differences between ReadText and SpontaneousDialogue tasks.
027. The thesis contribution includes grouped subject-level validation for Dataset A.
028. Another contribution is controlled feature-set ablation under matched model conditions.
029. A further contribution is transparent reporting of mean ± std for all key metrics.
030. The work also includes feature-importance interpretation rather than score-only reporting.
031. A lightweight demonstration web app supports presentation and qualitative interpretation.
032. The demo app is clearly labeled as research-only and not for clinical use.
033. The architecture separates Flask routes from inference internals through an adapter layer.
034. Audio input is normalized before inference to maintain consistent feature extraction.
035. The scope is intentionally restricted to binary PD vs HC classification.
036. The thesis excludes disease staging, prognosis, and differential neurological diagnosis.
037. The model family is restricted to classical machine learning methods.
038. Deep learning models are explicitly out of scope in this thesis.
039. Interpretability and reproducibility are prioritized over chasing maximum benchmark scores.
040. All comparisons are framed conservatively as observed trends under fixed conditions.
041. Chapter organization moves from motivation and evidence to methods, results, and limits.
042. Section: Chapter 2 — Literature Review
043. The literature review establishes speech impairment as common in PD populations.
044. It distinguishes detection/screening objectives from progression monitoring objectives.
045. The review reports that most recent studies emphasize detection over longitudinal monitoring.
046. Sustained vowels are often useful for discrimination-focused tasks.
047. Connected speech tasks provide richer articulation and prosody dynamics.
048. The thesis uses both structured and spontaneous speech tasks to compare behavior.
049. Acoustic features are grouped into prosodic, perturbation, harmonic, and spectral families.
050. Pitch statistics summarize fundamental frequency behavior and vocal monotony.
051. Jitter and shimmer capture cycle-to-cycle instability in phonation.
052. HNR-related descriptors reflect harmonic versus noisy voice characteristics.
053. Formant features represent vocal-tract resonant structure and articulation cues.
054. MFCC and delta descriptors capture perceptual spectral envelope dynamics.
055. The review highlights the practical importance of dataset design and metadata quality.
056. Raw-audio datasets permit controlled extraction and reproducible feature engineering.
057. Pre-extracted datasets simplify modeling but hide extraction assumptions.
058. A key literature risk is random sample-level splitting with repeated-subject records.
059. Subject-independent validation is less common than expected in published studies.
060. External validation across datasets is still rare across the field.
061. This limits confidence in cross-context generalization claims.
062. The review positions SVM and Random Forest as common classical baselines.
063. Logistic Regression is treated as an interpretable linear reference model.
064. Gradient Boosting and XGBoost are included as strong non-linear tabular baselines.
065. Methodological quality is framed as equally important as raw metric values.
066. Reproducibility gaps in prior work include unclear feature parameters and split logic.
067. The thesis responds by fixing seeds and documenting extraction settings explicitly.
068. Interpretability gaps in the literature motivate feature-importance analysis.
069. Recent reviews report growing use of deep models but uneven validation rigor.
070. The thesis therefore contributes a careful classical baseline under transparent constraints.
071. The review stresses cautious wording when comparing studies with different protocols.
072. Direct score comparisons across heterogeneous datasets are treated as limited.
073. Validation heterogeneity is presented as a major reason for conflicting literature claims.
074. Class imbalance handling is reviewed as a common but inconsistently effective tactic.
075. The review also discusses speech-task choice as an experimental design variable.
076. Read text and spontaneous dialogue can emphasize different acoustic phenomena.
077. The chapter builds a rationale for task-specific rather than silently pooled analysis.
078. It justifies reporting uncertainty, not only mean performance, in medical ML contexts.
079. The review creates the methodological bridge to the thesis experimental design.
080. It identifies open gaps in grouped validation, controlled ablation, and transparent caveats.
081. These gaps become explicit design requirements in later chapters.
082. The chapter concludes that robust methodology is essential for credible voice PD findings.
083. Section: Chapter 3 — Data Description
084. The thesis uses two complementary datasets with distinct strengths and limitations.
085. Dataset A is MDVR-KCL with raw audio recordings and subject identifiers.
086. Dataset A includes two speech tasks: ReadText and SpontaneousDialogue.
087. ReadText includes 37 subjects in the analyzed split configuration.
088. SpontaneousDialogue includes 36 subjects due to one missing subject instance.
089. Class composition is mildly imbalanced in Dataset A across both tasks.
090. Dataset A recordings originate from smartphone-call-scenario collection settings.
091. Raw waveform availability allows fully controlled and documented extraction choices.
092. Dataset A supports grouped subject-level cross-validation to reduce leakage risk.
093. Dataset B is a pre-extracted PD speech feature table in CSV format.
094. Dataset B contains 756 rows with binary class labels.
095. Dataset B is strongly imbalanced with PD majority representation.
096. Dataset B does not provide subject IDs in the released table.
097. Without subject IDs, grouped subject-level CV cannot be applied directly.
098. Sample-level stratified CV is feasible but potentially optimistic for repeated subjects.
099. The thesis explicitly flags this as a critical interpretation caveat.
100. Dataset A and Dataset B are not treated as directly comparable in absolute terms.
101. The two datasets differ in validation feasibility, task type, and feature provenance.
102. Dataset A includes reading and spontaneous speech contexts.
103. Dataset B mainly reflects sustained-phonation style descriptors in tabular form.
104. Dataset A enables controlled ablations for extraction-driven feature sets.
105. Dataset B enables broad feature-space modeling under constrained metadata.
106. Comparative interpretation is trend-based and caveated rather than deterministic.
107. The thesis avoids merging Dataset A and Dataset B at subject level.
108. Each dataset is analyzed in its own methodological context.
109. This separation preserves internal validity and avoids invalid assumptions.
110. The chapter emphasizes unit-of-analysis clarity for each dataset.
111. In Dataset A, recordings are grouped by subject for validation.
112. In Dataset B, each row is treated as a sample under stratified CV.
113. The chapter documents these differences before presenting model outcomes.
114. This transparent setup reduces the risk of overclaiming cross-dataset conclusions.
115. Dataset descriptors include class proportions and available modality information.
116. The chapter explains why Dataset B may look numerically stronger but less reliable.
117. Dataset A is smaller and noisier yet methodologically stricter.
118. Dataset B is larger and more stable yet potentially optimistic due to unknown overlap.
119. The thesis treats this as an instructive contrast in ML evaluation realism.
120. Data constraints directly influence the design choices of Chapter 5.
121. All downstream results are interpreted through the data limitations established here.
122. The chapter closes by emphasizing cautious generalization outside the studied datasets.
123. This data framing underpins the validity caveats in Chapter 8.
124. Section: Chapter 4 — Methodology
125. The methodology transforms audio into structured feature vectors for classical ML.
126. For Dataset A, all recordings undergo consistent preprocessing before extraction.
127. Audio is resampled to 22.05 kHz to standardize processing.
128. Stereo content is converted to mono for consistent downstream representation.
129. Amplitude normalization is applied to control recording-level level differences.
130. Silence trimming is performed with a fixed energy-based thresholding strategy.
131. Prosodic extraction uses Praat/Parselmouth-based measurements.
132. Pitch features include mean, standard deviation, minimum, and maximum F0 statistics.
133. Jitter descriptors include local jitter, RAP, and PPQ5 variants.
134. Shimmer descriptors include local shimmer plus APQ and DDA family metrics.
135. Harmonicity descriptors include HNR-related statistics and autocorrelation cues.
136. Intensity descriptors summarize average level, variability, and dynamic range.
137. Formant descriptors capture mean and variability for F1–F3 components.
138. Spectral extraction uses librosa-driven cepstral and shape descriptors.
139. Baseline spectral set includes MFCC means and delta-MFCC means.
140. Extended set adds MFCC standard deviations to capture within-utterance variability.
141. Extended set also adds delta-delta MFCC means for second-order temporal dynamics.
142. Additional spectral-shape descriptors are included in the extended representation.
143. These include centroid, bandwidth, rolloff, flatness, and zero-crossing-related behavior.
144. Baseline total dimensionality is 47 features.
145. Extended total dimensionality is 78 features.
146. Feature extension is designed as a controlled ablation, not arbitrary feature inflation.
147. The aim is to test whether richer spectral-temporal information helps classification.
148. The model set is fixed: LR, SVM-RBF, RF, GB, XGBoost.
149. This fixed model family ensures comparability across tasks and conditions.
150. Random seed settings are fixed for reproducibility across repeated runs.
151. The extraction process is deterministic under defined preprocessing parameters.
152. Each audio file yields one feature vector for model consumption.
153. Pipeline outputs are saved as feature tables for subsequent training and evaluation.
154. Methodological transparency is prioritized over opaque optimization procedures.
155. The chapter includes mathematical definitions for key perturbation descriptors.
156. It also explains the practical interpretation of each feature family.
157. The design balances interpretability and representational richness.
158. No deep neural feature encoders are introduced in this thesis pipeline.
159. This keeps the study aligned with small-sample and explainability constraints.
160. The same extraction logic is applied consistently within each experimental condition.
161. Configuration options are centralized to reduce manual inconsistency risks.
162. Method choices are justified as suitable for reproducible, thesis-level experimentation.
163. The chapter prepares the formal experiment matrix implemented in Chapter 5.
164. It defines the operational foundation for all reported metrics in Chapter 6.
165. Section: Chapter 5 — Experimental Design
166. The chapter formalizes questions, factors, and controlled experiment conditions.
167. RQ1 evaluates baseline capability of classical models for PD vs HC classification.
168. RQ2 tests feature-set expansion from 47 to 78 under matched model settings.
169. RQ3 tests whether class weighting improves outcomes under class imbalance.
170. RQ4 examines differences between stricter and less strict validation contexts.
171. RQ5 compares ReadText and SpontaneousDialogue behavior in Dataset A.
172. Three primary factors are varied: features, weighting, and model family.
173. Feature factor has baseline and extended levels.
174. Weighting factor has unweighted and balanced settings.
175. Model factor includes five predefined classifiers.
176. This yields four condition families: C1, C2, C3, and C4.
177. C1 is baseline features without class weighting.
178. C2 is baseline features with class weighting.
179. C3 is extended features without class weighting.
180. C4 is extended features with class weighting.
181. Each condition is run with all five models.
182. Each dataset-task context uses 5-fold cross-validation.
183. Dataset A uses grouped stratified folds at subject level.
184. Dataset B uses stratified folds at sample level due to missing IDs.
185. Total runs equal 300 across datasets, conditions, models, and folds.
186. Evaluation metrics include Accuracy, Precision, Recall, F1, and ROC-AUC.
187. All results are reported as mean ± std across folds.
188. The chapter discourages single-point reporting for medical ML interpretation.
189. Comparisons are performed under identical classifier configurations.
190. This supports fair attribution of changes to controlled factors.
191. The design avoids silent pooling of speech tasks in Dataset A.
192. Task-level reporting is preserved to expose speech-context dependence.
193. Reproducibility is reinforced with fixed random-state control.
194. Results artifacts are organized by condition directories for traceability.
195. The chapter includes caveat markers for Dataset B optimism risk.
196. It explicitly ties protocol limitations to interpretation boundaries.
197. Class weighting is not presumed beneficial and is treated empirically.
198. Feature extension is not presumed beneficial and is tested by ablation.
199. The design favors transparent hypothesis testing over aggressive tuning.
200. Hyperparameter search is constrained to maintain fair, stable comparisons.
201. The protocol supports both numeric and qualitative feature-importance analyses.
202. The experiment matrix is broad enough to answer all stated RQs.
203. The chapter creates a clear bridge from methodology to quantitative outcomes.
204. It also defines the reproducible structure used for appendix-level reporting.
205. The section closes by reinforcing conservative interpretation requirements.
206. Section: Chapter 6 — Results
207. Results are reported by dataset, task, condition, model, and uncertainty.
208. In Dataset A, best SpontaneousDialogue ROC-AUC is 0.857 ± 0.171 with RF (C3).
209. In Dataset A ReadText, best ROC-AUC is 0.834 ± 0.153 with SVM-RBF (extended).
210. In Dataset B, best ROC-AUC is 0.952 ± 0.015 with XGBoost.
211. Dataset B shows higher means and lower variance than Dataset A.
212. The thesis cautions that Dataset B may be optimistic due to unknown subject overlap.
213. Feature extension provides notable gains in ReadText for most non-linear models.
214. For ReadText, RF improves by approximately +0.232 ROC-AUC from baseline to extended.
215. For ReadText, SVM improves by approximately +0.220 ROC-AUC with extension.
216. For ReadText, GB improves by approximately +0.224 ROC-AUC with extension.
217. For ReadText, XGBoost improves by approximately +0.166 ROC-AUC with extension.
218. For ReadText, LR shows slight decrease under extension in the reported setup.
219. For SpontaneousDialogue, extension effects are smaller and model dependent.
220. SpontaneousDialogue RF rises modestly under extension in unweighted condition.
221. SpontaneousDialogue XGBoost slightly decreases under extension in the reported matrix.
222. Class weighting does not show a stable directional benefit across settings.
223. In RF ReadText baseline, weighting helps relative to unweighted.
224. In RF extended settings, weighting may reduce ROC-AUC in some tasks.
225. Overall, weighting behavior is heterogeneous and task-specific.
226. Variance in Dataset A is materially larger than Dataset B across metrics.
227. High fold-to-fold std in Dataset A supports cautious interpretation language.
228. Accuracy, Precision, Recall, F1, and ROC-AUC are all provided comprehensively.
229. The chapter emphasizes that uncertainty overlap can weaken ranking claims.
230. Random Forest appears robust across many Dataset A configurations.
231. SVM-RBF can perform strongly when richer features are available.
232. Gradient Boosting benefits from extension particularly in ReadText.
233. Logistic Regression acts as a stable linear baseline with lower flexibility.
234. XGBoost dominates Dataset B in headline ROC-AUC under internal CV.
235. Confusion matrices are presented for the best model-task scenarios.
236. ROC curves visualize separability trends across datasets and tasks.
237. Appendices provide full condition-level result tables for transparency.
238. No metric is presented as standalone proof of clinical readiness.
239. Findings are described as observed outcomes under specific protocol constraints.
240. Main-text tables prioritize key comparisons and uncertainty-aware summaries.
241. Appendix content supports auditability and reproducibility of claims.
242. Result narratives avoid overgeneralized superiority statements.
243. The chapter concludes that protocol context is inseparable from score interpretation.
244. Performance appears feasible, but confidence varies strongly by dataset conditions.
245. These quantitative outcomes feed directly into discussion and limitation framing.
246. The chapter sets up a conservative synthesis rather than leaderboard-style claims.
247. Section: Chapter 7 — Discussion
248. The discussion interprets outcomes through feature choice, task type, and validation design.
249. Feature-set expansion appears most beneficial in the structured ReadText context.
250. SpontaneousDialogue retains strong baseline separability with smaller extension gains.
251. The contrast suggests task-dependent utility of additional spectral-temporal descriptors.
252. Class weighting lacks universal benefit and should not be assumed by default.
253. Weighting effects vary with model bias-variance behavior and task distribution.
254. Random Forest exhibits comparatively stable behavior in many Dataset A conditions.
255. SVM-RBF benefits strongly from richer representations in ReadText.
256. Observed differences are interpreted as trends when uncertainty ranges overlap.
257. The thesis intentionally avoids absolute superiority language.
258. Comparisons with prior literature are framed as partially compatible, not equivalent.
259. Protocol differences in splitting and dataset composition limit direct score matching.
260. Grouped validation in Dataset A strengthens internal credibility of reported trends.
261. Dataset B strengths are acknowledged with explicit optimism caveats.
262. Feature-importance analysis indicates task-specific acoustic emphasis patterns.
263. ReadText often highlights pitch-related and stability descriptors.
264. SpontaneousDialogue emphasizes MFCC and perturbation-related descriptors more strongly.
265. Some features recur across tasks, suggesting potential task-general PD signatures.
266. Other high-rank features are task-specific and context sensitive.
267. This supports analyzing tasks separately rather than silently merged.
268. The discussion emphasizes interpretability as a practical research value.
269. It positions transparent feature behavior as useful for future validation studies.
270. Methodological implications include preserving subject grouping where possible.
271. Another implication is mandatory uncertainty reporting for small medical datasets.
272. A third implication is explicit caveat reporting when metadata is incomplete.
273. The chapter links findings to literature concerns about leakage and heterogeneity.
274. It highlights that strong internal scores do not automatically imply external robustness.
275. The thesis contributes by combining careful protocol design with reproducible reporting.
276. Feature ablation is presented as a controlled mechanism for evidence generation.
277. The discussion notes that improvements can be conditional, not universal.
278. This nuance is critical for responsible biomedical ML communication.
279. The chapter refrains from causality claims not supported by the experiment design.
280. It distinguishes practical usefulness from clinical deployment readiness.
281. Results are interpreted as incremental evidence in a broader research continuum.
282. The narrative aligns with conservative scientific language requirements.
283. The chapter encourages replication with larger cohorts and external validation.
284. It also recommends richer metadata for fairer cross-study comparison.
285. Overall, discussion conclusions remain evidence-bounded and method-aware.
286. The chapter forms the transition to explicit threats-to-validity in Chapter 8.
287. Its central message is that rigor and caveats are as important as performance.
288. Section: Chapter 8 — Limitations
289. The thesis identifies data and protocol constraints that bound interpretation confidence.
290. Dataset A has small subject counts, increasing fold-to-fold variance.
291. Small folds can magnify instability in model ranking outcomes.
292. Dataset A class imbalance is moderate but still relevant for sensitivity patterns.
293. Dataset B lacks subject IDs, preventing grouped subject-level splitting.
294. This can introduce train-test contamination risk at participant level.
295. Dataset B class imbalance is strong and may affect calibration and threshold behavior.
296. Therefore Dataset B headline scores may be optimistic.
297. Cross-dataset score differences cannot be attributed to one factor only.
298. Task type, metadata quality, and validation structure all vary simultaneously.
299. The study uses internal 5-fold CV and no external test cohort.
300. External generalization across centers and devices remains unresolved.
301. Hyperparameter tuning is intentionally constrained for comparability and stability.
302. This may understate best-case performance but improves fairness across conditions.
303. Feature sets are predefined from literature and not exhaustively optimized.
304. Alternative feature transformations could change model behavior in future work.
305. Audio quality variability can still influence extracted descriptors.
306. Pipeline normalization reduces but does not eliminate all recording artifacts.
307. Label noise and cohort heterogeneity are possible in public biomedical datasets.
308. The thesis acknowledges these as common threats in voice-based health ML.
309. Internal validity is strengthened where subject IDs are available.
310. External validity remains limited by dataset scope and protocol context.
311. Construct validity is supported by clinically motivated acoustic descriptor families.
312. Conclusion validity is constrained by sample size and uncertainty overlap.
313. The limitations chapter explicitly pairs threats with mitigation actions.
314. Mitigations include grouped CV, fixed seeds, and standardized preprocessing.
315. Mitigations also include transparent uncertainty reporting and cautious wording.
316. No limitation is hidden; each is surfaced in interpretation sections.
317. The chapter stresses that results are research evidence, not diagnostic proof.
318. Caveats are integrated into conclusions rather than isolated as afterthoughts.
319. This improves credibility and aligns with responsible AI communication norms.
320. The work invites broader validation rather than overclaiming maturity.
321. Future studies should prioritize external cohorts with explicit subject identifiers.
322. Longitudinal data would support progression monitoring beyond binary detection.
323. Richer demographic metadata would support subgroup fairness checks.
324. Nested validation could assess tuning effects more rigorously with larger cohorts.
325. Prospective collection protocols could reduce hidden confounders.
326. The chapter closes by defining clear boundaries for claim strength.
327. These boundaries directly inform the final conclusions of Chapter 9.
328. Limitations are treated as design-informed context, not failures.
329. Section: Chapter 9 — Conclusion
330. The thesis demonstrates feasible PD vs HC voice classification using classical ML.
331. Its central contribution is methodological discipline under realistic dataset constraints.
332. Grouped subject-level CV is implemented where subject IDs permit leakage control.
333. Feature-set ablation provides controlled evidence on representation effects.
334. Reporting includes mean ± std across all core metrics.
335. ReadText benefits strongly from feature extension in several non-linear models.
336. SpontaneousDialogue achieves strong performance with more modest extension deltas.
337. Class weighting does not yield a universal gain across model-task conditions.
338. Dataset B appears numerically strong but requires optimism caveats.
339. The thesis answers all five research questions with evidence-bounded interpretations.
340. RQ1 is answered positively with viable classical model performance.
341. RQ2 is answered conditionally, with strongest gains in ReadText.
342. RQ3 is answered negatively for universal weighting benefit.
343. RQ4 is answered with protocol-sensitive differences and caution on Dataset B.
344. RQ5 is answered with task-dependent behavior across metrics and feature importance.
345. The work provides a reproducible baseline for future PD voice studies.
346. It also provides a transparent benchmark for comparing richer future methods.
347. Clinical deployment is explicitly outside the scope of this thesis.
348. The final claim is framed as research support, not diagnostic substitution.
349. Future work priorities include external validation across independent cohorts.
350. Another priority is longitudinal monitoring data for progression modeling.
351. Future datasets should include reliable subject IDs and richer metadata.
352. Expanded fairness and subgroup analyses are recommended where sample sizes allow.
353. Methodologically, nested validation can be revisited with larger data.
354. Feature refinement should continue with transparent ablation logic.
355. Cross-dataset transfer experiments can test robustness more directly.
356. Standardized reporting templates can improve field-wide comparability.
357. The thesis advocates conservative language for biomedical ML reporting.
358. This helps prevent overinterpretation of internal validation results.
359. Overall, the study contributes credible, reproducible, and cautious evidence.
360. It demonstrates that careful classical ML remains valuable in small-data settings.
361. It highlights that protocol quality and caveats are integral to scientific value.
362. The final takeaway is balanced optimism grounded in methodological realism.
363. Results suggest promise, while limitations define clear boundaries.
364. The thesis is positioned as a robust foundation for subsequent research expansion.
365. It supports incremental progress through transparent and replicable practices.
366. Its conclusions align with responsible AI principles in health-related applications.
367. The chapter closes with a research-first perspective on future validation.
368. The overall contribution is methodological rigor paired with interpretable outcomes.
369. This completes a coherent end-to-end study from data to cautious conclusions.
370. Synthesis: The thesis consistently prioritizes internal validity over peak score optimization.
371. Synthesis: Subject-aware validation is the strongest protection against identity leakage artifacts.
372. Synthesis: Feature engineering decisions materially affect model behavior across speech tasks.
373. Synthesis: Reporting uncertainty is necessary for responsible interpretation in small cohorts.
374. Synthesis: Dataset context determines how far score comparisons can be trusted.
375. Synthesis: Task-specific analysis reveals patterns that pooled analysis might hide.
376. Synthesis: Conservative language improves scientific reliability in biomedical ML reporting.
377. Synthesis: The study’s contribution is a reproducible and transparent classical ML baseline.
378. Synthesis: Dataset B findings are useful but should remain caveated due to metadata limits.
379. Synthesis: Dataset A findings are stricter but noisier because of smaller sample size.
380. Synthesis: Random Forest is comparatively robust under several controlled conditions.
381. Synthesis: SVM-RBF shows strong gains when richer features are provided.
382. Synthesis: Logistic Regression remains a useful interpretability-oriented baseline.
383. Synthesis: Gradient Boosting and XGBoost provide strong tabular non-linear comparisons.
384. Synthesis: Feature importance helps convert model outputs into interpretable acoustic narratives.
385. Synthesis: Cross-dataset differences cannot be explained by a single variable.
386. Synthesis: Reproducibility infrastructure is central to thesis credibility.
387. Synthesis: The results support research progression, not immediate clinical deployment.
388. Synthesis: Explicit caveats are a core deliverable, not a peripheral note.
389. Synthesis: Future validation breadth is the key requirement for stronger generalization claims.
390. Synthesis: The thesis consistently prioritizes internal validity over peak score optimization.
391. Synthesis: Subject-aware validation is the strongest protection against identity leakage artifacts.
392. Synthesis: Feature engineering decisions materially affect model behavior across speech tasks.
393. Synthesis: Reporting uncertainty is necessary for responsible interpretation in small cohorts.
394. Synthesis: Dataset context determines how far score comparisons can be trusted.
395. Synthesis: Task-specific analysis reveals patterns that pooled analysis might hide.
396. Synthesis: Conservative language improves scientific reliability in biomedical ML reporting.
397. Synthesis: The study’s contribution is a reproducible and transparent classical ML baseline.
398. Synthesis: Dataset B findings are useful but should remain caveated due to metadata limits.
399. Synthesis: Dataset A findings are stricter but noisier because of smaller sample size.
400. Synthesis: Random Forest is comparatively robust under several controlled conditions.

---
End of 400-line summary.