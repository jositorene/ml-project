import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize

print("Loading dataset...")
df = pd.read_csv('final_recipe_index.csv')
df['recipe_features'] = df['recipe_features'].fillna('')

print("Vectorizing ingredients... (this may take several minutes for 2M rows)")

# IMPORTANT: limit max_features to reduce memory explosion
tfidf = TfidfVectorizer(
    stop_words='english',
    max_features=50000,      # prevents huge RAM usage
    dtype=np.float32         # reduce memory
)

tfidf_matrix = tfidf.fit_transform(df['recipe_features'])

# Normalize vectors (important for cosine similarity)
tfidf_matrix = normalize(tfidf_matrix)

print("Building NearestNeighbors index...")

# Use brute force with cosine on sparse matrix (best for TF-IDF sparse)
nn_model = NearestNeighbors(
    n_neighbors=5,
    metric='cosine',
    algorithm='brute',
    n_jobs=-1
)

nn_model.fit(tfidf_matrix)

print("System ready!")

def suggest_recipes(user_ingredients, top_n=5):
    
    # Transform user input
    user_vec = tfidf.transform([user_ingredients.lower()])
    user_vec = normalize(user_vec)
    
    # Get nearest neighbors
    distances, indices = nn_model.kneighbors(user_vec, n_neighbors=top_n)
    
    # Convert cosine distance → similarity
    similarity_scores = 1 - distances.flatten()
    
    results = df.iloc[indices.flatten()].copy()
    results['similarity_score'] = similarity_scores
    
    return results.sort_values(by='similarity_score', ascending=False)

# --- TEST ---
my_fridge = "tomato, cheese, lettuce, potatoes, rice"
suggestions = suggest_recipes(my_fridge, top_n=5)

print(f"\nTop suggestions for: {my_fridge}")
print(suggestions[['title', 'directions' , 'link', 'similarity_score']])