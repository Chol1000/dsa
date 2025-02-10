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
        Read a sparse matrix from a file.
        File format:
        rows=<number_of_rows>
        cols=<number_of_columns>
        (row1, col1, value1)
        (row2, col2, value2)
        ...
        """
        with open(file_path, 'r') as file:
            lines = file.readlines()

        rows_read = False
        cols_read = False

        for line in lines:
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
                    value = int(parts[2])
                except ValueError:
                    raise ValueError("Input file contains non-integer values")

                if row >= self.rows or col >= self.cols:
                    raise ValueError("Row or column index out of bounds")

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
            raise ValueError("Row or column index out of bounds")
        return self.data.get((row, col), 0)

    def set_element(self, row, col, value):
        """
        Set the value at (row, col).
        """
        if row >= self.rows or col >= self.cols:
            raise ValueError("Row or column index out of bounds")
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
        Multiply two sparse matrices.
        """
        if self.cols != other.rows:
            raise ValueError("Number of columns in the first matrix must match number of rows in the second matrix")

        result = SparseMatrix(num_rows=self.rows, num_cols=other.cols)

        for (row1, col1), value1 in self.data.items():
            for (row2, col2), value2 in other.data.items():
                if col1 == row2:
                    # Accumulate the product in the result matrix
                    current_value = result.get_element(row1, col2)
                    result.set_element(row1, col2, current_value + value1 * value2)

        return result

    def __str__(self):
        """
        String representation of the sparse matrix.
        """
        matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for (row, col), value in self.data.items():
            matrix[row][col] = value
        return "\n".join(" ".join(map(str, row)) for row in matrix)


def main():
    try:
        # Load matrices from files
        matrix1 = SparseMatrix("matrix1.txt")
        matrix2 = SparseMatrix("matrix2.txt")

        # Perform operations
        addition_result = matrix1.add(matrix2)
        subtraction_result = matrix1.subtract(matrix2)
        multiplication_result = matrix1.multiply(matrix2)

        # Print results
        print("Addition Result:")
        print(addition_result)

        print("\nSubtraction Result:")
        print(subtraction_result)

        print("\nMultiplication Result:")
        print(multiplication_result)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
