# Contributing

Thank you for helping make data science and ML workflows easier for beginners to understand.

## Good first contributions

- Fix a confusing explanation or typo.
- Add a small glossary entry with a clear example.
- Add a KNIME screenshot captured from a real workflow and the KNIME version used.
- Reproduce the shared case study in a different KNIME version and record the actual node settings.
- Add an equivalent Python implementation with tests.
- Add a use case showing when SQL, KNIME, Python, or a hybrid design is appropriate.

## Contribution guidelines

1. Keep explanations beginner-friendly without making them inaccurate.
2. Explain **what** a step does, **why** it is used, and **when** it is useful.
3. Do not claim that a node or library feature exists without checking its documentation or reproducing it.
4. Avoid screenshots of hypothetical or fabricated interfaces. State the software version for real screenshots.
5. Keep the shared dataset, target, split, and feature definitions unchanged unless a change is explained and tested.
6. Never commit secrets, access tokens, credentials, private datasets, or personally identifiable information.
7. Add or update tests when changing executable code.

## Local checks

```bash
python -m pip install -r requirements.txt
python data/generate_dataset.py
python python/train_model.py
pytest
```

## Pull requests

Keep pull requests focused. Include:
- What changed.
- Why the change helps a learner.
- How you tested it.
- Relevant software versions, especially for KNIME changes.
