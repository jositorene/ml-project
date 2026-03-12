import pandas as pd 
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize

# --- Load ingredients from JSON file ---
with open("ingredients.json", "r", encoding="utf-8") as f:
    ingredients_list = json.load(f)

# Join list into a single string for TF-IDF
my_fridge = ", ".join(ingredients_list)

print("Loading dataset...")
df = pd.read_csv('final_recipe_index.csv')
df['recipe_features'] = df['recipe_features'].fillna('')

print("Vectorizing ingredients... (this may take several minutes for 2M rows)")
tfidf = TfidfVectorizer(
    stop_words='english',
    max_features=50000,
    dtype=np.float32
)
tfidf_matrix = tfidf.fit_transform(df['recipe_features'])
tfidf_matrix = normalize(tfidf_matrix)

print("Building NearestNeighbors index...")
nn_model = NearestNeighbors(
    metric='cosine',
    algorithm='brute',
    n_jobs=-1
)
nn_model.fit(tfidf_matrix)

print("System ready!")

def suggest_recipes(user_ingredients, top_n=5):
    user_vec = tfidf.transform([user_ingredients.lower()])
    user_vec = normalize(user_vec)
    
    distances, indices = nn_model.kneighbors(user_vec, n_neighbors=top_n)
    similarity_scores = 1 - distances.flatten()
    
    results = df.iloc[indices.flatten()].copy()
    results['similarity_score'] = similarity_scores
    
    results = results.sort_values(by='similarity_score', ascending=False)
    return results

# --- TEST ---
suggestions = suggest_recipes(my_fridge, top_n=5)

# Select only needed columns
output = suggestions[['title', 'directions', 'link', 'similarity_score']].fillna('')

# Convert to JSON structure
result_json = {
    "query": my_fridge,
    "total_results": len(output),
    "recipes": output.to_dict(orient="records")
}

# Save JSON to file
with open("recipe_suggestions.json", "w", encoding="utf-8") as f:
    json.dump(result_json, f, indent=4, ensure_ascii=False)

print("\nResults saved to recipe_suggestions.json")
print(output)