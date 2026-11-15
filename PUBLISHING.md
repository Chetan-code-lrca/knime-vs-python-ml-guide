# Working with the published repository

The public repository is available at:

https://github.com/Chetan-code-lrca/knime-vs-python-ml-guide

## Clone the project

```bash
git clone https://github.com/Chetan-code-lrca/knime-vs-python-ml-guide.git
cd knime-vs-python-ml-guide
```

## Contribute changes

1. Create a feature branch: `git switch -c docs/your-change`.
2. Make a focused change and run the relevant checks.
3. For Python changes, run `python -m pytest -q`.
4. Commit your work and push the branch.
5. Open a pull request describing what changed and how you tested it.

Do not commit virtual environments, cache folders, credentials, API keys, private datasets, or generated model binaries.

## Maintainer checklist for releases

- Verify the Python example and tests on a clean environment.
- Recreate the KNIME workflow using the stated KNIME version and extensions.
- Export a `.knwf` only after it has been opened and executed successfully.
- Add screenshots and record the exact KNIME version and extension versions.
- Check all external documentation links and update the learning roadmap.
