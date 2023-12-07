import os
import nbformat
from fuzzywuzzy import fuzz 

class Detector:
    
    def __init__(self, path):
        self.path = path

    def compare_notebooks(self, notebook1, notebook2):
        cells1 = notebook1['cells']
        cells2 = notebook2['cells']
        content1 = '\n'.join([cell['source'] for cell in cells1 if cell['cell_type'] == 'code'])
        content2 = '\n'.join([cell['source'] for cell in cells2 if cell['cell_type'] == 'code'])
        similarity_ratio = fuzz.ratio(content1, content2)
        return similarity_ratio

    def generate_results(self, threshold=40, output_size=3):
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

                similarity_ratio = self.compare_notebooks(notebook1, notebook2)

                if similarity_ratio > threshold:
                    result = (similarity_ratio, f"The similarity score of the .ipynb files {ipynb_files[i]} and {ipynb_files[j]} is {similarity_ratio}, indicating potential plagiarism.\n")
                    results.append(result)

        sorted_results = sorted(results, key=lambda x: x[0], reverse=True)

        for score, message in sorted_results[:output_size]:
            print(message)
