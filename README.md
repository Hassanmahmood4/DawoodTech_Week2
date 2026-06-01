# Student Performance Data Analysis

**Week 2 Internship Task** — Data Analysis with Python

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?style=flat-square&logo=pandas)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=flat-square&logo=streamlit)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

---

## Overview

This project demonstrates a complete **real-world data analysis workflow** on a Student Performance dataset containing **1,000+ records** with 17 features including subject scores, attendance, study habits, and demographic information.

---

## Project Structure

```
DawoodTech_Week2/
│
├── data/
│   ├── student_performance.csv          ← Raw dataset
│   └── student_performance_clean.csv    ← Cleaned dataset
│
├── notebook/
│   └── analysis.ipynb                   ← Full Jupyter Notebook
│
├── visualizations/
│   ├── 01_bar_subject_avg.png
│   ├── 02_line_study_trend.png
│   ├── 03_pie_gender.png
│   ├── 04_hist_avg_score.png
│   ├── 05_heatmap_correlation.png
│   └── 06_box_grade_score.png
│
├── screenshots/                         ← Dashboard screenshots
│
├── app.py                               ← Streamlit Dashboard
├── analysis.py                          ← Standalone analysis script
├── requirements.txt
└── README.md
```

---

## Dataset Features

| Column | Description |
|--------|-------------|
| `student_id` | Unique student identifier |
| `age` | Student age (14–18) |
| `gender` | Male / Female |
| `grade` | School grade (9th–12th) |
| `school` | School name |
| `Math / Science / English / History / Art` | Subject scores (0–100) |
| `Study_Hours` | Study hours per day |
| `Attendance` | Attendance percentage |
| `Internet` | Internet access (Yes/No) |
| `Parent_Edu` | Parental education level |
| `Extracurricular` | Extracurricular activity (Yes/No) |
| `study_group` | Study group membership |

---

## Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/Hassanmahmood4/DawoodTech_Week2.git
cd DawoodTech_Week2

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run analysis script
python analysis.py

# 4. Launch Streamlit dashboard
streamlit run app.py
```

---

## What Was Done

### Part 2 – Data Cleaning
- Removed **30 duplicate records**
- Handled **missing values** using median/mean/mode imputation
- Renamed columns for clarity
- Fixed data types (student_id → str, age → int)
- Dropped the `name` column (not analytically useful)
- Created derived column: `Avg_Score`

### Part 3 – Data Analysis
- Total records, grade distribution
- Subject-wise averages, min, max
- Top and bottom performers
- Gender-wise, grade-wise, school-wise analysis
- Correlation analysis (Study Hours ↔ Avg Score)
- Parent education impact

### Part 4 – Visualizations
| # | Chart Type | Insight |
|---|------------|---------|
| 1 | Bar Chart | Average score per subject |
| 2 | Line Chart | Study hours vs average score trend |
| 3 | Pie Chart | Gender distribution |
| 4 | Histogram | Distribution of average scores |
| 5 | Heatmap | Correlation between all numeric metrics |
| 6 | Box Plot | Score spread across grades |

### Part 5 – Streamlit Dashboard
- Dataset preview with download button
- Statistical summary (3 tabs)
- 8+ interactive charts
- Sidebar filters: Gender, Grade, School, Internet, Attendance %, Study Hours
- Dynamic comparison chart (Bonus)
- KPI cards

---

## Key Insights

- **Art** has the highest average score; **History** the lowest
- Students studying **4–6 hours/day** perform best
- **Internet access** shows a modest positive effect on scores
- Higher **parent education** correlates with slightly better performance
- Score distribution is approximately **normal** (mean ≈ 68.9)

---

## Bonus Features Implemented

- [x] Dashboard filters (sidebar)
- [x] Export/download filtered CSV
- [x] Dynamic comparison charts
- [ ] Streamlit Cloud deployment (optional)
- [ ] Dark/light mode toggle

---

## Technologies Used

- **Python 3.10+**
- **Pandas** — Data manipulation
- **NumPy** — Numerical operations
- **Matplotlib** — Static charts
- **Seaborn** — Statistical visualizations
- **Streamlit** — Interactive dashboard
- **Jupyter Notebook** — Analysis notebook

---

## Author

Intern — Week 2 Data Analysis Task  
*Part of the Machine Learning & Data Science Internship Program*
