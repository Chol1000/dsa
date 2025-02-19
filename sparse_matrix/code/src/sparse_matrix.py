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
        try:
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
                        # Skip out-of-bounds elements
                        if row >= self.rows or col >= self.cols:
                            print(f"Skipping out-of-bounds element: ({row}, {col}) with value {value}")
                            continue
                        self.data[(row, col)] = value
                    else:
                        raise ValueError("Input file has wrong format")
            if not rows_read or not cols_read:
                raise ValueError("Input file missing rows or cols")
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Error reading the input file: {e}")

    def get_element(self, row, col):
        """
        Get the value at (row, col).
        Returns 0 if the element is not in the sparse matrix.
        """
        if row >= self.rows or col >= self.cols:
            print(f"Skipping out-of-bounds request for element: ({row}, {col})")
            return 0
        return self.data.get((row, col), 0)

    def set_element(self, row, col, value):
        """
        Set the value at (row, col).
        """
        if row >= self.rows or col >= self.cols:
            print(f"Skipping out-of-bounds request to set element: ({row}, {col})")
            return
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
        all_keys = set(self.data.keys()).union(other.data.keys())
        for key in all_keys:
            result.set_element(key[0], key[1], self.get_element(*key) + other.get_element(*key))
        return result

    def subtract(self, other):
        """
        Subtract the second matrix from the first.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction")
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        all_keys = set(self.data.keys()).union(other.data.keys())
        for key in all_keys:
            result.set_element(key[0], key[1], self.get_element(*key) - other.get_element(*key))
        return result

    def multiply(self, other):
        """
        Multiply two sparse matrices efficiently for large datasets.
        """
        if self.cols != other.rows:
            raise ValueError("Number of columns in the first matrix must match number of rows in the second matrix")
        result = SparseMatrix(num_rows=self.rows, num_cols=other.cols)
        col_map = {}
        for (row2, col2), value2 in other.data.items():
            if col2 not in col_map:
                col_map[col2] = []
            col_map[col2].append((row2, value2))
        for (row1, col1), value1 in self.data.items():
            if col1 in col_map:
                for (row2, value2) in col_map[col1]:
                    result.set_element(row1, row2, result.get_element(row1, row2) + value1 * value2)
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
        # Define the path to the sample input files in the sample_inputs folder
        sample_input_dir = '/dsa/sparse_matrix/sample_inputs/'
        output_dir = '/dsa/output/'  # Output directory path
        matrices = ['matrix1.txt', 'matrix2.txt']
        while True:
            print("\nAvailable matrices:")
            for i, matrix in enumerate(matrices, 1):
                print(f"{i}. {matrix}")
            print(f"{len(matrices) + 1}. Exit")
            matrix_choice1 = int(input("Choose the first matrix (Enter the number): "))
            if matrix_choice1 == len(matrices) + 1:
                print("Exiting...")
                break
            file1 = matrices[matrix_choice1 - 1]
            matrix_choice2 = int(input("Choose the second matrix (Enter the number): "))
            if matrix_choice2 == len(matrices) + 1:
                print("Exiting...")
                break
            file2 = matrices[matrix_choice2 - 1]
            matrix1 = SparseMatrix(sample_input_dir + file1)
            matrix2 = SparseMatrix(sample_input_dir + file2)
            print("\nAvailable operations:")
            print("1. Add")
            print("2. Subtract")
            print("3. Multiply")
            print("4. Exit")
            operation_choice = int(input("Choose an operation (1/2/3/4): ").strip())
            if operation_choice == 1:
                result = matrix1.add(matrix2)
                output_file = output_dir + "addition_result.txt"
            elif operation_choice == 2:
                result = matrix1.subtract(matrix2)
                output_file = output_dir + "subtraction_result.txt"
            elif operation_choice == 3:
                result = matrix1.multiply(matrix2)
                output_file = output_dir + "multiplication_result.txt"
            elif operation_choice == 4:
                print("Exiting...")
                break
            else:
                print("Invalid operation. Please choose 1, 2, 3, or 4.")
                continue
            result.write_to_file(output_file)
            print(f"Result written to {output_file}.\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
