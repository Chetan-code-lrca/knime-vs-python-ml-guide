# Roadmap

This project should grow as a practical learning resource. The first milestone focuses on a clear introduction and one reproducible regression case study.

## Milestone 1 — Beginner foundation

- [x] Explain KNIME, Python, libraries, and ML fundamentals separately.
- [x] Create a structured beginner learning path.
- [x] Explain when KNIME, Python, SQL, and hybrid workflows are useful.
- [x] Explain common preprocessing operations and data leakage.
- [x] Create a synthetic dataset with a shared chronological train/test split.
- [x] Implement and test the Python baseline.
- [x] Write a KNIME build-along with current node references.
- [ ] Recreate the KNIME workflow in a real installation and export the `.knwf` file.
- [ ] Add version-labelled screenshots from the verified KNIME workflow.

## Milestone 2 — More ML problem types

- [ ] Add a classification case study with precision, recall, F1, confusion matrix, and threshold selection.
- [ ] Add an unsupervised clustering case study and explain that clusters do not have ground-truth labels by default.
- [ ] Compare a linear model with a tree-based model on a suitable dataset.
- [ ] Add a time-series forecasting lesson that explains chronological validation.

## Milestone 3 — Engineering and deployment

- [ ] Add a model persistence and inference example in Python.
- [ ] Add a simple FastAPI endpoint and test it.
- [ ] Explain workflow automation and operational monitoring.
- [ ] Demonstrate a hybrid KNIME + Python workflow.
- [ ] Add a reproducibility checklist for dataset versions, dependencies, seeds, and model settings.

## Quality bar

Every new case study should state its problem, dataset source/license, target, valid features, split strategy, preprocessing, model settings, metrics, limitations, and reproducible instructions. Screenshots and serialized KNIME workflows must be produced from a real KNIME installation and tested before being marked complete.
