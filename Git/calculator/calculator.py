from tkinter import *

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        # Display
        self.display = Entry(root, font=('Arial', 20), justify='right', bd=5)
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        
        # Button layout
        self.create_buttons()
        
        # Configure grid weights
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
    
    def create_buttons(self):
        # Button texts
        button_list = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        # Create and place buttons
        row = 1
        col = 0
        for button_text in button_list:
            button = Button(self.root, text=button_text, font=('Arial', 15),
                          command=lambda x=button_text: self.button_click(x))
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Clear and Delete buttons
        clear_button = Button(self.root, text='C', font=('Arial', 15),
                            command=self.clear_display)
        clear_button.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky="nsew")
        
        delete_button = Button(self.root, text='⌫', font=('Arial', 15),
                             command=self.delete_last_char)
        delete_button.grid(row=5, column=2, columnspan=2, padx=2, pady=2, sticky="nsew")
    
    def button_click(self, value):
        if value == '=':
            try:
                result = eval(self.display.get())
                self.display.delete(0, END)
                self.display.insert(END, str(result))
            except:
                self.display.delete(0, END)
                self.display.insert(END, "Error")
        else:
            self.display.insert(END, value)
    
    def clear_display(self):
        self.display.delete(0, END)
        
    def delete_last_char(self):
        current = self.display.get()
        self.display.delete(0, END)
        self.display.insert(0, current[:-1])

if __name__ == "__main__":
    root = Tk()
    calculator = Calculator(root)
    root.mainloop()