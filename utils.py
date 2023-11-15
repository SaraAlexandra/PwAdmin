
from tkinter import *

class Table:
    def __init__(self, root, alllPws, listOfWidths):
        # code for creating table
        for i in range(len(alllPws)):
            for j in range(4):
                self.e = Entry(root, width=listOfWidths[j], fg='black',
                               font=('Arial', 14, 'bold'))
                 
                self.e.grid(row=i, column=j)
                self.e.insert(END, alllPws[i][j])


  
