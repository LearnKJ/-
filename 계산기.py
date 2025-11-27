import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)

        self.expression = ""
        self.input_text = tk.StringVar()

        input_frame = self.create_display()
        input_frame.pack(side=tk.TOP)

        btns_frame = self.create_buttons()
        btns_frame.pack()

    def create_display(self):
        frame = tk.Frame(self.root, width=312, height=50, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        
        input_field = tk.Entry(frame, font=('arial', 18, 'bold'), textvariable=self.input_text, width=50, bg="#eee", bd=0, justify=tk.RIGHT)
        input_field.grid(row=0, column=0)
        input_field.pack(ipady=15)
        return frame

    def create_buttons(self):
        frame = tk.Frame(self.root, width=312, height=322.5, bg="grey")
        
        tk.Button(frame, text="C", fg="black", width=32, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: self.btn_clear()).grid(row=0, column=0, columnspan=3, padx=1, pady=1)
        tk.Button(frame, text="/", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                  command=lambda: self.btn_click("/")).grid(row=0, column=3, padx=1, pady=1)

        tk.Button(frame, text="7", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: self.btn_click(7)).grid(row=1, column=0, padx=1, pady=1)
        tk.Button(frame, text="8", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: self.btn_click(8)).grid(row=1, column=1, padx=1, pady=1)
        tk.Button(frame, text="9", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: self.btn_click(9)).grid(row=1, column=2, padx=1, pady=1)
        tk.Button(frame, text="*", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                  command=lambda: self.btn_click("*")).grid(row=1, column=3, padx=1, pady=1)

        tk.Button(frame, text="4", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: self.btn_click(4)).grid(row=2, column=0, padx=1, pady=1)
        tk.Button(frame, text="5", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: self.btn_click(5)).grid(row=2, column=1, padx=1, pady=1)
        tk.Button(frame, text="6", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: self.btn_click(6)).grid(row=2, column=2, padx=1, pady=1)
        tk.Button(frame, text="-", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                  command=lambda: self.btn_click("-")).grid(row=2, column=3, padx=1, pady=1)

        tk.Button(frame, text="1", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: self.btn_click(1)).grid(row=3, column=0, padx=1, pady=1)
        tk.Button(frame, text="2", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: self.btn_click(2)).grid(row=3, column=1, padx=1, pady=1)
        tk.Button(frame, text="3", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: self.btn_click(3)).grid(row=3, column=2, padx=1, pady=1)
        tk.Button(frame, text="+", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                  command=lambda: self.btn_click("+")).grid(row=3, column=3, padx=1, pady=1)

        tk.Button(frame, text="0", fg="black", width=21, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: self.btn_click(0)).grid(row=4, column=0, columnspan=2, padx=1, pady=1)
        tk.Button(frame, text=".", fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2",
                  command=lambda: self.btn_click(".")).grid(row=4, column=2, padx=1, pady=1)
        tk.Button(frame, text="=", fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2",
                  command=lambda: self.btn_equal()).grid(row=4, column=3, padx=1, pady=1)

        return frame

    def btn_click(self, item):
        self.expression = self.expression + str(item)
        self.input_text.set(self.expression)

    def btn_clear(self):
        self.expression = ""
        self.input_text.set("")

    def btn_equal(self):
        try:
            result = str(eval(self.expression)) 
            self.input_text.set(result)
            self.expression = result
        except ZeroDivisionError:
            self.input_text.set("Error")
            self.expression = ""
        except SyntaxError:
            self.input_text.set("Error")
            self.expression = ""

if __name__ == "__main__":
    win = tk.Tk()
    app = CalculatorApp(win)
    win.mainloop()
