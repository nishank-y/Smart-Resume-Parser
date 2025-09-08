import json
import pandas as pd

def load_skills_list(file_path='data/skills_list.txt'):
    with open(file_path, 'r', encoding='utf-8') as f:
        skills = [line.strip() for line in f if line.strip()]
    return skills

def save_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def save_csv(data, output_file):
    """
    Save single dictionary or list of dictionaries to CSV.
    Converts lists in values to comma-separated strings.
    """
    # If a single dictionary is passed, wrap it in a list
    if isinstance(data, dict):
        data = [data]

    # Flatten lists in each dictionary
    flat_data = []
    for d in data:
        flat_row = {k: (', '.join(v) if isinstance(v, list) else v) for k, v in d.items()}
        flat_data.append(flat_row)

    # Create DataFrame and save
    df = pd.DataFrame(flat_data)
    df.to_csv(output_file, index=False)
