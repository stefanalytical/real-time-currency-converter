import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk

# This class gets the exchange rate and returns the converted amount
class RealTimeCurrencyConverter():
    def __init__(self,url):
            self.data = requests.get(url).json()
            self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        if from_currency != 'USD' : 
            amount = amount / self.currencies[from_currency] 
  
        # Limit to 4 decimal places 
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

# This class creates an interface using tkinter
class App(tk.Tk):

    # Creates a frame
    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title = 'Currency Converter'
        self.currency_converter = converter

        # Set the size of the window
        self.geometry("600x225")
        
        # Label
        self.intro_label = Label(self, text = 'Real Time Currency Converter', fg = 'white')
        self.intro_label.config(font = ('Helvetica', 32 ,'bold'))
        label = self.intro_label
        label.place(relx= 0.5, rely= .1, anchor=CENTER)

        self.date_label = Label(self, text = f"1 US Dollar equals = {self.currency_converter.convert('USD','EUR',1)} EUR \n Date : {self.currency_converter.data['date']}", relief = tk.GROOVE, borderwidth = 2, padx = 3, pady = 3)
        label = self.date_label
        label.place(relx= 0.5, rely= .38, anchor=CENTER)

        # Entry
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = Entry(self,bd = 3, relief = tk.RIDGE, justify = tk.CENTER,validate='key', validatecommand=valid, width = 20)
        self.converted_amount_field_label = Label(self, text = '', fg = 'black', bg = 'white', relief = tk.RIDGE, justify = tk.CENTER, width = 20, borderwidth = 3)
        entry = self.amount_field
        entry.place(relx= 0.16, rely= .1, anchor=CENTER)
        label = self.converted_amount_field_label
        label.place(relx= 0.19, rely= .1, anchor=CENTER)

        # Dropdown
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("USD") # default value
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("EUR") # default value
        font = ("Helvetica", 14, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 22, justify = tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 22, justify = tk.CENTER)
        drop = self.from_currency_dropdown
        drop.place(relx=0.17, rely=.11, anchor=CENTER)
        drop2 = self.to_currency_dropdown
        drop2.place(relx=0.20, rely=.11, anchor=CENTER)
        drop.option_add('*TCombobox*Listbox.Justify', 'center')

        # Placing
        self.from_currency_dropdown.place(x = 30, y= 120)
        self.amount_field.place(x = 36, y = 150)
        self.to_currency_dropdown.place(x = 340, y= 120)
        self.converted_amount_field_label.place(x = 346, y = 150)
        
        # Convert button
        self.convert_button = Button(self, text = "Convert", fg = "black", height= "2", command = self.perform) 
        self.convert_button.config(font=('Helvetica', 20, 'bold'))
        convert = self.convert_button
        convert.place(relx=0.495, rely=.715, anchor=CENTER)

    def perform(self):
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr,to_curr,amount)
        converted_amount = round(converted_amount, 4)

        self.converted_amount_field_label.config(text = str(converted_amount))
    
    def restrictNumberOnly(self, action, string):
        regex = compile(r"[0-9]+")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))

if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)

    App(converter)
    mainloop()