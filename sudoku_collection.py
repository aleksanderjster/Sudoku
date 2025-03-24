# Example of initializing a candidate matrix
# Each empty cell contains {1-9}, filled cells have an empty set
# sudoku_grid = [
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],

#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],

#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0]
#     ]

# sudoku resolved successfully
# sudoku_grid = [
#         [0, 0, 0,  2, 0, 0,  0, 4, 0],
#         [0, 8, 7,  0, 3, 0,  0, 0, 5],
#         [0, 6, 0,  1, 0, 0,  9, 0, 0],
        
#         [5, 0, 0,  9, 0, 0,  0, 0, 1],
#         [0, 0, 0,  0, 0, 0,  0, 0, 0],
#         [8, 0, 0,  0, 0, 3,  0, 0, 7],
        
#         [0, 0, 3,  0, 0, 5,  0, 8, 0],
#         [6, 0, 0,  0, 4, 0,  5, 2, 0],
#         [0, 4, 0,  0, 0, 6,  0, 0, 0]
#     ]

# sudoku resolved successfully
# sudoku_grid = [
#         [0, 0, 8,  3, 9, 0,  0, 4, 0],
#         [0, 0, 0,  7, 0, 0,  1, 6, 0],
#         [0, 0, 2,  1, 0, 0,  0, 0, 9],
        
#         [8, 1, 0,  0, 0, 0,  0, 0, 4],
#         [4, 0, 5,  0, 0, 0,  6, 0, 2],
#         [6, 0, 0,  0, 0, 0,  0, 7, 1],
        
#         [2, 0, 0,  0, 0, 7,  5, 0, 0],
#         [0, 7, 1,  0, 0, 8,  0, 0, 0],
#         [0, 4, 0,  0, 2, 3,  7, 0, 0]
#     ]

sudoku_grid = [
        [0, 0, 8,  0, 0, 0,  0, 3, 0],
        [0, 0, 0,  2, 4, 0,  1, 0, 0],
        [0, 0, 0,  0, 0, 6,  0, 8, 0],

        [4, 2, 0,  5, 0, 0,  0, 0, 0],
        [6, 0, 0,  9, 0, 2,  0, 7, 0],
        [0, 0, 0,  0, 3, 0,  8, 0, 0],

        [7, 4, 9,  0, 0, 0,  0, 0, 0],
        [0, 0, 0,  0, 0, 0,  7, 6, 0],
        [1, 0, 0,  0, 0, 0,  5, 0, 0]
    ]

last_resolved = [
    [0, 0, 8, 0, 0, 0, 0, 3, 0], 
    [3, 0, 0, 2, 4, 8, 1, 0, 0], 
    [0, 1, 4, 3, 0, 6, 0, 8, 0], 
    [4, 2, 0, 5, 8, 7, 0, 0, 0], 
    [6, 8, 0, 9, 1, 2, 0, 7, 0], 
    [0, 0, 0, 6, 3, 4, 8, 0, 0], 
    [7, 4, 9, 0, 6, 5, 0, 0, 0], 
    [8, 0, 0, 4, 0, 0, 7, 6, 0], 
    [1, 0, 0, 0, 0, 0, 5, 4, 0]
    ]

# last_resolved_candidates = [
#     [{2, 5, 9}, {5, 6, 7, 9}, set(), {1, 7}, {5, 7, 9}, {1, 9}, {2, 4, 6, 9}, set(), {2, 4, 5, 6, 7}],
#     [set(), {5, 6, 7, 9}, {5, 6, 7}, set(), set(), set(), set(), {5, 9}, {5, 6, 7}],
#     [{2, 5, 9}, set(), set(), set(), {5, 7, 9}, set(), {2, 9}, set(), {2, 5, 7}],
#     [set(), set(), {1, 3}, set(), set(), set(), {3, 6, 9}, {1, 9}, {1, 3, 6}],
#     [set(), set(), {3, 5}, set(), set(), set(), {3, 4}, set(), {3, 4, 5}],
#     [{5, 9}, {5, 7, 9}, {1, 5, 7}, set(), set(), set(), set(), {1, 2, 5}, {1, 2, 5}],
#     [set(), set(), set(), {1, 8}, set(), set(), {2, 3}, {1, 2}, {1, 2, 3, 8}],
#     [set(), {3, 5}, {2, 5}, set(), {2, 9}, {1, 3, 9}, set(), set(), {1, 2, 3, 9}],
#     [set(), {3, 6}, {2, 6}, {7, 8}, {2, 7, 9}, {3, 9}, set(), set(), {2, 3, 8, 9}]
# ]

last_resolved_candidates = [
    [{2, 5, 9}, {5, 6, 7, 9}, set(), {1, 7}, {5, 7, 9}, {1, 9}, {2, 4, 6, 9}, set(), {2, 4, 5, 6, 7}], 
    [set(), {5, 6, 7, 9}, {5, 6, 7}, set(), set(), set(), set(), {5, 9}, {5, 6, 7}], 
    [{2, 5, 9}, set(), set(), set(), {5, 7, 9}, set(), {2, 9}, set(), {2, 5, 7}], 
    [set(), set(), {1, 3}, set(), set(), set(), {3, 6, 9}, {1, 9}, {1, 3, 6}], 
    [set(), set(), {3, 5}, set(), set(), set(), {3, 4}, set(), {3, 4, 5}], 
    [{5, 9}, {5, 7, 9}, {1, 5, 7}, set(), set(), set(), set(), {1, 2, 5}, {1, 2, 5}], 
    [set(), set(), set(), {1, 8}, set(), set(), {2, 3}, {1, 2}, {1, 2, 3, 8}], 
    [set(), {3, 5}, {2, 5}, set(), {2, 9}, {1, 3, 9}, set(), set(), {1, 9}], 
    [set(), {3, 6}, {2, 6}, {7, 8}, {2, 7, 9}, {3, 9}, set(), set(), {8, 9}]
]

# # most hardest sudoku
# sudoku_grid = [
#         [8, 0, 0,  0, 0, 0,  0, 0, 0],
#         [0, 0, 3,  6, 0, 0,  0, 0, 0],
#         [0, 7, 0,  0, 9, 0,  2, 0, 0],

#         [0, 5, 0,  0, 0, 7,  0, 0, 0],
#         [0, 0, 0,  0, 4, 5,  7, 0, 0],
#         [0, 0, 0,  1, 0, 0,  0, 3, 0],

#         [0, 0, 1,  0, 0, 0,  0, 6, 8],
#         [0, 0, 8,  5, 0, 0,  0, 1, 0],
#         [0, 9, 0,  0, 0, 0,  4, 0, 0]
#     ]