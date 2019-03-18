# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:38:55 2019

@author: sonerk
"""

import sys


def print_out(a):
    sys.stdout.write(str(a))

grid_size = 4

board = [[0,0,0,0],[4,0,0,0],[0,0,0,2],[0,3,0,0]]

def print_board(board):

    if not board:
        print_out("There is no solution.")
        return
    for i in range(grid_size):
        for j in range(grid_size):
            
            cell = board[i][j]
            if cell == 0 or isinstance(cell, set):
                print_out('.')
            else:
                print_out(cell)
            if (j + 1) % 2 == 0 and j < 2:
                print_out(' |')

            if j != 3:
                print_out(' ')
        print_out('\n')
        if (i + 1) % 2 == 0 and i < 2:
            print_out("- - - - -  \n")

def monitor_board(board):
    
    state = list(board)
    
    for i in range(grid_size):
        for j in range(grid_size):
            
            cell = state[i][j]
            
            if cell == 0:
                
                state[i][j] = set(range(1,5))

    return state




def check_goalstate(state):
    for row in state:
        for cell in row:
            if isinstance(cell, set):
                return False
    return True


def step(state):

    new_units = False
    for i in range(grid_size):
        
        row = state[i]
        values = set([x for x in row if not isinstance(x, set)])
        
        for j in range(grid_size):
            
            if isinstance(state[i][j], set):
                
                state[i][j] -= values
                if len(state[i][j]) == 1:
                    
                    val = state[i][j].pop()
                    state[i][j] = val
                    values.add(val)
                    new_units = True
                    
                elif len(state[i][j]) == 0:
                    
                    return False, None

    for j in range(grid_size):
        
        column = [state[x][j] for x in range(grid_size)]
        values = set([x for x in column if not isinstance(x, set)])
        for i in range(grid_size):
            
            if isinstance(state[i][j], set):
                
                state[i][j] -= values
                if len(state[i][j]) == 1:
                    
                    val = state[i][j].pop() #### STACK_WISE
                    state[i][j] = val
                    values.add(val)
                    new_units = True
                    
                elif len(state[i][j]) == 0:
                    
                    return False, None

    for x in range(2):
        for y in range(2):
            
            values = set()
            for i in range(2 * x, 2 * x + 2):
                for j in range(2 * y, 2 * y + 2):
                    
                    cell = state[i][j]
                    if not isinstance(cell, set):
                        values.add(cell)
                        
            for i in range(2 * x, 2 * x + 2):
                for j in range(2 * y, 2 * y + 2):
                    
                    if isinstance(state[i][j], set):
                        
                        state[i][j] -= values
                             
                        if len(state[i][j]) == 1:
                            
                            val = state[i][j].pop()
                            state[i][j] = val
                            values.add(val)
                            new_units = True
                            
                        elif len(state[i][j]) == 0:
                            
                            return False, None

    return True, new_units

def distribute(state):

    while True:
        solvable, new_unit = step(state)
        if not solvable:
            return False
        if not new_unit:
            return True


def solver(state):
    solvable = distribute(state)

    if not solvable:
        return None

    if check_goalstate(state):
        return state

    for i in range(grid_size):
        for j in range(grid_size):
            
            cell = state[i][j]
            
            if isinstance(cell, set):
                
                for value in cell:
                    
                    new_state = list(state)
                    new_state[i][j] = value
                    solved = solver(new_state) # Recursion
                    if solved is not None:
                        
                        return solved
                return None
print('Initial State starts from [0,0] point \n')
print_board(board)
print('\n')			
state = monitor_board(board)
print('Goal State (Solved State) \n')
print_board(solver(state))
