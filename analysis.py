"""
Week 2 Internship Task – Student Performance Data Analysis
Covers: Data Cleaning, Analysis, and Visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')
os.makedirs('visualizations', exist_ok=True)

# ─────────────────────────────────────────────────────────────
# PART 2 – DATA CLEANING
# ─────────────────────────────────────────────────────────────
print("=" * 60)
print("PART 2 – DATA CLEANING")
print("=" * 60)

df = pd.read_csv('data/student_performance.csv')

print(f"\n[Raw Dataset]")
print(f"  Shape          : {df.shape}")
print(f"  Duplicate rows : {df.duplicated().sum()}")
print(f"  Missing values :\n{df.isnull().sum()[df.isnull().sum() > 0]}")

# Step 1: Remove duplicates
df.drop_duplicates(inplace=True)
print(f"\n[After removing duplicates] Shape: {df.shape}")

# Step 2: Handle missing values
df['math_score'].fillna(df['math_score'].median(), inplace=True)
df['science_score'].fillna(df['science_score'].median(), inplace=True)
df['study_hours_per_day'].fillna(df['study_hours_per_day'].mean(), inplace=True)
df['attendance_percent'].fillna(df['attendance_percent'].mean(), inplace=True)
df['parent_education'].fillna('Unknown', inplace=True)
print(f"[After filling NaN]  Missing values left: {df.isnull().sum().sum()}")

# Step 3: Rename columns
df.rename(columns={
    'math_score'          : 'Math',
    'science_score'       : 'Science',
    'english_score'       : 'English',
    'history_score'       : 'History',
    'art_score'           : 'Art',
    'study_hours_per_day' : 'Study_Hours',
    'attendance_percent'  : 'Attendance',
    'parent_education'    : 'Parent_Edu',
    'internet_access'     : 'Internet',
    'extracurricular'     : 'Extracurricular',
}, inplace=True)

# Step 4: Data types
df['student_id'] = df['student_id'].astype(str)
df['age'] = df['age'].astype(int)

# Step 5: Derived column – average score
score_cols = ['Math', 'Science', 'English', 'History', 'Art']
df['Avg_Score'] = df[score_cols].mean(axis=1).round(2)

# Step 6: Drop unnecessary column
df.drop(columns=['name'], inplace=True)

print(f"\n[Clean Dataset Info]")
print(df.dtypes)
print(f"\nDataset shape after cleaning: {df.shape}")
df.to_csv('data/student_performance_clean.csv', index=False)
print("\nClean dataset saved → data/student_performance_clean.csv")

# ─────────────────────────────────────────────────────────────
# PART 3 – DATA ANALYSIS
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("PART 3 – DATA ANALYSIS")
print("=" * 60)

print(f"\nTotal students       : {len(df)}")
print(f"Grade distribution   :\n{df['grade'].value_counts().to_string()}")
print(f"\nOverall Statistics:")
print(df[score_cols + ['Avg_Score', 'Study_Hours', 'Attendance']].describe().round(2))

print("\n[Top & Bottom Performers]")
print(f"  Highest Avg Score : {df['Avg_Score'].max():.2f}  (Student ID: {df.loc[df['Avg_Score'].idxmax(), 'student_id']})")
print(f"  Lowest  Avg Score : {df['Avg_Score'].min():.2f}  (Student ID: {df.loc[df['Avg_Score'].idxmin(), 'student_id']})")
print(f"  Mean Avg Score    : {df['Avg_Score'].mean():.2f}")

print("\n[Subject-wise Average Scores]")
for s in score_cols:
    print(f"  {s:10s}: {df[s].mean():.2f}  |  Max: {df[s].max()}  |  Min: {df[s].min()}")

print("\n[Gender-wise Average Score]")
print(df.groupby('gender')['Avg_Score'].mean().round(2).to_string())

print("\n[Grade-wise Average Score]")
print(df.groupby('grade')['Avg_Score'].mean().round(2).sort_values(ascending=False).to_string())

print("\n[School-wise Average Score]")
print(df.groupby('school')['Avg_Score'].mean().round(2).sort_values(ascending=False).to_string())

print("\n[Correlation – Study Hours & Avg Score]")
corr = df['Study_Hours'].corr(df['Avg_Score'])
print(f"  Pearson r = {corr:.4f}")

print("\n[Internet Access Impact]")
print(df.groupby('Internet')['Avg_Score'].mean().round(2).to_string())

print("\n[Parent Education Impact]")
order = ['None', 'High School', 'Bachelor', 'Master', 'Unknown']
pe = df.groupby('Parent_Edu')['Avg_Score'].mean().round(2).reindex(order)
print(pe.to_string())

# ─────────────────────────────────────────────────────────────
# PART 4 – DATA VISUALIZATION (6 charts)
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("PART 4 – DATA VISUALIZATION")
print("=" * 60)

PALETTE = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']
BG      = '#f8f9fa'
ACCENT  = '#2a9d8f'

plt.rcParams.update({
    'font.family'     : 'DejaVu Sans',
    'axes.spines.top' : False,
    'axes.spines.right': False,
    'figure.facecolor': BG,
    'axes.facecolor'  : BG,
    'axes.grid'       : True,
    'grid.alpha'      : 0.3,
})

# ── Chart 1: Bar – Subject-wise Average Scores ──────────────
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor(BG)
avgs = df[score_cols].mean().sort_values(ascending=False)
bars = ax.bar(avgs.index, avgs.values, color=PALETTE, edgecolor='white', linewidth=0.8, width=0.55)
for bar, val in zip(bars, avgs.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.set_title('Average Score by Subject', fontsize=16, fontweight='bold', pad=15)
ax.set_ylabel('Average Score', fontsize=12)
ax.set_xlabel('Subject', fontsize=12)
ax.set_ylim(0, 105)
plt.tight_layout()
plt.savefig('visualizations/01_bar_subject_avg.png', dpi=140, bbox_inches='tight')
plt.close()
print("  ✔ Chart 1: Bar – Subject Averages")

# ── Chart 2: Line – Study Hours vs Avg Score (binned) ───────
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor(BG)
df['Study_Bin'] = pd.cut(df['Study_Hours'], bins=8)
trend = df.groupby('Study_Bin')['Avg_Score'].mean().dropna()
x_labels = [str(i) for i in trend.index]
ax.plot(range(len(trend)), trend.values, color=ACCENT, linewidth=2.5, marker='o',
        markersize=8, markerfacecolor='white', markeredgewidth=2.5)
ax.fill_between(range(len(trend)), trend.values, alpha=0.15, color=ACCENT)
ax.set_xticks(range(len(trend)))
ax.set_xticklabels(x_labels, rotation=25, ha='right', fontsize=9)
ax.set_title('Study Hours vs Average Score (Trend)', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Study Hours per Day (Bins)', fontsize=12)
ax.set_ylabel('Average Score', fontsize=12)
plt.tight_layout()
plt.savefig('visualizations/02_line_study_trend.png', dpi=140, bbox_inches='tight')
plt.close()
print("  ✔ Chart 2: Line – Study Hours Trend")

# ── Chart 3: Pie – Gender Distribution ──────────────────────
fig, ax = plt.subplots(figsize=(7, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
gender_counts = df['gender'].value_counts()
wedges, texts, autotexts = ax.pie(
    gender_counts, labels=gender_counts.index,
    autopct='%1.1f%%', colors=['#2a9d8f', '#e76f51'],
    startangle=140, pctdistance=0.80,
    wedgeprops=dict(edgecolor='white', linewidth=2))
for t in autotexts:
    t.set_fontsize(13); t.set_fontweight('bold')
ax.set_title('Student Gender Distribution', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('visualizations/03_pie_gender.png', dpi=140, bbox_inches='tight')
plt.close()
print("  ✔ Chart 3: Pie – Gender Distribution")

# ── Chart 4: Histogram – Avg Score Distribution ─────────────
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor(BG)
ax.hist(df['Avg_Score'], bins=25, color=ACCENT, edgecolor='white', linewidth=0.6, alpha=0.85)
ax.axvline(df['Avg_Score'].mean(), color='#e76f51', linewidth=2, linestyle='--',
           label=f"Mean: {df['Avg_Score'].mean():.1f}")
ax.axvline(df['Avg_Score'].median(), color='#264653', linewidth=2, linestyle=':',
           label=f"Median: {df['Avg_Score'].median():.1f}")
ax.legend(fontsize=11)
ax.set_title('Distribution of Average Scores', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Average Score', fontsize=12)
ax.set_ylabel('Number of Students', fontsize=12)
plt.tight_layout()
plt.savefig('visualizations/04_hist_avg_score.png', dpi=140, bbox_inches='tight')
plt.close()
print("  ✔ Chart 4: Histogram – Avg Score Distribution")

# ── Chart 5: Heatmap – Correlation Matrix ───────────────────
fig, ax = plt.subplots(figsize=(9, 7))
fig.patch.set_facecolor(BG)
num_cols = score_cols + ['Avg_Score', 'Study_Hours', 'Attendance']
corr_matrix = df[num_cols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='YlGnBu',
            linewidths=0.5, ax=ax, annot_kws={'size': 9},
            cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Heatmap – Student Metrics', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('visualizations/05_heatmap_correlation.png', dpi=140, bbox_inches='tight')
plt.close()
print("  ✔ Chart 5: Heatmap – Correlation Matrix")

# ── Chart 6: Box – Score by Grade ───────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor(BG)
grade_order = ['9th', '10th', '11th', '12th']
df_sorted = df[df['grade'].isin(grade_order)]
sns.boxplot(data=df_sorted, x='grade', y='Avg_Score', order=grade_order,
            palette=PALETTE, ax=ax, linewidth=1.4, flierprops={'marker': 'o', 'markersize': 4})
ax.set_title('Average Score Distribution by Grade', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Grade', fontsize=12)
ax.set_ylabel('Average Score', fontsize=12)
plt.tight_layout()
plt.savefig('visualizations/06_box_grade_score.png', dpi=140, bbox_inches='tight')
plt.close()
print("  ✔ Chart 6: Box – Grade vs Avg Score")

print("\nAll visualizations saved to /visualizations/")
print("\n✅ Analysis complete!")
