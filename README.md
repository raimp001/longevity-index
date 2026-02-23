# Longevity-Index

> Biological age computation and longitudinal tracking engine combining multi-omics, wearables, and clinical biomarkers to measure and reverse aging at the individual level.

## Vision

Chronological age is a poor proxy for how fast you are actually aging. Longevity-Index computes your **biological age** from dozens of validated biomarkers — then tracks how interventions (diet, exercise, supplements, therapeutics) change your trajectory. The goal: make aging measurable, reversible, and personal.

## Biological Age Clocks Supported

| Clock | Input Data | What It Measures |
|-------|-----------|------------------|
| Horvath v3 | DNA methylation | Epigenetic age |
| PhenoAge | 9 blood biomarkers | Phenotypic age |
| GrimAge | Plasma proteins | Mortality risk |
| DunedinPACE | DNA methylation | Aging pace/speed |
| VO2max Clock | Fitness data | Cardiorespiratory age |
| Composite Index | All above | Unified longevity score |

## Core Features

### 1. Multi-Omics Integration
- **Epigenomics:** DNA methylation array processing (Illumina 450K, EPIC)
- **Proteomics:** Plasma protein panel analysis (SomaScan, Olink)
- **Metabolomics:** Metabolite profiling and pathway analysis
- **Genomics:** Polygenic longevity risk scores

### 2. Clinical Biomarker Tracking
- 50+ standard lab biomarkers (HbA1c, lipids, CRP, IGF-1, etc.)
- Longitudinal trend analysis with statistical significance testing
- Reference range comparison against age/sex-matched populations
- Automated lab report parsing (PDF extraction)

### 3. Wearable Integration
- Apple Health, Garmin, Oura Ring, WHOOP data ingestion
- HRV, sleep quality, VO2max, resting heart rate tracking
- Continuous physiological age estimation

### 4. Intervention Tracking
- Log supplements, drugs, dietary changes, exercise protocols
- Attribution analysis: which interventions move your biomarkers?
- Personalized recommendations based on your biological age profile

### 5. Longevity Dashboard
- Interactive biological age timeline
- Biomarker radar charts and trend lines
- Peer comparison (anonymized population cohorts)
- Exportable health reports for physicians

## Why This Matters

Over **$4 billion** was invested in longevity biotech in 2024 alone. The missing piece is a unified measurement layer that tells individuals and researchers whether interventions actually work. Longevity-Index provides that measurement infrastructure.

## Roadmap

- [x] PhenoAge + GrimAge computation engine
- [x] Claude-powered biomarker interpretation
- [ ] Epigenetic clock pipeline (Horvath, DunedinPACE)
- [ ] Wearable API integrations (Apple Health, Oura)
- [ ] Longitudinal intervention attribution model
- [ ] Clinical report generator
- [ ] Population cohort comparison database

## Tech Stack

- **Backend:** Python, FastAPI, R (for epigenetic clocks)
- **ML:** scikit-learn, PyTorch, lifelines (survival analysis)
- **AI:** Anthropic Claude for report interpretation
- **Data:** PostgreSQL + TimescaleDB
- **Integrations:** Apple HealthKit, FHIR R4

## Getting Started

```bash
git clone https://github.com/raimp001/longevity-index
cd longevity-index
pip install -r requirements.txt
cp .env.example .env
python -m longevity_index.server
```

## License

MIT License
