import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk
import re
import pandas as pd
import matplotlib.pyplot as plt
import json

# Creates a dataframe using pandas that shows the 15 currencies more valuable than the USD.
df = pd.read_csv('rates.csv')
newdf = df.nsmallest(16, "Rate")
print(newdf)

# Gets the exchange rate from an external exchange rate api and returns the converted amount.
class RealTimeCurrencyConverter():
    def __init__(self,url):
            self.data = requests.get(url).json()
            self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        if from_currency != 'USD' : 
            amount = amount / self.currencies[from_currency] 
  
        # Limits rates to 4 decimal places 
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

# Creates a GUI using tkinter
class App(tk.Tk):

    # Creates a frame
    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title = 'Currency Converter'
        self.currency_converter = converter

        # Sets the size of the window
        self.geometry("600x225")
        
        # Label - This is the header.
        self.intro_label = Label(self, text = 'Real Time Currency Converter', fg = 'white')
        self.intro_label.config(font = ('Helvetica', 32 ,'bold'))
        label = self.intro_label
        label.place(relx= 0.5, rely= .1, anchor=CENTER)

        # Creates the text box in the middle of the frame that dispalys the value of $1 USD in 1 EUR.
        self.date_label = Label(self, text = f"1 US Dollar equals = {self.currency_converter.convert('USD','EUR',1)} EUR \n Date : {self.currency_converter.data['date']}", relief = tk.GROOVE, borderwidth = 2, padx = 3, pady = 3)
        label = self.date_label
        label.place(relx= 0.5, rely= .38, anchor=CENTER)

        # Entry box
        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        # Sets the characteristics for the entry box
        self.amount_field = Entry(self,bd = 3, relief = tk.RIDGE, justify = tk.CENTER,validate='key', validatecommand=valid, width = 20)
        # Sets the characteristics for the converted amount field
        self.converted_amount_field_label = Label(self, text = '', fg = 'black', bg = 'white', relief = tk.RIDGE, justify = tk.CENTER, width = 20, borderwidth = 3)
        entry = self.amount_field
        # Sets the position for the entry box
        entry.place(relx= .22, rely= .78, anchor=CENTER)
        
        # Sets the position for the Converted Amount box
        label = self.converted_amount_field_label
        label.place(relx= .773, rely= .78, anchor=CENTER)

        # Left dropdown menu.  Select currency you would like to convert.
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("USD") # default value
        # Right dropdown menu.  Select the currency you would like to convert into.
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("EUR") # default value
        font = ("Helvetica", 14, "bold")
        self.option_add('*TCombobox*Listbox.font', font)
        # Sets characteristics for left dropdown
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 22, justify = tk.CENTER)
        # Sets characteristics for right dropdown
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,values=list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 22, justify = tk.CENTER)
        # Sets positioning for left dropdown
        drop = self.from_currency_dropdown
        drop.place(relx= 0.22, rely= 0.65, anchor=CENTER)
        # Sets positioning for right dropdown
        drop2 = self.to_currency_dropdown
        drop2.place(relx= 0.773, rely= 0.65, anchor=CENTER)
        drop.option_add('*TCombobox*Listbox.Justify', 'center')
        
        # Creates convert button
        self.convert_button = Button(self, text = "Convert", fg = "black", height= "2", command = self.perform) 
        self.convert_button.config(font=('Helvetica', 20, 'bold'))
        # Sets positioning for convert button
        convert = self.convert_button
        convert.place(relx=0.495, rely=.715, anchor=CENTER)

    # Takes input and converts into selected currency and displays in converted_amount box
    def perform(self):
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr,to_curr,amount)
        converted_amount = round(converted_amount, 4)

        self.converted_amount_field_label.config(text = str(converted_amount))

    # Restricts entries to only numbers 
    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))

if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)

    App(converter)
    mainloop()

# Creates a chart using myplotlib showing the 15 listed currencies that are more valuable than the USD.
# Each currency's value to the left of the USD is the amount $1 USD converts to.
newdf.plot(x ='Currency', y='Rate', kind = 'bar', title= '15 Currencies More Valuable Than The USD')
plt.show()