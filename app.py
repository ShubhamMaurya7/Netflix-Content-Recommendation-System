import streamlit as st
import pickle
import pandas as pd

# Load data
df = pickle.load(open("netflix_df.pkl", "rb"))
cosine_sim = pickle.load(open("cosine_sim.pkl", "rb"))

# Create title index
indices = pd.Series(df.index, index=df['title'].str.lower())

# Recommendation logic
def recommend(title):
    title = title.lower()
    if title not in indices:
        return ["Sorry, title not found."]
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices].tolist()

# Streamlit UI
st.set_page_config(page_title="Netflix Recommender", layout="centered")
st.title("🎬 Netflix Content Recommender System")

user_input = st.text_input("Enter a Netflix Title:", placeholder="E.g. Narcos")

if st.button("Get Recommendations"):
    recommendations = recommend(user_input)
    st.subheader("Top 5 Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        st.write(f"{i}. {rec}")
