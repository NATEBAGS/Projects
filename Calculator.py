#Nathaniel Bagchee
from tkinter import *
from calculator import calculate

def calculator(gui):
    '''This is what creats the calculator interface'''
    # gui window
    gui.title("Calculator")
    # entry text box
    entrybox = Entry(gui, width=36, borderwidth=5)
    # position the entry text box
    entrybox.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    # create buttons
    b0 = addButton(gui, entrybox, '0')
    b1 = addButton(gui, entrybox, '1')
    b2 = addButton(gui, entrybox, '2')
    b3 = addButton(gui, entrybox, '3')
    b4 = addButton(gui, entrybox, '4')
    b5 = addButton(gui, entrybox, '5')
    b6 = addButton(gui, entrybox, '6')
    b7 = addButton(gui, entrybox, '7')
    b8 = addButton(gui, entrybox, '8')
    b9 = addButton(gui, entrybox, '9')
    b_add = addButton(gui, entrybox, '+')
    b_sub = addButton(gui, entrybox, '-')
    b_mult = addButton(gui, entrybox, '*')
    b_div = addButton(gui, entrybox, '/')
    b_clr = addButton(gui, entrybox, 'c')
    b_eq = addButton(gui, entrybox, '=')

    # add buttons
    buttons = [b7, b8, b9, b_clr,
               b4, b5, b6, b_sub,
               b1, b2, b3, b_add,
               b_mult, b0, b_div, b_eq]
    k = 4
    #Intitializing the interior design of the GUIA
    for i in range(k):
        for j in range(k):
            buttons[i * k + j].grid(row=i + 1, column=j, columnspan=1)


def addButton(gui, entrybox, value):
    '''Adds the buttons to the interface'''
    return Button(gui, text=value, height=4, width=9, command=lambda: clickButton(entrybox, value))

#Function to handle what happens after button is clicked
def clickButton(entrybox, value):
    '''This is the function that activates the calculator'''
    if value == 'c':
        # clears it
        entrybox.delete(0, END)
    elif value == '=':
        # Outputs the calculation
        expression = entrybox.get()
        result = calculate(expression)
        # clear and display the result
        entrybox.delete(0, END)
        entrybox.insert(0, result)
    else:
        # append the button value
        entrybox.insert(END, value)

# main program
# create the main window
gui = Tk()
# create the calculator layout
calculator(gui)
# update the window
gui.mainloop()
