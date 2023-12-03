# import functions from other files
from src.parser import *
import os
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

verbose = False
cell_list = []

class Detector:

    def __init__(self, path):
        self.path = path #path

    def generate_results(self):
        # Implement your code here to generate results using the provided path
        # For example:
        print(f"Similarity Score Using CountVector: {self.get_sim()}")
        return self.get_sim()
    
    def get_file_content(self):
        #return in json object
        return get_list_cells(self.path)
    
    def get_combined_text(self):
        combined_text = []
        # Call get_file_content method to get the file content
        cell_list = self.get_file_content()

        # Process the returned content to get the combined text
        for cell in cell_list:
            if verbose:
                print(cell['cell_type'])
                print(cell['source'])

            if cell['cell_type'] == "markdown":
                # continue
                combined_text += cell['source']
            elif cell['cell_type'] == "code": 
                combined_text += cell['source']
                if verbose: 
                    print("code session: ")
                    print(f"code content: {cell['source']}")
                    print(combined_text)
                    print("-----")
        return combined_text

    def tokenize_database_files(self):
        data_directory = 'data'  # Replace this with your actual data directory path
        combined_dataset = []

        # Iterate through the files in the directory
        for filename in os.listdir(data_directory):
            if filename.endswith(".ipynb"):  # Check if the file is a Jupyter Notebook
                notebook_path = os.path.join(data_directory, filename)

                with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
                    notebook_content = nbformat.read(notebook_file, as_version=4)

                    # Iterate through the cells in each notebook and add them to the combined notebook
                    for cell in notebook_content.cells:
                        if cell['cell_type'] == "markdown":
                            combined_dataset += [cell['source']]
                        elif cell['cell_type'] == "code":
                            combined_dataset += [cell['source']]
        return combined_dataset
    

    def get_sim(self):
        list1 = self.get_combined_text()  # Your input list
        list2 = list(set(self.tokenize_database_files()))

        # Initialize CountVectorizer and TF-IDF Vectorizer
        count_vectorizer = CountVectorizer()
        tfidf_vectorizer = TfidfVectorizer()

        # Fit and transform data with CountVectorizer
        count_matrix_list1 = count_vectorizer.fit_transform(list1)
        count_matrix_list2 = count_vectorizer.transform(list2)

        # Fit and transform data with TF-IDF Vectorizer
        tfidf_matrix_list1 = tfidf_vectorizer.fit_transform(list1)
        tfidf_matrix_list2 = tfidf_vectorizer.transform(list2)

        # Calculate cosine similarity for CountVectorizer and TF-IDF
        similarity_count = cosine_similarity(count_matrix_list1, count_matrix_list2)
        similarity_tfidf = cosine_similarity(tfidf_matrix_list1, tfidf_matrix_list2)

        if verbose:
            print("Similarity using CountVectorizer:")
            print(similarity_count)
            print("max:")
            print(similarity_count.max())
            print(f"Score: {similarity_count.max() * 100} ")

            print("\nSimilarity using TF-IDF:")
            print(similarity_tfidf)
            print("max:")
            print(similarity_tfidf.max())
            print(f"Score: {similarity_tfidf.max() * 100} ")

        similarity_countVec_score = round(similarity_count.max() * 100, 2)
        return similarity_countVec_score




