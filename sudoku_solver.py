import time
from typing import List, Tuple
from math import sqrt


user_mode = False


class Solver:

    def __init__(self, read_file_path: str='', save_file_path: str='') -> None:


        # Initializing the variables used for 9x9 board
        self.read_file_path = read_file_path
        self.save_file_path = save_file_path
        self.board_rows = 9
        self.board_cols = 9
        self.sudoku_table = [0] * self.board_rows
        self.read_table()
        

    # Reading a board from txt file, each line is a row, 0s are empty spaces
    def read_table(self) -> None:

        try:
            with open(self.read_file_path, 'r') as f:
                lines = f.readlines()
                for i in range(len(lines)):
                    self.sudoku_table[i] = [int(num) for num in lines[i].rstrip('\n').split(',')]
        except (FileNotFoundError, PermissionError, OSError):
            print("Error opening file")


    # Helper function to save the answer to txt file
    def save_answer(self) -> None:

        with open(self.save_file_path, 'w') as f:
            for row in range(self.board_rows):
                f.write(','.join(map(str, self.sudoku_table[row])))
                f.write('\n')
        

    # Helper function for 'nicer' printing of the table
    def print_table(self) -> None:
        print()
        for i in range(self.board_rows):
            line = ''
            for j in range(self.board_cols):
                line += str(self.sudoku_table[i][j])
                if (j+1) % 3 == 0:
                    line += '    '
            print(line)
            line = ''
            if (i+1) % 3 == 0:
                print('\n')

    # Function that finds the next empty space on board
    def find_next_empty(self) -> None | Tuple[int, int]:
        
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.sudoku_table[row][col]  == 0:
                    return (row, col)
                
        return None
    

    # Function to check whether the number we'd like to put in the board is correct
    def is_valid_number(self, position: Tuple[int, int], number: int) -> bool:

        square_size = int(sqrt(self.board_rows))

        row_idx, col_idx = position

        # We check for the same number in row
        if number in self.sudoku_table[row_idx]:
            return False
        
        col_numbers = [row[col_idx] for row in self.sudoku_table]

        # We check for the same number in column
        if number in col_numbers:
            return False
        
        # Then we calculate the square position we are currently in
        square_x_idx = row_idx // square_size
        square_y_idx = col_idx // square_size


        square_nums = []
        # Adding numbers in the square to the square list
        for row in range(square_x_idx*square_size, square_x_idx*square_size +square_size):
            for col in range(square_y_idx*square_size, square_y_idx*square_size +square_size):
                square_nums.append(self.sudoku_table[row][col])

        # Check for the same number in the square
        if number in square_nums:
            return False
        
        return True



    def solve(self) -> bool:

        # Finding next empty spot position
        next_empty = self.find_next_empty()

        # If the function returns None, then the board is full and we can stop
        if not next_empty:
            return True
        
        row, col = next_empty

        # Try to insert every number in current spot
        for i in range(1,10):

            # If it's a valid place, then insert into the board
            if self.is_valid_number(position=(row, col), number=i):
                self.sudoku_table[row][col] = i

                # Continue solving board with recurring calls of solve
                if self.solve():
                    return True
                
        # If we're here it means that we should backtrack, so reset the current cell and return False so we can continue previous call 
        self.sudoku_table[row][col] = 0
        return False
                


if __name__ == '__main__':
    
    read_path = 'sudoku_input_file.txt'
    save_path = 'sudoku_output_file.txt'

    solver = Solver(read_file_path=read_path, save_file_path=save_path)

    start = time.time()
    solver.solve()
    end = time.time()
    print(f'Solving took: {end-start:3f}s')
    # solver.print_table()
    solver.save_answer()
