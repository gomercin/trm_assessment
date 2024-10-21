# General

This repository contains code and tests for calculating option pricing using Black&Scholes model, and using historical VaR methodology to calculate VaR for a simple portfolio.

# Notes
The code is designed around the assessment, thus it is not a complete model.
There are some shortcuts taken, or potential parameters that are not included in the calculation
as the assessment is mainly for calculating for specific values.
Such shortcuts and assumptions are mentioned in the relevant parts of the code.
Also, in general using utility libraries such as logging, or argparse would be preferred, but 
they wouldn't bring much value for the current context, so they are deliberately excluded.

# Usage
## To run the code and display the results
```
python main.py <path to input excel file>
```

## To run the tests:
The E2E tests uses the input excel file as reference for calculated values. Thus, the path to the file
should be provided as an environment variable before running the tests.
```
export TEST_INPUT_FILE=<path to input excel file>
python -m unittest discover
```

Note that the results from the Excel formulas differ from the results from the Python scripts and online resources. This seems to happen due to how rounding is handled in different systems.
To reduce the impact, I limited the E2E data comparisons to 3 digits.
In the real environment, we would need to discuss these topics (quality of the reference data, comparison threshold, implementation details, etc) with domain experts and other stakeholders.