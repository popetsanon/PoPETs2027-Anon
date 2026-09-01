# Format Leakage

Anonymized version.

This project measures how much information is revealed by string formats. Two datasets are analyzed, but only one is included due to privacy concerns.

Download the FEC dataset from https://www.fec.gov/data/browse-data/?tab=bulk-data into the `Raw Data` folder.

## Data Flow

The public dataset (FEC) workflow is split across two notebooks:

1. `data_processing.ipynb`
	- Loads raw FEC contribution data from `Raw Data/itcont.txt`.
	- Selects the attributes under study: `NAME`, `CITY`, `ZIP_CODE`, `EMPLOYER`, and `OCCUPATION`.
	- Cleans names and derives `FIRST_NAME`, `LAST_NAME`, and `CLEAN_NAME`.
	- Builds a format-only dataset where characters are replaced by `x` while preserving simple structure such as spaces and string length.
	- Outputs processed CSVs for use by the leakage notebook.

2. `leakage_calc.ipynb`
	- Loads the processed plaintext, format, and format-count tables.
	- Computes min-entropy of the plaintext attributes.
	- Computes conditional min-entropy given the observed format.
    - Computes Shannon entropy of the format classes.

## Notes
- The format mapping functions are intentionally simple, so the analysis measures leakage from coarse structural patterns rather than exact character content.