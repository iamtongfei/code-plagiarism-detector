
import nbformat
import json



def get_list_cells(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Parse the notebook content using nbformat
        notebook = nbformat.reads(content, as_version=4)

        # Convert the notebook content to a JSON object
        notebook_json = nbformat.writes(notebook)
        notebook_json_obj = json.loads(notebook_json)

    return notebook_json_obj['cells']