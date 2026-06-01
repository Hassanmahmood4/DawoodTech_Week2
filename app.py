"""
Week 2 Internship Task – Streamlit Dashboard
Student Performance Data Analysis
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import io

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .main { background: #ffffff; }

  .metric-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 5px solid #000000;
    margin-bottom: 1rem;
  }
  .metric-card h3 { margin: 0; color: #000000; font-size: 1.8rem; font-weight: 700; }
  .metric-card p  { margin: 0; color: #525252; font-size: 0.85rem; font-weight: 500; }

  .section-header {
    background: #000000;
    color: #ffffff;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    font-size: 1.05rem;
    font-weight: 600;
    margin: 1.2rem 0 0.8rem 0;
  }

  .stSelectbox label, .stMultiSelect label, .stSlider label { font-weight: 600; }

  div[data-testid="stSidebarContent"] { background: #000000; color: #ffffff; }
  div[data-testid="stSidebarContent"] * { color: #ffffff !important; }
  div[data-testid="stSidebarContent"] .stSelectbox > div > div {
    background: #171717; border-color: #ffffff;
  }
</style>
""", unsafe_allow_html=True)

# ── Load & Cache Data ──────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('data/student_performance.csv')

    # Clean
    df.drop_duplicates(inplace=True)

    score_cols = ['math_score', 'science_score', 'english_score', 'history_score', 'art_score']
    for col in score_cols:
        df[col].fillna(df[col].median(), inplace=True)
    df['study_hours_per_day'].fillna(df['study_hours_per_day'].mean(), inplace=True)
    df['attendance_percent'].fillna(df['attendance_percent'].mean(), inplace=True)
    df['parent_education'].fillna('Unknown', inplace=True)

    df.rename(columns={
        'math_score': 'Math', 'science_score': 'Science',
        'english_score': 'English', 'history_score': 'History',
        'art_score': 'Art', 'study_hours_per_day': 'Study_Hours',
        'attendance_percent': 'Attendance', 'parent_education': 'Parent_Edu',
        'internet_access': 'Internet', 'extracurricular': 'Extracurricular',
    }, inplace=True)

    df['student_id'] = df['student_id'].astype(str)
    SCORE_COLS = ['Math', 'Science', 'English', 'History', 'Art']
    df['Avg_Score'] = df[SCORE_COLS].mean(axis=1).round(2)
    df.drop(columns=['name'], inplace=True, errors='ignore')
    return df

df = load_data()
SCORE_COLS = ['Math', 'Science', 'English', 'History', 'Art']
PALETTE    = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']
BG         = '#f8f9fa'

# ── Sidebar Filters ────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Filters")
    st.markdown("---")

    gender_opt  = st.multiselect("Gender",  df['gender'].unique(), default=list(df['gender'].unique()))
    grade_opt   = st.multiselect("Grade",   sorted(df['grade'].unique()), default=list(df['grade'].unique()))
    school_opt  = st.multiselect("School",  df['school'].unique(), default=list(df['school'].unique()))
    internet_opt= st.multiselect("Internet Access", df['Internet'].unique(), default=list(df['Internet'].unique()))

    min_att, max_att = float(df['Attendance'].min()), float(df['Attendance'].max())
    att_range = st.slider("Attendance %", min_att, max_att, (min_att, max_att), step=0.5)

    min_hrs, max_hrs = float(df['Study_Hours'].min()), float(df['Study_Hours'].max())
    hrs_range = st.slider("Study Hours/Day", min_hrs, max_hrs, (min_hrs, max_hrs), step=0.1)

    st.markdown("---")
    st.markdown("**Quick Stats**")
    st.metric("Total Records", len(df))

# ── Apply Filters ──────────────────────────────────────────────
fdf = df[
    (df['gender'].isin(gender_opt)) &
    (df['grade'].isin(grade_opt)) &
    (df['school'].isin(school_opt)) &
    (df['Internet'].isin(internet_opt)) &
    (df['Attendance'].between(*att_range)) &
    (df['Study_Hours'].between(*hrs_range))
]

if fdf.empty:
    st.warning("No data matches your filters. Try adjusting the sidebar options.")
    st.stop()

