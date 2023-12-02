# functions
def addNumbers(a, b):
    print("Sum is ", a + b)

file_path = "data/0101.ipynb"
def get_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content
    print(content)