import json
import os

all_text_file = './original_json/all_text.json'
output_dir = "./output"

chapter_out_dir = output_dir + '/chapters'
book_out_dir = output_dir + '/books'
intro_material_out_dir = output_dir + '/intro_material'

os.makedirs(output_dir, exist_ok=True)
os.makedirs(chapter_out_dir, exist_ok=True)
os.makedirs(book_out_dir, exist_ok=True)
os.makedirs(intro_material_out_dir, exist_ok=True)

with open(all_text_file, 'r', encoding='utf-8') as file:
    all_text_data = json.load(file)

current_book = ''
# Split the JSON into individual chapter files
for chunk in all_text_data['contents']:
    section = all_text_data['contents'][chunk]
    if 'verses' in section:
        ## actual chapter of scripture
        if section['chapter_name'] == 'Chapter 1':
            current_book = section['book_title']
        chapter_filename = f"{section['chapter_name'].lower().replace(' ', '_')}.json"
        output_path = chapter_out_dir + '/' + current_book.lower().replace(' ', '-')
        filepath = os.path.join(output_path, chapter_filename)

        # Prepare chapter-specific JSON
        chapter_data = {
            "title": section["title"],
            "chapter_title": section["chapter_name"],
            "summary": str(section["chapter_summary"][0]).replace('—', ' — '),
            "verses": section["verses"]
        }

        if "book_intro" in section and "book_title" not in section:
            ## i.e. the 3 nephi chapter heading before the summary
            chapter_data['chapter_heading'] = section['book_intro']

        os.makedirs(output_path, exist_ok=True)

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as chapter_file:
            json.dump(chapter_data, chapter_file, indent=2, ensure_ascii=False)
        
        ## handle book info if needed
        if "book_title" in section:
            book_data = {
                "title": section["book_title"],
            }

            if "subtitle" in section:
                book_data["subtitle"] = section["subtitle"]

            if "book_intro" in section:
                book_data["intro"] = section["book_intro"]

            book_filename = f"{section['book_title'].lower().replace(' ', '-')}.json"
            book_path = os.path.join(book_out_dir, book_filename)

                    # Write to file
            with open(book_path, 'w', encoding='utf-8') as book_file:
                json.dump(book_data, book_file, indent=2, ensure_ascii=False)
    else:
        ## title pages etc

        filename = f"{section['title'].lower().replace(' ', '-')}.json"
        filepath = os.path.join(intro_material_out_dir, filename)

        # Prepare chapter-specific JSON
        section_data = {
            "title": section["title"],
            "paragraphs": section["text"]
        }

        if "subtitle" in section_data:
            section_data["subtitle"] = section["subtitle"],

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as section_file:
            json.dump(section_data, section_file, indent=2, ensure_ascii=False)

# Provide the new directory structure as output
output_dir
