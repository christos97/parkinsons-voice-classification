# Ταξινόμηση Νόσου Parkinson μέσω Φωνής με Χρήση Κλασικής Μηχανικής Μάθησης

*Voice-Based Classification of Parkinson's Disease Using Classical Machine Learning*

---

| | |
|---|---|
| **Ίδρυμα** | Εθνικό Μετσόβιο Πολυτεχνείο |
| **Σχολή** | Ηλεκτρολόγων Μηχανικών και Μηχανικών Υπολογιστών |
| **Τομέας** | Συστημάτων Μετάδοσης Πληροφορίας και Τεχνολογίας Υλικών |
| **Συγγραφέας** | Μάριος Χρήστος Συρμακέζης |
| **Επιβλέπων** | Γεώργιος Ματσόπουλος, Καθηγητής Ε.Μ.Π. |
| **Συνεπιβλέπουσα** | Δρ. Ουρανία Πετροπούλου, ΕΔΙΠ Ε.Μ.Π. |
| **Ημερομηνία** | Μάρτιος 2026 |

---

## Σκοπός

Αξιολόγηση και σύγκριση της απόδοσης κλασικών αλγορίθμων μηχανικής μάθησης στο πρόβλημα δυαδικής ταξινόμησης **Νόσος Parkinson (PD) έναντι Υγιών Ατόμων (HC)** με βάση χαρακτηριστικά φωνής. Εξετάζονται δύο προσεγγίσεις:

1. Εξαγωγή ακουστικών χαρακτηριστικών από ακατέργαστες ηχογραφήσεις (Dataset A — MDVR-KCL)
2. Χρήση προ-εξαγμένων χαρακτηριστικών (Dataset B — PD Speech Features)

---

## Δεδομένα

| Dataset | Τύπος | Τοπική διαδρομή |
|---------|-------|-----------------|
| **A: MDVR-KCL** ([Zenodo](https://zenodo.org/records/2867215)) | Raw WAV recordings | `assets/DATASET_MDVR_KCL/` |
| **B: PD Speech Features** ([Kaggle](https://www.kaggle.com/datasets/dipayanbiswas/parkinsons-disease-speech-signal-features)) | Pre-extracted CSV | `assets/PD_SPEECH_FEATURES.csv` |

---

## Μεθοδολογία

### Εγκατάσταση

```bash
make install        # Εγκατάσταση εξαρτήσεων μέσω Poetry
```

### Εκτέλεση πειραμάτων

```bash
make extract-all    # Εξαγωγή χαρακτηριστικών από το Dataset A
make experiments    # Εκτέλεση όλων των πειραμάτων ταξινόμησης
make results        # Εμφάνιση αποτελεσμάτων
```

### Demo εφαρμογή

```bash
make demo-install       # Εγκατάσταση Flask
make train-demo-model   # Εκπαίδευση μοντέλου για inference
make demo               # Εκκίνηση εφαρμογής → http://127.0.0.1:5000
```

### Μεταγλώττιση διπλωματικής

```bash
make thesis         # Δημιουργία PDF μέσω latexmk
make thesis-watch   # Συνεχής αναμεταγλώττιση κατά αλλαγές
```

---

## Δομή Αποθετηρίου

```text
parkinsons-voice-classification/
├── assets/                    # Σύνολα δεδομένων
│   ├── DATASET_MDVR_KCL/     # Ηχογραφήσεις WAV (Dataset A)
│   └── PD_SPEECH_FEATURES.csv # Προ-εξαγμένα χαρακτηριστικά (Dataset B)
├── demo_app/                  # Flask demo εφαρμογή
├── outputs/                   # Παραγόμενα αρχεία
│   ├── features/              # Εξαχθέντα χαρακτηριστικά (baseline / extended)
│   ├── models/                # Εκπαιδευμένα μοντέλα (.joblib)
│   ├── results/               # Αποτελέσματα πειραμάτων (CSV)
│   └── plots/                 # Γραφήματα
├── src/parkinsons_voice_classification/
│   ├── cli/                   # Εντολές CLI (pvc-*)
│   ├── data/                  # Φόρτωση δεδομένων
│   ├── features/              # Εξαγωγή χαρακτηριστικών
│   ├── models/                # Ταξινομητές & cross-validation
│   ├── visualization/         # Σχεδίαση γραφημάτων
│   ├── config.py              # Κεντρική διαμόρφωση
│   └── inference.py           # API πρόβλεψης
├── thesis/                    # Πηγαίος κώδικας LaTeX διπλωματικής
├── Makefile                   # Αυτοματοποίηση εργασιών
└── pyproject.toml             # Εξαρτήσεις Poetry
```

---

## Βασικές Εντολές

| Κατηγορία | Εντολή | Περιγραφή |
|-----------|--------|-----------|
| **Εγκατάσταση** | `make install` | Εξαρτήσεις μέσω Poetry |
| **Εξαγωγή** | `make extract-all` | Όλα τα tasks |
| | `make extract-readtext` | Μόνο ReadText |
| | `make extract-spontaneous` | Μόνο SpontaneousDialogue |
| **Πειράματα** | `make experiments` | Εκτέλεση όλων |
| | `make results` | Εμφάνιση αποτελεσμάτων |
| **Demo** | `make demo` | Εκκίνηση Flask app |
| **Διπλωματική** | `make thesis` | Μεταγλώττιση PDF |
| | `make thesis-clean` | Καθαρισμός artifacts |
| **QA** | `make test` | Εκτέλεση δοκιμών |
| | `make lint` | Έλεγχος κώδικα (ruff) |

### CLI εντολές

| Εντολή | Σκοπός |
|--------|--------|
| `pvc-extract` | Εξαγωγή ακουστικών χαρακτηριστικών |
| `pvc-experiment` | Εκτέλεση πειραμάτων ταξινόμησης |
| `pvc-train` | Εκπαίδευση μοντέλου για inference |
| `pvc-importance` | Ανάλυση σημαντικότητας χαρακτηριστικών |

---

## Αποποίηση Ευθυνών

> **Μόνο για ερευνητικούς και ακαδημαϊκούς σκοπούς.**
> Η demo εφαρμογή προορίζεται αποκλειστικά για παρουσίαση της διπλωματικής εργασίας.
> Δεν αποτελεί διαγνωστικό εργαλείο και δεν έχει κλινική εγκυρότητα.

---

## Απαιτήσεις

- Python 3.10+
- [Poetry](https://python-poetry.org/)
- LaTeX (για μεταγλώττιση διπλωματικής)

## Άδεια Χρήσης

MIT License
