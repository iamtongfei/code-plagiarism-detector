# import functions from other files
from src.parser import *

addNumbers(1,2)


class Detector:
    def __init__(self, path):
        self.path = path #path

    def generate_results(self):
        # Implement your code here to generate results using the provided path
        # For example:
        print("start the work now 2:02")
        # Your detection logic goes here
    
    def get_file_content(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

        print(content)


