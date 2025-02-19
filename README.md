# Sparse Matrix Implementation

# Overview
# This project implements a sparse matrix data structure optimized for memory and runtime efficiency.
# The program supports loading sparse matrices from files, performing addition, subtraction, and multiplication operations,
# and saving results to output files. It adheres to the requirements and instructions provided in the
# "Data Structures and Algorithms for Engineers" programming assignment.

# Directory Structure
# The project follows the specified directory structure:
# /dsa/sparse_matrix/code/src/       - Source code
# /dsa/sparse_matrix/sample_inputs/  - Input files
# /dsa/output/                       - Output files

# Ensure that the sample_inputs directory contains the input files (e.g., matrix1.txt, matrix2.txt)
# and that the output directory exists for storing results.

# Features
# - File Parsing: Reads sparse matrices from files in the format:
#   rows=8433
#   cols=3180
#   (0, 381, -694)
#   (0, 128, -838)
#   ...
#   Handles whitespace, ignores invalid lines, and raises errors for incorrect formats.
# - Matrix Operations:
#   - Addition: Adds two matrices with the same dimensions.
#   - Subtraction: Subtracts one matrix from another with the same dimensions.
#   - Multiplication: Multiplies two matrices where the number of columns in the first matrix matches
#     the number of rows in the second matrix.
# - Efficient Storage: Uses a dictionary to store only non-zero elements, minimizing memory usage.
# - Error Handling: Ensures robust error handling for invalid inputs, mismatched dimensions, and out-of-bounds indices.
# - Output Format: Saves results in the same sparse matrix format as the input files.

# Requirements
# - Python 3.x
# - No external libraries are used; all functionality is implemented from scratch.

# Installation and Setup
# 1. Clone the Repository:
#    git clone https://github.com/<https://github.com/Chol1000/dsa.git>/sparse_matrix.git
#    cd sparse_matrix
# 2. Organize Files:
#    - Place the source code in /dsa/sparse_matrix/code/src/.
#    - Place input files in /dsa/sparse_matrix/sample_inputs/.
#    - Ensure the /dsa/output/ directory exists for saving results.
# 3. Run the Program:
#    Navigate to the source code directory and execute the program:
#    python src/main.py

# Usage
# 1. Select Matrices:
#    - The program lists available matrices in the sample_inputs directory.
#    - Choose two matrices by entering their corresponding numbers.
# 2. Choose an Operation:
#    - Select an operation (Add, Subtract, or Multiply) by entering the corresponding number.
# 3. View Results:
#    - The result is saved in the /dsa/output/ directory with filenames like:
#      - addition_result.txt
#      - subtraction_result.txt
#      - multiplication_result.txt
# 4. Exit:
#    - Enter 4 to exit the program.

# Example Input File
# An example input file (matrix1.txt) might look like this:
# rows=5
# cols=5
# (0, 1, 10)
# (1, 2, 20)
# (2, 3, 30)
# (3, 4, 40)
# (4, 0, 50)

# Implementation Details
# Classes and Methods
# 1. SparseMatrix Class:
#    - Initialization:
#      - SparseMatrix(file_path=None, num_rows=0, num_cols=0)
#        - Loads a matrix from a file or initializes an empty matrix with given dimensions.
#    - Methods:
#      - get_element(row, col): Retrieves the value at (row, col); returns 0 if not present.
#      - set_element(row, col, value): Sets the value at (row, col); removes zero values.
#      - add(other): Adds two matrices.
#      - subtract(other): Subtracts one matrix from another.
#      - multiply(other): Multiplies two matrices.
#      - write_to_file(file_path): Writes the matrix to a file in sparse format.
# 2. Main Function:
#    - Handles user interaction, loads matrices, performs operations, and saves results.

# Error Handling
# - Invalid File Format:
#   - Raises an error if the file does not follow the expected format:
#     Input file has wrong format: std::invalid_argument
# - Mismatched Dimensions:
#   - Raises an error if matrices have incompatible dimensions for addition/subtraction/multiplication:
#     Matrices must have the same dimensions for addition
#     Number of columns in the first matrix must match number of rows in the second matrix
# - Out-of-Bounds Indices:
#   - Skips elements with out-of-bounds indices and prints a warning:
#     Skipping out-of-bounds element: (row, col) with value value

# Testing
# To test the program:
# 1. Place sample input files in /dsa/sparse_matrix/sample_inputs/.
# 2. Run the program and verify that results are saved correctly in /dsa/output/.

# Contribution
# This project was developed independently, adhering to the assignment's requirements.

# Contact
# For questions or feedback, contact the author at <c.monykuch@alustudent.com>.
