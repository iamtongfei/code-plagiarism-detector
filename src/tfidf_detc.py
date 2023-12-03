import os
import nbformat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

        # TF-IDF Vectorization
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform([content1, content2])

        # Calculate cosine similarity between TF-IDF vectors
        similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
        return similarity_score

    def generate_results(self, output_size=3):
        similarity_scores = []
        for i in range(len(self.ipynb_files)):
            for j in range(i + 1, len(self.ipynb_files)):
                file1_path = os.path.join(self.path, self.ipynb_files[i])
                file2_path = os.path.join(self.path, self.ipynb_files[j])
                similarity_ratio = self.compare_notebook_similarity(file1_path, file2_path)
                similarity_scores.append(((self.ipynb_files[i], self.ipynb_files[j]), similarity_ratio))

        # Sort similarity_scores list based on similarity ratio (second element in tuple)
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Display the top output_size pairs with the highest plagiarism scores
        for pair, score in similarity_scores[:output_size]:
            file1, file2 = pair
            print(f"Potential plagiarism detected between {file1} and {file2} - Similarity: {float(score * 100)}")
