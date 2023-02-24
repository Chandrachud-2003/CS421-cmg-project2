# Using Python, write a small program to crawl through the repositories looking for Python files, such files will have an extension of “.py”.

import os
import sys

# Declaring class
class PythonCrawler:

    # Storing the paths of all the .py files in a list
    py_files = []
    path = ""

    # Declaring constructor
    def __init__(self, path):
        self.path = path
        self.py_files = []

    # Declaring method to crawl through the repositories
    def crawl(self):
        self.py_files = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".py"):
                    # Removing the whitespaces before and after the file name
                    file = file.strip()
                    # Adding the path of the file to the list
                    self.py_files.append(os.path.join(root, file))

        # Returning the list of all the .py files
        return self.py_files

    # Getting the list of all the .py files
    def get_py_files(self):
        return self.py_files
                    
    # Decaring method to print the paths of all the .py files
    def print_py_files(self):
        for file in self.py_files:
            print(file)


    # Aggregating all the py files in a single file
    def aggregate_py_files(self, invalid_char='?'):

        import os
        import re
        
        # Deleting the file if it already exists
        if os.path.exists("aggregate_py_files.py"):
            os.remove("aggregate_py_files.py")

        with open("aggregate_py_files.py", "w", encoding='utf-8') as f:
            for file in self.py_files:
                # Checking if the file path is valid
                if os.path.exists(file):
                    # Use a raw string by prefixing the string literal with 'r'.
                    file = r"{}".format(file)
                    with open(file, "r", encoding='latin-1') as f1:
                        # Removing all the comments from the file
                        lines = f1.readlines()
                        for line in lines:
                            # Fixing inconsistent use of tabs and spaces in indentation
                            if line.startswith("\t"):
                                line = line.replace("\t", "    ")
                            f.write(line)
                else:
                    print("File path is invalid")

    # Crawling through only the Python repositories (numpy) and aggregating all the py files in a single file
    def aggregate_py_files_flask(self, invalid_char='?'):

        import os
        import re

        # Crawling through numpy repository to store all the file paths in a list
        numpy_py_files = []
        for root, dirs, files in os.walk("Python Repositories/flask"):
            for file in files:
                if file.endswith(".py"):
                    # Removing the whitespaces before and after the file name
                    file = file.strip()
                    # Adding the path of the file to the list
                    numpy_py_files.append(os.path.join(root, file))
        
        # Deleting the file if it already exists
        if os.path.exists("aggregate_py_files_flask.py"):
            os.remove("aggregate_py_files_flask.py")

        with open("aggregate_py_files_flask.py", "w", encoding='utf-8') as f:
            for file in numpy_py_files[0:1]:
                # Checking if the file path is valid
                if os.path.exists(file):
                    # Use a raw string by prefixing the string literal with 'r'.
                    file = r"{}".format(file)
                    with open(file, "r", encoding='latin-1') as f1:
                        # Removing all the comments from the file
                        lines = f1.readlines()
                        for line in lines:
                            # Fixing inconsistent use of tabs and spaces in indentation
                            if line.startswith("\t"):
                                line = line.replace("\t", "    ")
                            f.write(line)
                else:
                    print("File path is invalid") 