import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Load the dataset
# Make sure the dataset file is in the same directory as your script
# or provide the full path to the file.
try:
    df = pd.read_csv('technical_skills_Job_roles_dataset.csv')
except FileNotFoundError:
    print("Error: The file 'technical_skills_Job_roles_dataset.csv' was not found.")
    # As a fallback for demonstration, creating a dummy dataframe.
    # In your environment, please ensure the file is correctly uploaded.
    data = {'Technical_Skills': ['Risk Management, Auditing', 'Photoshop, Illustrator, InDesign', 'HVAC Design, Revit, BIM', 'Java, Spring Boot, REST API', 'Data Analytics, Power BI, DAX'],
            'Educational_Qualification': ['M.Sc in Data Science', 'B.Tech in Computer Science', 'B.Pharm in Pharmacy', 'B.Des in Graphic Design', 'B.Pharm in Pharmacy'],
            'Job_Role': ['Business Analyst', 'Graphic Designer', 'Mechanical Engineer', 'Cybersecurity Analyst', 'Data Analyst']}
    df = pd.DataFrame(data)


# Take a random sample of 1000 rows if the dataframe is large enough
if len(df) > 1000:
    df_sample = df.sample(n=1000, random_state=42)
else:
    df_sample = df

# ---- Visualization 1: Distribution of Job Roles ----
plt.figure(figsize=(12, 8))
sns.countplot(y='Job_Role', data=df_sample, order=df_sample['Job_Role'].value_counts().index, palette='viridis')
plt.title('Distribution of Job Roles')
plt.xlabel('Count')
plt.ylabel('Job Role')
plt.tight_layout()
plt.savefig('job_roles_distribution.png')
# plt.show() # Uncomment to display the plot directly

# ---- Visualization 2: Distribution of Educational Qualifications ----
plt.figure(figsize=(12, 8))
sns.countplot(y='Educational_Qualification', data=df_sample, order=df_sample['Educational_Qualification'].value_counts().index, palette='plasma')
plt.title('Distribution of Educational Qualifications')
plt.xlabel('Count')
plt.ylabel('Educational Qualification')
plt.tight_layout()
plt.savefig('educational_qualifications_distribution.png')
# plt.show()

# ---- Visualization 3: Top 20 most frequent Technical Skills ----
# Process the 'Technical_Skills' column
skills = df_sample['Technical_Skills'].str.split(', ').explode().str.strip()
top_20_skills = skills.value_counts().nlargest(20)

plt.figure(figsize=(12, 8))
sns.barplot(x=top_20_skills.values, y=top_20_skills.index, palette='magma')
plt.title('Top 20 Most Frequent Technical Skills')
plt.xlabel('Frequency')
plt.ylabel('Technical Skill')
plt.tight_layout()
plt.savefig('top_20_skills.png')
# plt.show()

# ---- Visualization 4: Heatmap of Educational Qualification vs. Job Role ----
contingency_table = pd.crosstab(df_sample['Educational_Qualification'], df_sample['Job_Role'])

# To make the heatmap more readable, let's select the top 10 job roles and top 10 qualifications
top_10_job_roles = df_sample['Job_Role'].value_counts().nlargest(10).index
top_10_qualifications = df_sample['Educational_Qualification'].value_counts().nlargest(10).index
# Ensure that all top 10 qualifications and job roles are in the contingency table
contingency_table_top10 = contingency_table.loc[contingency_table.index.isin(top_10_qualifications), contingency_table.columns.isin(top_10_job_roles)]


plt.figure(figsize=(14, 10))
sns.heatmap(contingency_table_top10, annot=True, fmt='d', cmap='YlGnBu')
plt.title('Heatmap of Top 10 Educational Qualifications vs. Top 10 Job Roles')
plt.xlabel('Job Role')
plt.ylabel('Educational Qualification')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('qualification_vs_job_role_heatmap.png')
# plt.show()

# ---- Visualization 5: Box plot of Number of Skills per Job Role ----
# We will consider only the top 10 job roles for better readability
df_sample['Skills_Count'] = df_sample['Technical_Skills'].str.split(',').str.len()
top_10_job_roles_for_boxplot = df_sample['Job_Role'].value_counts().nlargest(10).index
df_top_10_jobs = df_sample[df_sample['Job_Role'].isin(top_10_job_roles_for_boxplot)]

plt.figure(figsize=(15, 8))
sns.boxplot(x='Skills_Count', y='Job_Role', data=df_top_10_jobs, palette='coolwarm', order=top_10_job_roles_for_boxplot)
plt.title('Number of Skills per Job Role (Top 10 Roles)')
plt.xlabel('Number of Skills')
plt.ylabel('Job Role')
plt.tight_layout()
plt.savefig('skills_per_job_role_boxplot.png')
# plt.show()

print("5 visualizations have been generated and saved as PNG files.")