'''
Sequence Online -- data.py: Stores all data 

Author: Pratiksha Jain

'''

rooms = {}

places = [
        ['0-0', 'S-2', 'S-3', 'S-4', 'S-5', 'S-6', 'S-7', 'S-8', 'S-9', '0-0'], 
        ['C-6', 'C-5', 'C-4', 'C-3', 'C-2', 'H-1', 'H-13', 'H-12', 'H-10', 'S-10'],
        ['C-7', 'S-1', 'D-2', 'D-3', 'D-4', 'D-5', 'D-6', 'D-7', 'H-9', 'S-12'],
        ['C-8', 'S-13', 'C-6', 'C-5', 'C-4', 'C-3', 'C-2', 'D-8', 'H-8', 'S-13'],
        ['C-9', 'S-12', 'C-7', 'H-6', 'H-5', 'H-4', 'H-1', 'D-9', 'H-7', 'S-1'],
        ['C-10', 'S-10', 'C-8', 'H-7', 'H-2', 'H-3', 'H-13', 'D-10', 'H-6', 'D-2'], 
        ['C-12', 'S-9', 'C-9', 'H-8', 'H-9', 'H-10', 'H-12', 'D-12', 'H-5', 'D-3'],
        ['C-13', 'S-8', 'C-10', 'C-12', 'C-13', 'C-1', 'D-1', 'D-13', 'H-4', 'D-4'],
        ['C-1', 'S-7', 'S-6', 'S-5', 'S-4', 'S-3', 'S-2', 'H-2', 'H-3', 'D-5'],
        ['0-0', 'D-1', 'D-13', 'D-12', 'D-10', 'D-9', 'D-8', 'D-7', 'D-6', '0-0'] 

        ]

status_dict = {
            -1: "Game Over!",
            0: "Accepted",
            1:"One eyed joker trying to remove fixed card",
            2:"no wildcard, Wrong card or location entered",
            3:"space not empty - cannot place card there",
            4:"wildcard(1) used incorrectly: no card present there",
            5:"Not present in cards",
            6: "Not your turn yet",
            7: "Sequence Detected!"
        }
