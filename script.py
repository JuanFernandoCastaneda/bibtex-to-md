# 0. Assume that all entries of papers end in a double }}.
# 1. I will assume that the file is a well written bib file.
# 2. I will assume that citation's attributes have a space (\n) 
# between them. It is a reasonable assumption because all
# bib generators in journals do it by default. Even if not, it 
# can be fixed by hand when adding a new bib.
# 3. I will assume there are no spaces (\n) INSIDE the attributes.

def generate_literature_md_files():
    f = open("bibtex.bib", "r", encoding='utf-8')
    # Transform all at once all accent encodings into accents. 
    f = transform_accents(f.read())
    # Remove all tabs and split by ocurrence. "{" is not replaced yet 
    # because it can be part of the texts.
    entries = f.replace("\t", "").split("@")
    for index, entry in enumerate(entries):
        # This means its a year ({---2XXX---}) or is an empty entry.
        if entry == "" or entry[0] == "{":
            continue 
        rows = entry.split("\n")
        # Remove all empty rows.
        # This will make the evaluation of the last row make sense.
        rows = [row for row in rows if row]
        print(rows)
        # A dictionary is created because we want to minimize IO ops.
        attributes = {}
        # First row is the type. Get the type of the bib and its id. 
        # Comma can be removed without problem.
        first_row = rows.pop(0).replace(",", "")
        type, id = first_row.split("{")
        for index, row in enumerate(rows):
            first_equal_index = row.find("=")
            attribute_name = row[:first_equal_index].strip().capitalize()
            attribute_value = row[(first_equal_index+1):]
            # There is still a ending colon and a {} in attribute value.
            # Colon is removed by last } because its always after that.
            attribute_value = attribute_value[attribute_value.find("{")+1
                :attribute_value.rfind("}")].strip()
            # If it is the last row there is another } to remove.
            if row == rows[-1]:
                attribute_value = attribute_value[:attribute_value.rfind("}")]
            attributes[attribute_name] = attribute_value
        save_attributes(attributes)

def save_attributes(attributes):
    # Get file name.
    if 'Doi' in attributes:
        # Looks cool
        id = "".join(letter for letter in attributes['Doi']
                     if letter.isalnum() or letter == ".")
    else:
        # Convert it to a format good for files.
        id = "".join(letter for letter 
                     in attributes['Title'].replace(" ", "-")
                     if letter.isalnum() or letter == "-")
    f = open(f"_bib\\{id}.md", "w",
             encoding='utf-8')
    f.write("---\n")
    for attribute in attributes:
        f.write(f'{attribute}: "{attributes[attribute]}" \n')
    f.write("---")
    f.close()

def transform_accents(phrase):
    # Original structure: \'{letter}
    phrase = phrase.replace("\\\'{a}", "á")
    phrase = phrase.replace("\\\'{e}", "é")
    phrase = phrase.replace("\\\'{i}", "í")
    phrase = phrase.replace("\\\'{o}", "ó")
    phrase = phrase.replace("\\\'{u}", "ú")
    return phrase

generate_literature_md_files()

