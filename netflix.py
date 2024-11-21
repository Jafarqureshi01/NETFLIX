import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load Netflix Dataset
@st.cache
def load_data():
    return pd.read_csv("netflix_titles.csv")

# Data Cleaning
def clean_data(df):
    # Drop rows where 'title' or 'type' is missing
    df.dropna(subset=["title", "type"], inplace=True)
    # Fill missing values in 'country' and 'director' with "Unknown"
    df["country"].fillna("Unknown", inplace=True)
    df["director"].fillna("Unknown", inplace=True)
    # Fill missing values in 'rating' with "Not Rated"
    df["rating"].fillna("Not Rated", inplace=True)
    return df

# Streamlit App
st.title("Netflix Dataset Analysis")

# Load and Clean Data
netflix_df = load_data()
netflix_df = clean_data(netflix_df)

# Dataset Overview
st.subheader("Netflix Dataset")
st.dataframe(netflix_df)

# Dataset Summary
st.subheader("Dataset Summary")
st.write(netflix_df.describe(include="all"))

# Most Popular Types
st.subheader("Movies vs TV Shows")
type_counts = netflix_df["type"].value_counts()
fig1, ax1 = plt.subplots()
sns.barplot(x=type_counts.index, y=type_counts.values, palette="viridis", ax=ax1)
ax1.set_title("Movies vs TV Shows")
ax1.set_ylabel("Count")
ax1.set_xlabel("Type")
st.pyplot(fig1)

# Top 10 Countries
st.subheader("Top 10 Countries Producing Netflix Content")
top_countries = netflix_df["country"].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_countries.values, y=top_countries.index, palette="coolwarm", ax=ax2)
ax2.set_title("Top 10 Countries")
ax2.set_xlabel("Count")
ax2.set_ylabel("Country")
st.pyplot(fig2)

# Top Genres
st.subheader("Top Genres on Netflix")
netflix_df["genres"] = netflix_df["listed_in"].str.split(", ")
top_genres = pd.Series(
    [genre for sublist in netflix_df["genres"].dropna() for genre in sublist]
).value_counts().head(10)
fig3, ax3 = plt.subplots()
sns.barplot(x=top_genres.values, y=top_genres.index, palette="mako", ax=ax3)
ax3.set_title("Top Genres")
ax3.set_xlabel("Count")
ax3.set_ylabel("Genre")
st.pyplot(fig3)

# Content Trends by Year
st.subheader("Content Trend Over the Years")
content_by_year = netflix_df["release_year"].value_counts().sort_index()
fig4, ax4 = plt.subplots()
sns.lineplot(x=content_by_year.index, y=content_by_year.values, marker="o", color="green", ax=ax4)
ax4.set_title("Content Trend Over the Years")
ax4.set_xlabel("Year")
ax4.set_ylabel("Number of Titles Released")
st.pyplot(fig4)

# Download Cleaned Dataset
st.subheader("Download Cleaned Dataset")
csv = netflix_df.to_csv(index=False)
st.download_button(
    label="Download Cleaned Dataset as CSV",
    data=csv,
    file_name="cleaned_netflix_titles.csv",
    mime="text/csv",
)
