#!/usr/bin/env python3

class SparseMatrix:
    def __init__(self, file_path=None, num_rows=0, num_cols=0):
        """
        Initialize a sparse matrix.
        If file_path is provided, read the matrix from the file.
        Otherwise, initialize an empty matrix with given dimensions.
        """
        self.rows = num_rows
        self.cols = num_cols
        self.data = {}  # Dictionary to store non-zero elements: (row, col) -> value

        if file_path:
            self._read_from_file(file_path)

    def _read_from_file(self, file_path):
        """
        Read a sparse matrix from a file line by line to handle large files.
        """
        rows_read = False
        cols_read = False

        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace
                if not line:
                    continue  # Skip empty lines

                if line.startswith("rows="):
                    self.rows = int(line.split("=")[1])
                    rows_read = True
                elif line.startswith("cols="):
                    self.cols = int(line.split("=")[1])
                    cols_read = True
                elif line.startswith("(") and line.endswith(")"):
                    # Parse (row, col, value)
                    line = line[1:-1]  # Remove parentheses
                    parts = line.split(",")
                    if len(parts) != 3:
                        raise ValueError("Input file has wrong format")

                    try:
                        row = int(parts[0])
                        col = int(parts[1])
                        value = float(parts[2])  # Allow floating-point values
                    except ValueError:
                        raise ValueError("Input file contains invalid values")

                    if row >= self.rows or col >= self.cols:
                        raise ValueError(f"Row or column index out of bounds: ({row}, {col}) for matrix of size ({self.rows}, {self.cols})")

                    self.data[(row, col)] = value
                else:
                    raise ValueError("Input file has wrong format")

        if not rows_read or not cols_read:
            raise ValueError("Input file missing rows or cols")

    def get_element(self, row, col):
        """
        Get the value at (row, col).
        Returns 0 if the element is not in the sparse matrix.
        """
        if row >= self.rows or col >= self.cols:
            raise ValueError(f"Row or column index out of bounds: ({row}, {col}) for matrix of size ({self.rows}, {self.cols})")
        return self.data.get((row, col), 0)

    def set_element(self, row, col, value):
        """
        Set the value at (row, col).
        """
        if row >= self.rows or col >= self.cols:
            raise ValueError(f"Row or column index out of bounds: ({row}, {col}) for matrix of size ({self.rows}, {self.cols})")
        if value == 0:
            self.data.pop((row, col), None)  # Remove zero elements
        else:
            self.data[(row, col)] = value

    def add(self, other):
        """
        Add two sparse matrices.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition")

        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)

        # Add elements from self
        for (row, col), value in self.data.items():
            result.set_element(row, col, value + other.get_element(row, col))

        # Add elements from other that are not in self
        for (row, col), value in other.data.items():
            if (row, col) not in self.data:
                result.set_element(row, col, value)

        return result

    def subtract(self, other):
        """
        Subtract the second matrix from the first.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction")

        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)

        # Subtract elements from self
        for (row, col), value in self.data.items():
            result.set_element(row, col, value - other.get_element(row, col))

        # Subtract elements from other that are not in self
        for (row, col), value in other.data.items():
            if (row, col) not in self.data:
                result.set_element(row, col, -value)

        return result

    def multiply(self, other):
        """
        Multiply two sparse matrices efficiently for large datasets.
        """
        if self.cols != other.rows:
            raise ValueError("Number of columns in the first matrix must match number of rows in the second matrix")

        result = SparseMatrix(num_rows=self.rows, num_cols=other.cols)

        # Preprocess the second matrix for column-wise access
        col_map = {}
        for (row2, col2), value2 in other.data.items():
            if col2 not in col_map:
                col_map[col2] = []
            col_map[col2].append((row2, value2))

        # Perform multiplication
        for (row1, col1), value1 in self.data.items():
            if col1 in col_map:
                for (row2, value2) in col_map[col1]:
                    current_value = result.get_element(row1, row2)
                    result.set_element(row1, row2, current_value + value1 * value2)

        return result

    def write_to_file(self, file_path):
        """
        Write the sparse matrix to a file in the specified format.
        """
        with open(file_path, 'w') as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n")
            for (row, col), value in self.data.items():
                file.write(f"({row}, {col}, {value})\n")


def main():
    try:
        # Get input file paths from the user
        file1 = input("Enter the path to the first matrix file: ")
        file2 = input("Enter the path to the second matrix file: ")

        # Load matrices from files
        matrix1 = SparseMatrix(file1)
        matrix2 = SparseMatrix(file2)

        # Get operation from the user
        operation = input("Enter the operation (add/subtract/multiply): ").strip().lower()

        # Perform the selected operation
        if operation == "add":
            result = matrix1.add(matrix2)
            output_file = "addition_result.txt"
        elif operation == "subtract":
            result = matrix1.subtract(matrix2)
            output_file = "subtraction_result.txt"
        elif operation == "multiply":
            result = matrix1.multiply(matrix2)
            output_file = "multiplication_result.txt"
        else:
            raise ValueError("Invalid operation. Please choose 'add', 'subtract', or 'multiply'.")

        # Write result to file
        result.write_to_file(output_file)
        print(f"Result written to {output_file}.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
