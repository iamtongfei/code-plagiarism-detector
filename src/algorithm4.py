import nbformat
import os
import hashlib

class Detector:   
    def __init__(self, path):
        self.path = path
    
    def read_notebook_code(self, notebook_path):
        with open(notebook_path, 'r', encoding='utf-8') as file:
            notebook = nbformat.read(file, as_version=4)
        code_cells = [cell.source for cell in notebook.cells if cell.cell_type == 'code']
        return ' '.join(code_cells)

    def tokenize(self, code):
        return set(code.split())

    def jaccard_index(self, set1, set2):
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union) if union else 0

    def generate_results(self, threshold=0.5, output_size=3):
        notebooks = [os.path.join(self.path, f) for f in os.listdir(self.path) if f.endswith('.ipynb')]
        results = []
        for i, nb_path1 in enumerate(notebooks):
            code1 = self.read_notebook_code(nb_path1)
            tokens1 = self.tokenize(code1)
            for j, nb_path2 in enumerate(notebooks[i+1:], start=i+1):
                code2 = self.read_notebook_code(nb_path2)
                tokens2 = self.tokenize(code2)
                index = self.jaccard_index(tokens1, tokens2)
                if index >= threshold:
                    results.append(((os.path.basename(nb_path1), os.path.basename(nb_path2)), index))

        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

        for result in sorted_results[:output_size]:
            print(f"Jaccard index between {result[0][0]} and {result[0][1]} is {result[1]:.4f}, which meets or exceeds the threshold.")
