import pandas as pd
import re
import os

# 1. Configuration
input_file = 'full_dataset.csv'
output_file = 'cleaned_dataset.csv'
chunk_size = 50000  # Adjust if needed

# 2. Define cleaning function
def clean_ingredients(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s,]', '', text)
    return text.strip()

# 3. Remove old output file if it exists
if os.path.exists(output_file):
    os.remove(output_file)

print("Starting processing...")

# 4. Read CSV in chunks
chunks = pd.read_csv(input_file, chunksize=chunk_size)

for i, chunk in enumerate(chunks):

    # Normalize column names (fixes spaces, capitalization issues)
    chunk.columns = chunk.columns.str.strip().str.lower()

    # Ensure the ingredients column exists
    if 'ingredients' not in chunk.columns:
        raise ValueError(
            f"'ingredients' column not found. Available columns: {list(chunk.columns)}"
        )

    # Apply cleaning
    chunk['cleaned_ingredients'] = chunk['ingredients'].apply(clean_ingredients)

    # Write to output file
    chunk.to_csv(
        output_file,
        mode='a',
        index=False,
        header=(i == 0)
    )

    print(f"Finished chunk {i+1}")

print(f"Success! Cleaned data saved to: {output_file}")