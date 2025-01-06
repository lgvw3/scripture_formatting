import os
import json

# Define base path for scripture data
BASE_PATH = "output"

def load_json_file(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def preprocess_scriptures():
    """Preprocess scripture data into a searchable format."""
    searchable_data = []

    # Process books
    books_path = os.path.join(BASE_PATH, "books")
    for file_name in os.listdir(books_path):
        if file_name.endswith(".json"):
            book_data = load_json_file(os.path.join(books_path, file_name))
            if "subtitle" in book_data:
                subtitle = book_data["subtitle"][0]
            else:
                subtitle = ""
            searchable_data.append({
                "id": book_data['title'].lower().replace(' ', '-'),
                "type": "book",
                "text": book_data["title"],  # Book title
                "summary": subtitle,  # Subtitle if available
            })

    # Process chapters
    chapters_path = os.path.join(BASE_PATH, "chapters")
    for book_folder in os.listdir(chapters_path):
        book_folder_path = os.path.join(chapters_path, book_folder)
        if os.path.isdir(book_folder_path):
            for file_name in os.listdir(book_folder_path):
                if file_name.endswith(".json"):
                    chapter_data = load_json_file(os.path.join(book_folder_path, file_name))
                    chapter_id = file_name.replace(".json", "")

                    # Add chapter data
                    searchable_data.append({
                        "id": chapter_data['title'],
                        "type": "chapter",
                        "chapter_id": chapter_data['chapter_title'],
                        "book_id": book_folder,
                        "summary": chapter_data.get("summary", ""),  # Chapter summary
                    })

                    # Add verses
                    for verse in chapter_data.get("verses", []):
                        searchable_data.append({
                            "id": f"verse_{chapter_data['title']}_{verse['number']}",
                            "verse_number": verse['number'],
                            "type": "verse",
                            "text": verse["text"],  # Verse text
                            "chapter_id": chapter_data['chapter_title'],
                            "book_id": book_folder,
                        })

    # Process introductory material
    intro_path = os.path.join(BASE_PATH, "intro_material")
    for file_name in os.listdir(intro_path):
        if file_name.endswith(".json"):
            intro_data = load_json_file(os.path.join(intro_path, file_name))
            searchable_data.append({
                "id": f"intro_{file_name.replace('.json', '')}",
                "type": "intro",
                "text": intro_data["title"],  # Title of the intro material
                "content": intro_data.get("text", ""),  # Introductory text
            })

    return searchable_data

def save_preprocessed_data(data, output_file):
    """Save preprocessed data to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # Preprocess data
    preprocessed_data = preprocess_scriptures()

    # Save to a JSON file
    output_file = os.path.join("output", "preprocessed_scripture_data.json")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    save_preprocessed_data(preprocessed_data, output_file)

    print(f"Preprocessed scripture data saved to {output_file}!")
