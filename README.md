# PNG Radiomics Workflow

Preprocessing, feature extraction, and exploratory analysis built **with** [PyRadiomics](https://github.com/AIM-Harvard/pyradiomics). This repository is an application workflow, not the upstream feature-extraction library.

## Setup

Use **Python 3.11** in an isolated environment. PyRadiomics 3.0.1 uses an older build helper that fails with Python 3.12's removed `SafeConfigParser` API.

```bash
git clone https://github.com/Shayne-Pro/Pyradiomics.git
cd Pyradiomics
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install 'numpy<2' 'setuptools<70' wheel
python -m pip install --no-build-isolation pyradiomics==3.0.1
python -m pip install pandas pillow SimpleITK openpyxl
```

A compiler is required when no PyRadiomics wheel matches the platform. The exploratory notebook additionally imports `jupyterlab`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn`, `kydavra`, and `joblib`; its dependency compatibility is separate from the extraction command.

## Extract a batch

Files share a case ID: `data/normal/images/case001_img.png` and `data/normal/masks/case001_mask.png`. Images are converted to 8-bit grayscale. Masks must be single-channel, match image dimensions, and contain the selected foreground value (default `255`). PNG inputs use unit pixel spacing; physical calibration from a medical volume is not preserved.

```bash
python 5.feature_extract.py --images data/normal/images --masks data/normal/masks --class-label 0 --output results/normal_features.xlsx
python 5.feature_extract.py --images data/abnormal/images --masks data/abnormal/masks --class-label 1 --output results/abnormal_features.csv
```

`--class-label` is the classification target for the entire batch (0=normal, 1=abnormal). `--mask-label` selects the ROI value inside a mask. Pairing is checked by case ID, so equal-length but mismatched lists fail before extraction. Existing output files are not overwritten.

Each output row contains `case_id`, `label`, and upstream diagnostics/features. Default output is `features.xlsx`; CSV is also supported. All options: `python 5.feature_extract.py --help`.

## Historical preprocessing and analysis

| File | Behavior |
| --- | --- |
| `Image Preprocessing/1.rename.py` | Prefix PNG filenames; edits files in place |
| `Image Preprocessing/2.copy_file.py` | Collect files with a chosen suffix |
| `Image Preprocessing/3.mask.py` | Historical LabelMe conversion experiment; review its JSON/folder pairing before use |
| `Image Preprocessing/4.convert2gray.py` | Convert PNG images to grayscale |
| `6.merge_xlsx.py` | Concatenate rows from `features_1.xlsx` and `features_2.xlsx` into `features_merged.xlsx` |
| `7.Feature Filtering and Analysis.ipynb` | Statistical filtering, Lasso, random forest, and plotting |
| `8.LinearRegression.py` | In-sample regression with six configured feature columns and a `score` target |

The historical preprocessing and regression scripts contain `Path/to/...` settings that must be edited. Work on copies for rename/conversion experiments. The merge script uses fixed filenames; configure those to match your workbooks.

The notebook predates the `case_id` column: select numeric feature columns and exclude IDs and diagnostics strings. Configure its CSV paths and create its `model/` directory. Fit feature selection and scaling within each training fold before claiming independent evaluation. Historical exploratory scores are not a new validated benchmark.

No patient data is supplied. [MIT](LICENSE) covers this repository's code; upstream dependencies and source datasets retain their own terms.

## Regression checks

```bash
python -m unittest discover -s tests -v
```
