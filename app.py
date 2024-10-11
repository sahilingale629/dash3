import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
github_projects = pd.read_csv('data/github_dataset.csv')
repository_data = pd.read_csv('data/repository_data.csv')

# Remove the 'contributors' column from the repository_data dataset
if 'contributors' in repository_data.columns:
    repository_data = repository_data.drop(columns=['contributors'])

# Dashboard Title
st.title('GitHub Projects Data Dashboard')

# Sidebar filters
st.sidebar.header('Filter Options')
dataset_option = st.sidebar.selectbox('Select Dataset', ('GitHub Projects', 'Repository Data'))
language_filter = st.sidebar.multiselect('Filter by Language', 
                                         options=github_projects['language'].unique() if dataset_option == 'GitHub Projects' 
                                         else repository_data['primary_language'].unique(),
                                         default=None)
min_stars = st.sidebar.slider('Minimum Stars', 0, int(github_projects['stars_count'].max() if dataset_option == 'GitHub Projects' else repository_data['stars_count'].max()), 0)
# Filter the data based on selection
def filter_data(df, language_column):
    filtered_data = df if not language_filter else df[df[language_column].isin(language_filter)]
    filtered_data = filtered_data[filtered_data['stars_count'] >= min_stars]
    return filtered_data

# Select the correct dataset and apply filters
if dataset_option == 'GitHub Projects':
    data = filter_data(github_projects, 'language')
else:
    data = filter_data(repository_data, 'primary_language')

# Function to display language popularity
def language_popularity(df, language_column):
    lang_count = df[language_column].value_counts().head(10)
    fig, ax = plt.subplots()
    ax.bar(lang_count.index, lang_count.values, color='dodgerblue')
    ax.set_title('Top 10 Languages')
    ax.set_xlabel('Languages')
    ax.set_ylabel('Number of Repositories')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Language popularity visualization
st.header('Language Popularity')
language_popularity(data, 'language' if dataset_option == 'GitHub Projects' else 'primary_language')

# Stars vs Forks or Issues vs Pull Requests
st.header('Select Metric to Visualize')
metric_option = st.radio('Choose metric', ['Stars vs Forks', 'Issues vs Pull Requests'])

if metric_option == 'Stars vs Forks':
    st.write(f'Correlation between Stars and Forks ({dataset_option})')
    fig, ax = plt.subplots()
    ax.scatter(data['stars_count'], data['forks_count'], alpha=0.5, color='green')
    ax.set_xlabel('Stars')
    ax.set_ylabel('Forks')
    ax.set_title('Stars vs Forks')
    st.pyplot(fig)
else:
    st.write(f'Issues vs Pull Requests ({dataset_option})')
    fig, ax = plt.subplots()
    ax.scatter(data['issues_count'], data['pull_requests'], alpha=0.5, color='blue')
    ax.set_xlabel('Issues')
    ax.set_ylabel('Pull Requests')
    ax.set_title('Issues vs Pull Requests')
    st.pyplot(fig)

# Top contributors visualization (GitHub Projects only)
if dataset_option == 'GitHub Projects':
    st.header('Top Contributors')
    top_contributors = data.nlargest(10, 'contributors')
    st.table(top_contributors[['repositories', 'contributors']])

# Summary statistics
st.header('Summary Statistics')
if dataset_option == 'GitHub Projects':
    st.write(data[['stars_count', 'forks_count', 'issues_count', 'pull_requests', 'contributors']].describe())
else:
    st.write(data[['stars_count', 'forks_count', 'watchers', 'pull_requests']].describe())
