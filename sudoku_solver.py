import time
from typing import List, Tuple
from math import sqrt


user_mode = False


class Solver:

    def __init__(self, file_path: str='') -> None:
        
        self.file_path = file_path
        self.board_rows = 9
        self.board_cols = 9
        self.sudoku_table = [0] * self.board_rows
        self.read_table(self.file_path)
        

    def read_table(self, file_path: str) -> None:

        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for i in range(len(lines)):
                    self.sudoku_table[i] = [int(num) for num in lines[i].rstrip('\n').split(',')]
        except (FileNotFoundError, PermissionError, OSError):
            print("Error opening file")


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

    def find_next_empty(self) -> None | Tuple[int, int]:
        
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.sudoku_table[row][col]  == 0:
                    return (row, col)
                
        return None
    
    def is_valid_number(self, position: Tuple[int, int], number: int) -> bool:

        square_size = int(sqrt(self.board_rows))

        row_idx, col_idx = position

        if number in self.sudoku_table[row_idx]:
            return False
        
        col_numbers = [row[col_idx] for row in self.sudoku_table]

        if number in col_numbers:
            return False
        
        square_x_idx = row_idx // square_size
        square_y_idx = col_idx // square_size

        # print(square_x_idx, square_y_idx)

        square_nums = []
        for row in range(square_x_idx*square_size, square_x_idx*square_size +square_size):
            for col in range(square_y_idx*square_size, square_y_idx*square_size +square_size):
                square_nums.append(self.sudoku_table[row][col])

        if number in square_nums:
            return False
        
        return True

        
        # print(self.sudoku_table[row_idx][col_idx])

        



            
        




if __name__ == '__main__':
    
    path = 'sudoku_input_file.txt'

    solver = Solver(file_path=path)
    # print(solver.sudoku_table)
    # solver.print_table()
    # print(solver.find_next_empty())
    print(solver.is_valid_number((2,4), 3))
