import os
import nbformat
import difflib


class Detector:
    
    def __init__(self, path, threshold=0.9):
        self.path = path
        self.threshold = threshold
        self.ipynb_files = [f for f in os.listdir(self.path) if f.endswith('.ipynb')]

    def read_notebook_content(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            notebook = nbformat.read(file, as_version=4)
        code_cells = [cell['source'] for cell in notebook.cells if cell.cell_type == 'code']
        return '\n'.join(code_cells)

    def compare_notebook_similarity(self, notebook1_path, notebook2_path):
        content1 = self.read_notebook_content(notebook1_path)
        content2 = self.read_notebook_content(notebook2_path)
        return difflib.SequenceMatcher(None, content1, content2).ratio()

    def generate_results(self, output_size=3):
        for i in range(len(self.ipynb_files)):
            for j in range(i + 1, len(self.ipynb_files)):
                file1_path = os.path.join(self.path, self.ipynb_files[i])
                file2_path = os.path.join(self.path, self.ipynb_files[j])
                similarity_ratio = self.compare_notebook_similarity(file1_path, file2_path)
                if similarity_ratio > self.threshold:
                    print(f"Potential plagiarism detected between {self.ipynb_files[i]} and {self.ipynb_files[j]} - Similarity: {similarity_ratio}")
