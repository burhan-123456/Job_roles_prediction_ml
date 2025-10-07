import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the complete dataset
try:
    df = pd.read_csv('technical_skills_Job_roles_dataset.csv')
    print("Dataset loaded successfully.")
    print(f"The dataset contains {len(df)} rows.")
except FileNotFoundError:
    print("Error: The file 'technical_skills_Job_roles_dataset.csv' was not found.")
    # Create a dummy dataframe to allow the rest of the code to run for demonstration
    df = pd.DataFrame({
        'Job_Role': ['Data Analyst', 'Business Analyst', 'Data Analyst', 'Software Engineer', 'Financial Analyst', 'Data Analyst', 'Business Analyst', 'Graphic Designer'],
        'Educational_Qualification': ['M.Sc in Data Science', 'B.Tech in Computer Science', 'M.Sc in Data Science', 'B.Tech in Computer Science', 'MBA in Finance', 'M.Sc in Data Science', 'B.Tech in Computer Science', 'B.Des in Graphic Design'],
        'Technical_Skills': ['SQL, Python, Tableau', 'SQL, Power BI, Excel', 'Python, R, Power BI', 'Java, Python, Git', 'Excel, Financial Modeling', 'SQL, Excel, Python', 'Communication, SQL', 'Photoshop, Illustrator']
    })

# --- Data Preparation ---
# Calculate the number of skills for each role
df['Skills_Count'] = df['Technical_Skills'].astype(str).str.split(',').str.len()


# --- Visualization 1: Pie Chart of the Top 10 Job Roles ---
top_10_roles = df['Job_Role'].value_counts().nlargest(10)
plt.figure(figsize=(12, 10))
plt.pie(top_10_roles, labels=top_10_roles.index, autopct='%1.1f%%', startangle=140, pctdistance=0.85)
# Draw a circle at the center to make it a donut chart
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('Proportion of Top 10 Job Roles in the Dataset', size=16)
plt.tight_layout()
plt.savefig('pie_chart_top_10_job_roles.png')


# --- Visualization 2: Column Chart of Top Skills for the Most Frequent Job Role ---
most_frequent_role = df['Job_Role'].mode()[0]
df_specific_role = df[df['Job_Role'] == most_frequent_role]

# Process skills for this specific role
skills_specific_role = df_specific_role['Technical_Skills'].str.split(', ').explode().str.strip()
top_15_skills = skills_specific_role.value_counts().nlargest(15)

plt.figure(figsize=(12, 8))
sns.barplot(x=top_15_skills.index, y=top_15_skills.values, palette='crest')
plt.title(f'Top 15 Most Required Skills for a {most_frequent_role}', size=16)
plt.xlabel('Technical Skill', size=12)
plt.ylabel('Frequency', size=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('column_chart_top_skills_for_role.png')


# --- Visualization 3: Bar Chart of Average Number of Skills per Educational Qualification ---
avg_skills_per_qual = df.groupby('Educational_Qualification')['Skills_Count'].mean().sort_values(ascending=False).nlargest(15)

plt.figure(figsize=(12, 10))
sns.barplot(x=avg_skills_per_qual.values, y=avg_skills_per_qual.index, palette='rocket')
plt.title('Average Number of Skills per Educational Qualification (Top 15)', size=16)
plt.xlabel('Average Number of Skills', size=12)
plt.ylabel('Educational Qualification', size=12)
plt.tight_layout()
plt.savefig('bar_chart_avg_skills_per_qualification.png')


# --- Visualization 4: Box Plot of Skill Count Distribution for Top 5 Job Roles ---
top_5_roles_list = df['Job_Role'].value_counts().nlargest(5).index
df_top_5_roles = df[df['Job_Role'].isin(top_5_roles_list)]

plt.figure(figsize=(14, 8))
sns.boxplot(y='Job_Role', x='Skills_Count', data=df_top_5_roles, palette='mako', order=top_5_roles_list)
plt.title('Distribution of Number of Skills for the Top 5 Job Roles', size=16)
plt.xlabel('Number of Skills', size=12)
plt.ylabel('Job Role', size=12)
plt.tight_layout()
plt.savefig('boxplot_skill_count_per_role.png')

print("4 new visualizations have been generated and saved as PNG files from the complete dataset.")
print(f"The most frequent job role found was: '{most_frequent_role}'")