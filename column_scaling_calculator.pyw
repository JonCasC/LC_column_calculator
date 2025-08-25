from tkinter import *
import math

class Calculator:
    def __init__(self):
        self.master = Tk()
        self.master.title("Column Scale Calculator")
        
        self.namelist = ['I.D.(mm)', 'Length (mm)', 'Inj. volume (uL)', 'Flow rate (mL/min)', 'Column vol (mL)']
        self.y_list = ['','Column 1', 'Column 2']
        self.entry_boxes = [[None]*5 for _ in range(2)]  # 2 columns, 5 fields each

        # Header row
        Label(self.master, text="").grid(column=0, row=0)
        for i, name in enumerate(self.namelist):
            Label(self.master, text=name).grid(column=i+1, row=0)

        # Entry rows
        for row in range(2):
            Label(self.master, text=f"Column {row+1}").grid(column=0, row=row+1)
            for col in range(5):
                entry = Entry(self.master)
                entry.grid(column=col+1, row=row+1, pady=2, padx=1)
                # Set Inj. volume, Flow rate, and Column vol of second column to light grey
                if row == 1 and col in [2, 3, 4]:
                    entry.configure({"background": "lightgrey"})
                elif col == 4:
                    entry.configure({"background": "lightgrey"})
                self.entry_boxes[row][col] = entry

        ok_button = Button(self.master, text = "OK", command=self.calculate, width=10)
        ok_button.grid(row = 4, column = 0, pady = 4, padx=5)
        self.scaling_label = Label(self.master, text=f"Scaling Factor:")
        self.scaling_label.grid(row = 4, column = 1)
        self.warnlabel = Label(self.master, text=(""))
        self.warnlabel.grid(row = 4, column = 4, columnspan=3, sticky = W)
        self.master.bind('<Return>', self.calculate)
        self.master.mainloop()
        
    def calculate(self, *args): 
        self.warnlabel.configure(text="")
        
        try:
            flowrate_1 = float(self.entry_boxes[0][3].get()) 
            diameter_1 = float(self.entry_boxes[0][0].get())
            diameter_2 = float(self.entry_boxes[1][0].get())
            length_1  = float(self.entry_boxes[0][1].get())
            length_2 = float(self.entry_boxes[1][1].get())
            injection_volume_1 = float(self.entry_boxes[0][2].get())
            
            
        except ValueError:
            self.warnlabel.configure(text="Please enter values!")
            return
        
        if 0 in [flowrate_1, diameter_2, diameter_1, injection_volume_1, length_1, length_2]:
            self.warnlabel.configure(text="Inputs must be non zero!")
            return
        
        scaling_factor = ((diameter_2**2)/(diameter_1**2))
        flowrate_2 =  flowrate_1 * scaling_factor
        injection_volume_2 = injection_volume_1 * scaling_factor * (length_2/length_1)
        scaling = round(scaling_factor,1)
        column_volume_1 = (diameter_1/2)**2 * math.pi * length_1 / 1000
        column_volume_2 = (diameter_2/2)**2 * math.pi * length_2 / 1000
        
        self.entry_boxes[0][4].delete(0, END)
        self.entry_boxes[0][4].insert(0, round(column_volume_1, 1))
        self.entry_boxes[1][4].delete(0, END)
        self.entry_boxes[1][4].insert(0, round(column_volume_2, 1))
        self.entry_boxes[1][2].delete(0, END)
        self.entry_boxes[1][2].insert(0, round(injection_volume_2, 1))
        self.entry_boxes[1][3].delete(0, END)
        self.entry_boxes[1][3].insert(0, round(flowrate_2, 1))
        
        self.scaling_label.configure(text=f"Scaling Factor: {scaling}")
        
        
if __name__ == "__main__":      
    calc = Calculator()