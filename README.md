# AFM Force–Distance Curve Analysis (PyQt5 + Data Processing Pipeline)

This project is a Python application designed to automate the processing of atomic force microscopy (AFM) force–distance (F–D) curves.  
It combines an interactive graphical interface (PyQt5) with a computational pipeline based on NumPy, SciPy, Pandas, Matplotlib and scikit-learn to transform raw measurements into physically interpretable quantities.

---

## Motivation

Analyzing AFM force–distance curves often requires manual preprocessing (offset correction, calibration, contact-point detection, alignment to a reference curve) and model fitting.  
This tool streamlines the entire workflow so that users can go from raw AFM `.txt`/`.csv` files to reproducible results (contact depth, adhesion forces, local slopes, apparent Young’s modulus) in a single, interactive environment.

The program was originally developed in the context of a bachelor thesis on contact mechanics models (Hertz, DMT, JKR) and their applicability when adhesion is present.

---

## Features

- Complete data pipeline:
  - Import of raw AFM curve files (TXT/CSV)
  - Calibration of piezo displacement and cantilever deflection
  - Offset/baseline correction and simple noise filtering
  - Automatic detection of the contact point and alignment against a sapphire reference curve
  - Segmentation of the approach curve (before/after maximum force)
  - Linear regressions for local slopes and R² values
  - Constrained non-linear fitting of the Hertz 3/2 law using SciPy’s `curve_fit`
- Graphical interface (PyQt5):
  - Parameter editor for piezo sensitivity, spring constant and calibration coefficient
  - File chooser for the sapphire reference curve
  - Interactive toolbar via Matplotlib’s FigureCanvas
- Automated extraction of key features:
  - Contact point and contact depth
  - Minimum adhesion force
  - Local slopes on relevant segments with R²
  - Apparent Young’s modulus (from the non-linear fit)
- Reproducibility:
  - Settings persisted between runs
  - Annotated plots with the extracted metrics
  - Results made comparable across curves

---

## Processing pipeline (step by step)

1. **File import and parsing**  
   Raw AFM data are read, columns are standardized, and units are made explicit.

2. **Calibration**  
   Piezo voltage is converted to displacement (µm) using the user-defined sensitivity.  
   Deflection voltage is converted to force (nN) using the cantilever spring constant.

3. **Preprocessing**  
   A baseline correction removes the initial offset.  
   Very low-force regions (e.g., < 0.05 nN) are filtered out to avoid spurious detections.  
   The contact point is estimated at the first significant deviation of force from zero.

4. **Reference alignment**  
   Each sample curve is horizontally shifted to match a sapphire (rigid) reference curve, reducing curve-to-curve variance and defining a common depth origin.

5. **Segmentation**  
   The approach branch is split around the maximum force; each segment is analyzed separately.

6. **Regression and fitting**  
   Local linear regressions provide slopes and goodness-of-fit (R²).  
   A constrained non-linear fit is applied to the Hertz model  
   `F = α · |x − h_f|^(3/2)`  
   to estimate an apparent modulus (model- and calibration-dependent).

7. **Results and visualization**  
   Matplotlib plots show raw data, regression lines, the non-linear fit, the adhesion point and contact depth.  
   Numerical metrics are displayed alongside the plot.

---

## Technical details

- Programming language: Python 3
- GUI: PyQt5 (windows, dialogs, parameter editor, Matplotlib canvas)
- Data and computation: NumPy, Pandas, SciPy (`curve_fit`), scikit-learn (`LinearRegression`)
- Visualization: Matplotlib

Where possible, computations are vectorized (NumPy/Pandas), enabling fast processing of thousands of points on a standard CPU. Fits are bounded for stability, and calibration parameters are editable in the GUI to assess their impact on the results.

---

## GUI actions

- **Settings** : edit piezo sensitivity, spring constant, calibration coefficient  
- **Change Saphir File** : select the sapphire reference curve  
- **Young modulus with pow function fit** : run the non-linear Hertz (3/2) fit  
- **Young modulus with linear fit** : run linear regressions on curve segments and extract features  

---

## Roadmap

- Batch mode (process an entire folder and export features to CSV/Parquet)  
- Export of numerical results (contact depth, adhesion force, slopes, R², α, apparent modulus)  
- Model comparison (Hertz vs DMT vs JKR) with residual analysis and model selection criteria (AIC/BIC)  

---

## Background

The tool was created during a bachelor thesis on AFM force–distance analysis and contact mechanics.  
During the development of the graphical interface, PyQt5 was learned via the tutorials at:  
[pythonguis.com/tutorials](https://www.pythonguis.com/tutorials)