# ── Header ─────────────────────────────────────────────────────
st.markdown("""
<div style="background:#000000;padding:2rem 2.5rem;border-radius:16px;margin-bottom:1.5rem;border:1px solid #000000">
  <h1 style="color:#ffffff;margin:0;font-size:2rem;font-weight:700">Student Performance Dashboard</h1>
  <p style="color:#d4d4d4;margin:0.3rem 0 0 0;font-size:1rem">Week 2 Internship Task · Data Analysis with Python</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

def kpi(col, title, val, accent='#000000'):
    col.markdown(f"""
    <div class="metric-card" style="border-left-color:{accent}">
      <h3 style="color:{accent}">{val}</h3>
      <p>{title}</p>
    </div>""", unsafe_allow_html=True)

kpi(k1, "Filtered Students", f"{len(fdf):,}", '#000000')
kpi(k2, "Mean Avg Score", f"{fdf['Avg_Score'].mean():.1f}", '#333333')
kpi(k3, "Top Score", f"{fdf['Avg_Score'].max():.1f}", '#555555')
kpi(k4, "Avg Attendance", f"{fdf['Attendance'].mean():.1f}%", '#777777')
kpi(k5, "Avg Study Hours", f"{fdf['Study_Hours'].mean():.1f}h", '#999999')

# ── Dataset Preview ────────────────────────────────────────────
st.markdown('<div class="section-header">Dataset Preview</div>', unsafe_allow_html=True)

with st.expander("Click to expand / collapse dataset", expanded=False):
    st.dataframe(fdf.reset_index(drop=True), use_container_width=True, height=320)
    buf = io.StringIO()
    fdf.to_csv(buf, index=False)
    st.download_button("Download Filtered CSV", buf.getvalue(),
                       "filtered_students.csv", "text/csv", use_container_width=True)

# ── Statistical Summary ────────────────────────────────────────
st.markdown('<div class="section-header">Statistical Summary</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Numeric Stats", "Category Breakdown", "Subject Deep Dive"])

with tab1:
    st.dataframe(fdf[SCORE_COLS + ['Avg_Score', 'Study_Hours', 'Attendance']].describe().round(2),
                 use_container_width=True)

with tab2:
    c1, c2, c3 = st.columns(3)
    c1.subheader("By Gender")
    c1.dataframe(fdf.groupby('gender')['Avg_Score'].agg(['mean','count','std']).round(2))
    c2.subheader("By Grade")
    c2.dataframe(fdf.groupby('grade')['Avg_Score'].agg(['mean','count','std']).round(2)
                   .sort_values('mean', ascending=False))
    c3.subheader("By School")
    c3.dataframe(fdf.groupby('school')['Avg_Score'].agg(['mean','count']).round(2)
                   .sort_values('mean', ascending=False))

with tab3:
    subj_stats = fdf[SCORE_COLS].agg(['mean','min','max','std']).T.round(2)
    subj_stats.columns = ['Mean', 'Min', 'Max', 'Std Dev']
    subj_stats['Rank'] = subj_stats['Mean'].rank(ascending=False).astype(int)
    st.dataframe(subj_stats.sort_values('Rank'), use_container_width=True)

# ── Interactive Charts ─────────────────────────────────────────
st.markdown('<div class="section-header">Interactive Charts</div>', unsafe_allow_html=True)

plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.spines.top': False,
                     'axes.spines.right': False, 'figure.facecolor': BG,
                     'axes.facecolor': BG, 'axes.grid': True, 'grid.alpha': 0.3})

# Row 1
col_a, col_b = st.columns(2)

with col_a:
    fig, ax = plt.subplots(figsize=(7, 4.2))
    avgs = fdf[SCORE_COLS].mean().sort_values(ascending=False)
    bars = ax.bar(avgs.index, avgs.values, color=PALETTE, edgecolor='white', width=0.55)
    for bar, val in zip(bars, avgs.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    ax.set_title('Average Score by Subject', fontsize=13, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.set_ylabel('Avg Score')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_b:
    fig, ax = plt.subplots(figsize=(7, 4.2))
    fdf_s = fdf.copy()
    fdf_s['Study_Bin'] = pd.cut(fdf_s['Study_Hours'], bins=7)
    trend = fdf_s.groupby('Study_Bin')['Avg_Score'].mean().dropna()
    ax.plot(range(len(trend)), trend.values, color='#2a9d8f', linewidth=2.5,
            marker='o', markersize=7, markerfacecolor='white', markeredgewidth=2)
    ax.fill_between(range(len(trend)), trend.values, alpha=0.12, color='#2a9d8f')
    ax.set_xticks(range(len(trend)))
    ax.set_xticklabels([str(b) for b in trend.index], rotation=25, ha='right', fontsize=8)
    ax.set_title('Study Hours → Average Score Trend', fontsize=13, fontweight='bold')
    ax.set_ylabel('Avg Score')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Row 2
col_c, col_d = st.columns(2)

with col_c:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.set_facecolor(BG); fig.patch.set_facecolor(BG)
    gender_counts = fdf['gender'].value_counts()
    wedges, texts, autotexts = ax.pie(
        gender_counts, labels=gender_counts.index,
        autopct='%1.1f%%', colors=['#2a9d8f', '#e76f51'],
        startangle=140, pctdistance=0.80,
        wedgeprops=dict(edgecolor='white', linewidth=2))
    for t in autotexts:
        t.set_fontsize(12); t.set_fontweight('bold')
    ax.set_title('Gender Distribution', fontsize=13, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_d:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(fdf['Avg_Score'], bins=22, color='#2a9d8f', edgecolor='white', alpha=0.85)
    ax.axvline(fdf['Avg_Score'].mean(), color='#e76f51', linewidth=2, linestyle='--',
               label=f"Mean: {fdf['Avg_Score'].mean():.1f}")
    ax.axvline(fdf['Avg_Score'].median(), color='#264653', linewidth=2, linestyle=':',
               label=f"Median: {fdf['Avg_Score'].median():.1f}")
    ax.legend(fontsize=10)
    ax.set_title('Average Score Distribution', fontsize=13, fontweight='bold')
    ax.set_xlabel('Avg Score'); ax.set_ylabel('Count')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Row 3 – Heatmap full width
st.markdown('<div class="section-header">Correlation Heatmap</div>', unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
num_cols = SCORE_COLS + ['Avg_Score', 'Study_Hours', 'Attendance']
corr_matrix = fdf[num_cols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='YlGnBu',
            linewidths=0.5, ax=ax, annot_kws={'size': 10},
            cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Between Student Metrics', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
st.pyplot(fig)
plt.close()

# Row 4 – Boxplot by grade
col_e, col_f = st.columns(2)

with col_e:
    st.markdown("**Score Distribution by Grade**")
    fig, ax = plt.subplots(figsize=(7, 4.2))
    grade_order = [g for g in ['9th','10th','11th','12th'] if g in fdf['grade'].unique()]
    sns.boxplot(data=fdf[fdf['grade'].isin(grade_order)], x='grade', y='Avg_Score',
                order=grade_order, palette=PALETTE, ax=ax, linewidth=1.4)
    ax.set_title('Avg Score by Grade', fontsize=13, fontweight='bold')
    ax.set_xlabel('Grade'); ax.set_ylabel('Avg Score')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col_f:
    st.markdown("**Parent Education vs Avg Score**")
    fig, ax = plt.subplots(figsize=(7, 4.2))
    pe_order = [p for p in ['None','High School','Bachelor','Master','Unknown'] if p in fdf['Parent_Edu'].unique()]
    pe_avg = fdf.groupby('Parent_Edu')['Avg_Score'].mean().reindex(pe_order).dropna()
    bars = ax.barh(pe_avg.index, pe_avg.values, color=PALETTE[:len(pe_avg)], edgecolor='white')
    for bar, val in zip(bars, pe_avg.values):
        ax.text(val + 0.2, bar.get_y() + bar.get_height()/2, f'{val:.1f}',
                va='center', fontsize=10, fontweight='bold')
    ax.set_title("Parent Education Impact", fontsize=13, fontweight='bold')
    ax.set_xlabel('Avg Score')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ── Comparison Chart (Bonus) ───────────────────────────────────
st.markdown('<div class="section-header">Dynamic Comparison Charts</div>', unsafe_allow_html=True)

cc1, cc2 = st.columns(2)
x_axis = cc1.selectbox("X-axis (Category)", ['grade', 'gender', 'school', 'Internet', 'Parent_Edu', 'Extracurricular', 'study_group'])
y_axis = cc2.selectbox("Y-axis (Score)", SCORE_COLS + ['Avg_Score', 'Study_Hours', 'Attendance'])

fig, ax = plt.subplots(figsize=(10, 4.5))
fig.patch.set_facecolor(BG)
comp = fdf.groupby(x_axis)[y_axis].mean().sort_values(ascending=False)
bars = ax.bar(comp.index, comp.values, color=PALETTE[:len(comp)], edgecolor='white', width=0.55)
for bar, val in zip(bars, comp.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{val:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
ax.set_title(f'{y_axis} by {x_axis}', fontsize=14, fontweight='bold')
ax.set_xlabel(x_axis); ax.set_ylabel(y_axis)
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ── Footer ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#737373;font-size:0.85rem;padding:1rem 0">
  Week 2 · Data Analysis Internship Task · Built with Python, Pandas, Seaborn & Streamlit
</div>
""", unsafe_allow_html=True)
