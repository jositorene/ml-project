import pandas as pd
import ast
import csv

input_file = 'full_dataset.csv'
output_file = 'final_recipe_index.csv'
chunk_size = 50000

# This function converts the string "['salt', 'pepper']" into a real list ['salt', 'pepper']
def parse_ner(ner_string):
    try:
        return " ".join(ast.literal_eval(ner_string))
    except:
        return ""

# Remove the output file if it exists (start fresh)
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Write clean header explicitly
    writer.writerow(['title', 'recipe_features', 'ingredients', 'directions', 'link'])

# Process chunks
chunks = pd.read_csv(input_file, chunksize=chunk_size, dtype=str)

for i, chunk in enumerate(chunks):
    # Strip any whitespace from column names
    chunk.columns = [col.strip() for col in chunk.columns]

    # Ensure all required columns exist
    required_cols = ['title', 'NER', 'ingredients', 'directions', 'link']
    for col in required_cols:
        if col not in chunk.columns:
            chunk[col] = ""

    # 1. Clean the NER column: convert string-list to a simple space-separated string
    chunk['recipe_features'] = chunk['NER'].apply(parse_ner)

    # 2. Keep only the columns we need for the suggestion engine
    cols_to_keep = ['title', 'recipe_features', 'ingredients', 'directions', 'link']
    simplified_chunk = chunk[cols_to_keep]

    # 3. Strip extra quotes and whitespace from string columns
    for c in cols_to_keep:
        simplified_chunk[c] = simplified_chunk[c].astype(str).str.strip().str.replace(r'^"+|"+$', '', regex=True)

    # 4. Append to CSV
    simplified_chunk.to_csv(output_file, mode='a', index=False, header=False, encoding='utf-8', quoting=csv.QUOTE_MINIMAL)

    print(f"Processed {i+1} chunks...")

print("Done! Your optimized dataset is ready in final_recipe_index.csv")