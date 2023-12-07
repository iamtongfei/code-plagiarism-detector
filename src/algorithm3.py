import os
from datasketch import MinHash, MinHashLSH

class Detector:
    def __init__(self, path):
        self.path = path
        self.notebook_files = [os.path.join(path, f"{i:04d}.ipynb") for i in range(101, 131)]

    def minhash_similarity(self, content1, content2):
        m1 = MinHash()
        m2 = MinHash()

        for word in content1.split():
            m1.update(word.encode('utf-8'))

        for word in content2.split():
            m2.update(word.encode('utf-8'))

        similarity_score = m1.jaccard(m2)
        return similarity_score

    def generate_results(self, output_size=3, threshold=0.5):
        similarity_scores = []

        for i in range(len(self.notebook_files)):
            for j in range(i + 1, len(self.notebook_files)):
                with open(self.notebook_files[i], 'r', encoding='utf-8') as file1, open(self.notebook_files[j], 'r', encoding='utf-8') as file2:
                    content1 = file1.read()
                    content2 = file2.read()
                    similarity_score = self.minhash_similarity(content1, content2)
                    similarity_scores.append((os.path.basename(self.notebook_files[i]), os.path.basename(self.notebook_files[j]), similarity_score))

        # Sort the results by similarity score in descending order
        top_results = sorted(similarity_scores, key=lambda x: x[2], reverse=True)[:output_size]

        return top_results
    
detector = Detector(path="data")
results = detector.generate_results(output_size=3)

for i, result in enumerate(results, start=1):
    print(f"{i}. The MinHash similarity score between notebooks {result[0]} and {result[1]} is {result[2]}, indicating potential plagiarism.")
