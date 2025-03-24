import copy

# clean posibilities by row for defined numbers
def p_row_clean(val, row, p_mtrx):
# emoves val from opportunity matrix by rows
    
    for j in range(9):
        p_values = p_mtrx[row][j]
        if val in p_values:
            p_values.remove(val)
            flag = True

    return p_mtrx

# clean posibilities by column for defined numbers
def p_col_clean(val, col, p_mtrx):
# removes val from opportunity matrix by columns

    for i in range(9):
        p_values = p_mtrx[i][col]
        if val in p_values:
            p_values.remove(val)
            flag = True

    return p_mtrx

# clean posibilities by sections for defined numbers
def p_cell_clean(val, row, col, p_mtrx):
# removes opportunity values from ocupied cells
    rr = 3* int(row / 3)
    cc = 3* int(col / 3)
    for i in range(3):
        
        for j in range(3):
            p_values = p_mtrx[rr + i][cc + j]
            
            if val in p_values:
                p_values.remove(val)
                flag = True
            
    return p_mtrx

# clean the possibility values from possibility matrix for defined numbers
def p_clean(s_mtrx, p_mtrx):


    for i in range(9):      
        for j in range(9):
            val = s_mtrx[i][j]

            # removes opportunities due cell is ocupied
            if val > 0:
                p_mtrx[i][j] = []
                
            # remove val from corresponding row
            p_mtrx = p_row_clean(val, i, p_mtrx)

            # remove val from corresponding col
            p_mtrx = p_col_clean(val, j, p_mtrx)

            # remove val from corresponding cell
            p_mtrx = p_cell_clean(val, i, j, p_mtrx)

    return p_mtrx




# find clear singles in columns and update matrixes
def p_find_singles_by_columns(p_mtrx, cur_mtrx):

    flag = False

    for j in range(9):

        for k in range(1, 10):
            counter = 0
            pos_x = -1
            pos_y = -1
            
            # checks k for every oportunities in column
            for i in range(9):
                p_values = p_mtrx[i][j]
                if k in p_values:
                    counter += 1
                    #print(f'{k} is in {i}, {j} - counter: {counter}')
                    if counter <= 1:
                        pos_x = i
                        pos_y = j
                    else:                   # resets address if counter greater than 1
                        #pos_y = -1
                        #pos_x = -1
                        #print (f'counter exceed 1 and resets')
                        counter = 0
                        break

            if counter == 1:
                print(f'found column clear single {k} in column: {pos_y + 1} in row: {pos_x + 1}')
                cur_mtrx[pos_x][pos_y] = k  # writes clear single in row into solution
                p_mtrx[pos_x][pos_y] = []   # clears opportunities for this position
                flag = True
    return flag


# find clear singles in rows and update matrixes
def p_find_singles_by_rows (p_mtrx, cur_mtrx):

    flag = False
    for i in range(9):

        for k in range(1, 10):
            counter = 0
            pos_x = -1
            pos_y = -1
            
            # checks k for every oportunities in row
            for j in range(9):
                p_values = p_mtrx[i][j]
                if k in p_values:
                    counter += 1
                    #print(f'{k} is in {i}, {j} - counter: {counter}')
                    if counter <= 1:
                        pos_x = i
                        pos_y = j
                    else:                   # resets address if counter greater than 1
                        #pos_y = -1
                        #pos_x = -1
                        #print (f'counter exceed 1 and resets')
                        counter = 0
                        break

            if counter == 1:
                print(f'found row clear single {k} in row: {pos_x + 1} in column: {pos_y + 1}')
                cur_mtrx[pos_x][pos_y] = k  # writes clear single in row into solution
                p_mtrx[pos_x][pos_y] = []   # clears opportunities for this position
                flag = True

    return flag

# calls finding clear singles for rows and columns in cycle
def p_find_singles(p_mtrx, cur_mtrx):

    while True:
        
        # check for clear row singles until not found
        status_1 = p_find_singles_by_rows(p_mtrx, cur_mtrx)
        if status_1:  p_clean(cur_mtrx, p_mtrx)
        
        # check for clear column singles until not found
        status_2 = p_find_singles_by_columns(p_mtrx, cur_mtrx)
        if status_2: p_clean(cur_mtrx, p_mtrx)

        # Exit point is no singles found as for rows as for columns
        if status_1 == False and status_2 == False:
            print(f'INFO: no more singles found!')
            break
    




# clean posibilities for row and column like opportunities
# looks by sections for opportunities in one row or column
# removes opportunities in other sections  in row/ column as they are ocupied
def p_strike_out_by_row(p_mtrx):
    # take possibility number

    flag = False
    for k in range(1, 10):

    # check numbers are met in section
        for sec_x in range(3):          # section x coordinate

            for sec_y in range(3):      # section y coordinate
                #print(f'===== {k} in Section {sec_x},{sec_y} opprtunities ======')
                rows = []
                cols = []

                for i in range(3):      # row index in section
                    
                    for j in range(3):  # column index in section
                        p_values = p_mtrx[sec_x * 3 + i][sec_y * 3 + j]

                        # value met in section position among opportunities
                        if k in p_values:
                            rows.append(sec_x * 3 + i)
                            cols.append(sec_y * 3 + j)
                            #print(f'found {k} in row {sec_x * 3 + i + 1}')

                # check if they are row like
                # verification that all rows are equal
                if len(rows) != 0:    
                    status = rows.count(rows[0]) % len(rows)
                    if status == 0:
                        r = rows[0]                        

                        # remove possibilities from same row in other sections
                        for c in range(9):
                            p_values = p_mtrx[r][c]
                            if c not in cols:
                                if k in p_values:
                                    p_values.remove(k)
                                    flag = True

                    if flag == True:
                        print(f'Found clear row oportunities for {k} in row {r + 1}')

    return flag

