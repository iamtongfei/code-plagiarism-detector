import os
import nbformat
import re
from fuzzywuzzy import fuzz


class Detector:
    def __init__(self, path):
        self.path = path

    def extract_comments_and_identifiers(self,notebook):
        comments = []
        identifiers = set()
    
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                code = cell.source
                # Remove comments
                code = re.sub(r'#.*', '', code)  
                # Extract and Remove identifiers 
                code = re.sub(r'\b\w+\b', '', code)  
                comments.append(code)
                # Extract identifiers and add them to the set
                identifiers.update(re.findall(r'\b\w+\b', cell.source))
    
        return '\n'.join(comments), identifiers
    
    def generate_results(self, threshold=40, output_size=None):
        ipynb_files = [f for f in os.listdir(self.path) if f.endswith('.ipynb')]
        results = []

        for i in range(len(ipynb_files)):
            for j in range(i + 1, len(ipynb_files)):
                file1_path = os.path.join(self.path, ipynb_files[i])
                file2_path = os.path.join(self.path, ipynb_files[j])

                with open(file1_path, 'r', encoding='utf-8') as file1:
                    notebook1 = nbformat.read(file1, as_version=4)

                with open(file2_path, 'r', encoding='utf-8') as file2:
                    notebook2 = nbformat.read(file2, as_version=4)

                comments1, identifiers1 = self.extract_comments_and_identifiers(notebook1)
                comments2, identifiers2 = self.extract_comments_and_identifiers(notebook2)

                comments_similarity = fuzz.ratio(comments1, comments2)
                identifiers_similarity = fuzz.ratio(' '.join(identifiers1), ' '.join(identifiers2))

                max_similarity = max(comments_similarity, identifiers_similarity)

                if comments_similarity > threshold or identifiers_similarity > threshold:
                    result = (max_similarity, f"The content of {ipynb_files[i]} and {ipynb_files[j]} notebooks is similar, "
                                              f"with comment similarity of {comments_similarity} "
                                              f"and identifier similarity of {identifiers_similarity}.\n")
                    results.append(result)

        sorted_results = sorted(results, key=lambda x: x[0], reverse=True)

        for _, message in sorted_results[:output_size]:
            print(message)