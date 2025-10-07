import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from itertools import combinations
from collections import Counter

# Load the complete dataset
try:
    df = pd.read_csv('technical_skills_Job_roles_dataset.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: The file 'technical_skills_Job_roles_dataset.csv' was not found. Using a dummy dataset for demonstration.")
    df = pd.DataFrame({
        'Job_Role': ['Data Analyst', 'Business Analyst', 'Data Analyst', 'Software Engineer', 'Financial Analyst', 'Data Analyst', 'Business Analyst', 'Graphic Designer', 'Financial Analyst'],
        'Educational_Qualification': ['M.Sc in Data Science', 'B.Tech in Computer Science', 'M.Sc in Data Science', 'B.Tech in Computer Science', 'MBA in Finance', 'M.Sc in Data Science', 'B.Tech in Computer Science', 'B.Des in Graphic Design', 'MBA in Finance'],
        'Technical_Skills': ['SQL, Python, Tableau', 'SQL, Power BI, Excel', 'Python, R, Power BI', 'Java, Python, Git', 'Excel, Financial Modeling, Risk Management', 'SQL, Excel, Python', 'Communication, SQL, Excel', 'Photoshop, Illustrator', 'Auditing, Risk Management, Excel']
    })

# --- Data Preparation ---
# Clean and split skills, creating a list of lists
df['Skills_List'] = df['Technical_Skills'].astype(str).str.split(r',\s*')
df['Skills_Count'] = df['Skills_List'].str.len()

# --- Analysis 1: Skill Co-occurrence Heatmap ---
# Get the top 20 most common skills
all_skills = [skill for sublist in df['Skills_List'] for skill in sublist]
top_skills = [skill for skill, count in Counter(all_skills).most_common(20)]

# Create a co-occurrence matrix
co_occurrence_matrix = pd.DataFrame(0, index=top_skills, columns=top_skills)

# Populate the matrix
for skill_list in df['Skills_List']:
    # Filter the list to only include top skills to make the calculation faster
    present_top_skills = [skill for skill in skill_list if skill in top_skills]
    if len(present_top_skills) > 1:
        for skill1, skill2 in combinations(present_top_skills, 2):
            co_occurrence_matrix.loc[skill1, skill2] += 1
            co_occurrence_matrix.loc[skill2, skill1] += 1

# Mask the upper triangle for better readability
mask = np.triu(np.ones_like(co_occurrence_matrix, dtype=bool))
# Set diagonal to zero as we don't care about a skill co-occurring with itself
np.fill_diagonal(co_occurrence_matrix.values, 0)


plt.figure(figsize=(14, 12))
sns.heatmap(co_occurrence_matrix, mask=mask, cmap='viridis', annot=False)
plt.title('Heatmap of Co-occurrence of Top 20 Skills', size=16)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('skill_co_occurrence_heatmap.png')


# --- Analysis 2: Top Skill Combinations (Bigrams) ---
# Generate all pairs of co-occurring skills
skill_pairs = [pair for sublist in df['Skills_List'] if len(sublist) > 1 for pair in combinations(sorted(sublist), 2)]
pair_counts = Counter(skill_pairs)
top_20_bigrams = pair_counts.most_common(20)
bigram_df = pd.DataFrame(top_20_bigrams, columns=['pair', 'count'])
bigram_df['pair_str'] = bigram_df['pair'].apply(lambda x: f'{x[0]} & {x[1]}')

plt.figure(figsize=(12, 10))
sns.barplot(x='count', y='pair_str', data=bigram_df, palette='viridis')
plt.title('Top 20 Most Frequent Skill Combinations', size=16)
plt.xlabel('Frequency of Co-occurrence', size=12)
plt.ylabel('Skill Pair', size=12)
plt.tight_layout()
plt.savefig('top_skill_bigrams.png')


# --- Analysis 3: Histogram and Density of Skill Count ---
plt.figure(figsize=(12, 7))
sns.histplot(df['Skills_Count'], bins=15, kde=True, color='teal')
plt.title('Distribution of Number of Skills per Job Role', size=16)
plt.xlabel('Number of Skills', size=12)
plt.ylabel('Number of Job Roles', size=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('skill_count_histogram.png')


# --- Analysis 4: Job Role Diversity per Qualification ---
role_diversity = df.groupby('Educational_Qualification')['Job_Role'].nunique().sort_values(ascending=False).nlargest(15)

plt.figure(figsize=(12, 8))
sns.barplot(x=role_diversity.values, y=role_diversity.index, palette='plasma')
plt.title('Career Versatility: Job Role Diversity per Qualification (Top 15)', size=16)
plt.xlabel('Number of Unique Job Roles', size=12)
plt.ylabel('Educational Qualification', size=12)
plt.tight_layout()
plt.savefig('role_diversity_per_qualification.png')


# --- Analysis 5: Violin Plot of Skill Density for Top Job Roles ---
top_10_roles_list = df['Job_Role'].value_counts().nlargest(10).index
df_top_10_roles = df[df['Job_Role'].isin(top_10_roles_list)]

plt.figure(figsize=(16, 10))
sns.violinplot(y='Job_Role', x='Skills_Count', data=df_top_10_roles, order=top_10_roles_list, inner='quartile', palette='magma')
plt.title('Skill Count Density for Top 10 Job Roles', size=16)
plt.xlabel('Number of Skills', size=12)
plt.ylabel('Job Role', size=12)
plt.tight_layout()
plt.savefig('skill_density_violin_plot.png')

print("5 new EDA analyses have been generated and saved as PNG files.")