def p_strike_out_by_column(p_mtrx):
    # take possibility number
    # check numbers met in section
    # check if they are column like
    # remove possibilities from same column in other sections

    # take possibility number

    flag = False
    for k in range(1, 10):

    # check numbers are met in section
        for sec_x in range(3):          # section x coordinate

            for sec_y in range(3):      # section y coordinate
                #print(f'===== {k} in Section {sec_x},{sec_y} opprtunities ======')
                rows = []
                cols = []

                for j in range(3):      # col index in section
                    
                    for i in range(3):  # row index in section
                        p_values = p_mtrx[sec_x * 3 + i][sec_y * 3 + j]

                        # value met in section position among opportunities
                        if k in p_values:
                            rows.append(sec_x * 3 + i)
                            cols.append(sec_y * 3 + j)
                            #print(f'found {k} in col {sec_y * 3 + j + 1}')

                # check if they are row like
                # verification that all rows are equal
                if len(cols) != 0:    
                    status = cols.count(cols[0]) % len(cols)
                    if status == 0:
                        c = cols[0]
                        
                        # remove possibilities from same row in other sections
                        for r in range(9):
                            p_values = p_mtrx[r][c]
                            if r not in rows:
                                if k in p_values:
                                    p_values.remove(k)
                                    flag = True

                    if flag == True:
                        print(f'Found clear column oportunities for {k} in col {c + 1}')

    return flag

def p_strike_out(p_mtrx):
    status = False          # reflects if any opportunities where removed

    while True:
    
        status_1 = p_strike_out_by_row(p_mtrx)
        status_2 = p_strike_out_by_column(p_mtrx)

        if status_1 == False and status_2 == False: 
            break
        else:
            status = True
    
    return status

# prints 3D matrix as list of list. 
def print_3D_mtrx(mtrx):
    for i in range(9):
        print(f'=========== row {i} ============')
        for j in range(9):
            print(mtrx[i][j])


# prints 2D matrix as table.
def print_2D_mtrx(mtrx):
    str = ''
    for i in range(9):       
        for j in range(9):
            if mtrx[i][j] == 0:
                str = str + f'_ '
            else:
                str = str + f'{mtrx[i][j]} '
        print(str)
        str = ''

# prints 2D matrix as table.
def print_sudoku(mtrx):
    str = ''
    for i in range(9):       
        for j in range(9):
            if mtrx[i][j] == 0:
                str = str + f'_ '
            else:
                str = str + f'{mtrx[i][j]} '
            if j == 2 or j == 5:
                str = str + f'|| '
            else:
                str = str + f' '
        if i == 3 or i == 6:
            print(f'=============================')
        print(str)
        str = ''


# initiate matrixes
def sudoku_init():
    # set new sudoku matrix to solve
    # sudoku = [
    #     [2, 1, 0, 0, 6, 0, 0, 0, 0],
    #     [0, 0, 0, 5, 0, 0, 0, 0, 6],
    #     [0, 0, 0, 0, 8, 4, 0, 5, 0],
    #     [0, 0, 2, 0, 0, 6, 9, 4, 0],
    #     [0, 0, 0, 1, 0, 3, 0, 0, 0],
    #     [0, 9, 8, 4, 0, 0, 1, 0, 0],
    #     [0, 3, 0, 9, 1, 0, 0, 0, 0],
    #     [6, 0, 0, 0, 0, 5, 0, 0, 0],
    #     [0, 0, 0, 0, 3, 0, 0, 1, 7]
    #     ]
    # sudoku = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0]
    #     ]

    sudoku = [
        [0, 0, 0, 2, 0, 0, 0, 4, 0],
        [0, 8, 7, 0, 3, 0, 0, 0, 5],
        [0, 6, 0, 1, 0, 0, 9, 0, 0],
        [5, 0, 0, 9, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 3, 0, 0, 7],
        [0, 0, 3, 0, 0, 5, 0, 8, 0],
        [6, 0, 0, 0, 4, 0, 5, 2, 0],
        [0, 4, 0, 0, 0, 6, 0, 0, 0]
        ]
    
    solved_sudoku = [
        [2, 1, 5, 3, 6, 9, 4, 7, 8],
        [8, 4, 3, 5, 7, 1, 2, 9, 6],
        [7, 6, 9, 2, 8, 4, 3, 5, 1],
        [1, 7, 2, 8, 5, 6, 9, 4, 3],
        [4, 5, 6, 1, 9, 3, 7, 8, 2],
        [3, 9, 8, 4, 2, 7, 1, 6, 5],
        [5, 3, 7, 9, 1, 8, 6, 2, 4],
        [6, 2, 1, 7, 4, 5, 8, 3, 9],
        [9, 8, 4, 6, 3, 2, 5, 1, 7]
        ]
    return sudoku, solved_sudoku


def main():
    # initiation of the sudoku
    sudoku, solved_sudoku = sudoku_init()

    # makes working version of the initial sudoku.    
    sudoku_current = copy.deepcopy(sudoku)

    # creation of initial opportunities matrix
    p_matrix = [[[1, 2, 3, 4, 5, 6, 7, 8, 9] for _ in range(9)] for _ in range(9)]


    print_sudoku(sudoku_current)
    print("\n============= Solution ====================")


    # main solving engine
    p_matrix = p_clean(sudoku_current, p_matrix)
    while True:
        p_find_singles(p_matrix, sudoku_current)
        if p_strike_out(p_matrix) == False: break



    print("\n============= Solution Result====================")
    print_sudoku(sudoku_current)

    print("\n======== Opportunities ===============")
    print_3D_mtrx(p_matrix)
    

        

if __name__ == '__main__': 
    main()
