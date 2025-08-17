# AFM Force–Distance Curve Analysis (PyQt5 + Data Processing Pipeline)

This project is a Python application designed to automate the processing of atomic force microscopy (AFM) force–distance (F–D) curves.  
The software combines an interactive graphical interface (PyQt5) with a computational pipeline based on NumPy, SciPy and scikit-learn to transform raw measurements into physically interpretable quantities.

---

## Motivation
Analyzing AFM force–distance curves typically requires manual preprocessing (offset correction, calibration, detection of contact point, alignment to a reference curve) and curve fitting.  
This tool was created to streamline the entire workflow. It enables researchers and students to go from raw AFM text/csv files to reproducible results (contact depth, adhesion forces, slopes, apparent Young’s modulus) in a single, interactive environment.

The program was originally developed in the context of a bachelor thesis (carolina's one, not mine) focusing on contact mechanics models (Hertz, DMT, JKR) and their applicability in the presence of adhesion forces.

---

## Features
- Complete data pipeline:
  - Import of raw AFM curve files (txt/csv)
  - Calibration of piezo displacement and cantilever deflection
  - Offset correction and noise filtering
  - Detection of contact point and alignment against a sapphire reference curve
  - Segmentation of the curve into approach and retract branches
  - Linear regression for local slopes and R² values
  - Non-linear constrained fitting of the Hertz 3/2 law using SciPy’s `curve_fit`
- Graphical interface with PyQt5:
  - Parameter editor for sensitivity, spring constant and calibration coefficient
  - File chooser for the sapphire reference curve
  - Interactive toolbar based on Matplotlib’s FigureCanvas
- Automated extraction of key features:
  - Contact point and contact depth
  - Minimum adhesion force
  - Local slopes before and after maximum force
  - Apparent Young’s modulus (from non-linear fit)
- Persistence and reproducibility:
  - Settings stored between runs
  - Annotated plots with all extracted metrics
  - Results comparable across multiple curves

---

## Processing pipeline (step by step)
1. File import and column parsing  
   The program reads raw AFM data files, standardizes column names and units.

2. Calibration  
   Piezo voltage is converted into displacement (µm) using the sensitivity parameter.  
   Deflection voltage is converted into force (nN) using the cantilever spring constant.

3. Preprocessing  
   Baseline correction removes initial offsets.  
   Very low-force regions (<0.05 nN) are filtered out to avoid spurious detections.  
   The contact point is estimated where the force first deviates significantly from zero.

4. Reference alignment  
   Each curve is shifted horizontally to match a sapphire reference curve.  
   This reduces variance across measurements and provides a common depth origin.

5. Segmentation  
   The approach curve is split into two parts (before and after the maximum force).  
   Each branch is analyzed separately.

6. Regression and fitting  
   Local linear regressions yield slopes and R² values for curve segments.  
   A constrained non-linear fit is applied to the model  
   `F = α |x – h_f|^(3/2)` (Hertz law) to estimate the apparent modulus.

7. Results  
   Annotated Matplotlib plots display the contact depth, adhesion point, regression lines, and fitted curve.  
   Key metrics are printed alongside the plots.

---

## Technical details
- Programming language: Python 3
- GUI: PyQt5 (windows, dialogs, parameter editor, Matplotlib canvas integration)
- Data and computation: NumPy, Pandas, SciPy (curve_fit), scikit-learn (LinearRegression)
- Visualization: Matplotlib

The code is vectorized where possible, making the analysis of thousands of points very fast on a standard CPU. Fits are bounded to ensure stability, and calibration parameters can be modified interactively.

---

## Usage
Run the main script:

```bash
python FDC_fit2.py
