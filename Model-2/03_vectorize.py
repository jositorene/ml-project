import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

# --- CLEAN AND LOAD CSV ---
input_csv = 'final_recipe_index.csv'

# Read the CSV raw
with open(input_csv, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Clean header: remove BOM, extra quotes, whitespace
header = lines[0].strip()
header = header.replace('"', '').replace("'", "")
header = ','.join([col.strip() for col in header.split(',')])
lines[0] = header + '\n'

# Write cleaned CSV back permanently
with open(input_csv, 'w', encoding='utf-8') as f:
    f.writelines(lines)

# Load CSV with cleaned header
df = pd.read_csv(input_csv)
required_cols = ['title', 'recipe_features', 'ingredients', 'directions', 'link']
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    raise ValueError(f"Missing columns in CSV after cleaning: {missing_cols}")

# Fill empty recipe_features
df['recipe_features'] = df['recipe_features'].fillna('')

print("Vectorizing ingredients... (this may take a minute)")

# --- TF-IDF VECTOR ---
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['recipe_features'])

def suggest_recipes(user_ingredients, top_n=5):
    user_vec = tfidf.transform([user_ingredients.lower()])
    similarity_scores = cosine_similarity(user_vec, tfidf_matrix).flatten()
    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    return df.iloc[top_indices]

# --- LOAD INGREDIENTS JSON ---
ingredients_file = 'ingredients.json'
with open(ingredients_file, 'r', encoding='utf-8') as f:
    ingredients_list = json.load(f)

if not isinstance(ingredients_list, list) or not all(isinstance(x, str) for x in ingredients_list):
    raise ValueError("ingredients.json should contain a list of strings")

my_fridge = ', '.join(ingredients_list)
suggestions = suggest_recipes(my_fridge)

print(f"\nTop suggestions for your ingredients: {my_fridge}")
print(suggestions[['title', 'directions', 'link']])

# --- SAVE TO JSON ---
output_file = 'recipe_suggestions.json'
suggestions[['title', 'directions', 'link']].to_json(output_file, orient='records', indent=2, force_ascii=False)
print(f"\nSuggestions saved to {output_file}")