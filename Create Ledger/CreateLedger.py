from tkinter import *
import tkinter.font as font
from tkinter import ttk, messagebox
import requests


class MainWindow:

    def __init__(self, main):
        font_18 = font.Font(family='verdana', size=18)
        font_14 = font.Font(family='verdana', size=14)

        # name
        led_name = Label(main, text="Ledger Name:", font=font_14, fg='green')
        led_name.grid(row=3, column=2, ipadx=20, ipady=20)
        self.led_entry = Entry(main, font=font_18, width=20, )
        self.led_entry.grid(row=3, column=3, ipadx=20)

        # group
        led_group = Label(main, text='Group Name:', font=font_14, fg='green')
        led_group.grid(row=4, column=2, ipadx=20, ipady=20)
        led_options = ('Sundry Debtors', 'Sundry Creditors')
        self.led_combo = ttk.Combobox(main, values=led_options, width=18, font=font_18)
        self.led_combo.grid(row=4, column=3, ipadx=20)

        # address
        led_address = Label(main, text="Ledger Address:", font=font_14, fg='green')
        led_address.grid(row=5, column=2, ipadx=20, ipady=20)
        self.led_address_entry = Entry(main, font=font_18, width=20)
        self.led_address_entry.grid(row=5, column=3, ipadx=20)

        # country
        led_country = Label(main, text="Ledger Country:", font=font_14, fg='green')
        led_country.grid(row=6, column=2, ipadx=20, ipady=20)
        self.led_country_entry = Entry(main, font=font_18, width=20)
        self.led_country_entry.grid(row=6, column=3, ipadx=20)

        # State
        led_state = Label(main, text="Ledger State:", font=font_14, fg='green')
        led_state.grid(row=7, column=2, ipadx=20, ipady=20)
        self.led_state_entry = Entry(main, font=font_18, width=20)
        self.led_state_entry.grid(row=7, column=3, ipadx=20)

        # Mobile
        led_mobile = Label(main, text="Ledger Mobile:", font=font_14, fg='green')
        led_mobile.grid(row=8, column=2, ipadx=20, ipady=20)
        self.led_mobile_entry = Entry(main, font=font_18, width=20)
        self.led_mobile_entry.grid(row=8, column=3, ipadx=20)

        # Gst
        led_gst = Label(main, text="Ledger GSTIN:", font=font_14, fg='green')
        led_gst.grid(row=9, column=2, ipadx=20, ipady=20)
        self.led_gst_entry = Entry(main, font=font_18, width=20)
        self.led_gst_entry.grid(row=9, column=3, ipadx=20)

        # submit button
        submit_button = Button(main, text="Submit", font=font_14, fg='white', bg="green", command=self.Submit)
        submit_button.grid(row=10, column=3, ipadx=20)

    def Submit(self):
        led_name = self.led_entry.get()
        led_group = self.led_combo.get()
        led_address = self.led_address_entry.get()
        led_country = self.led_country_entry.get()
        led_state = self.led_state_entry.get()
        led_mobile = self.led_mobile_entry.get()
        led_gst = self.led_gst_entry.get()
        url = 'http://localhost:9000'
        data = '<ENVELOPE><HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER><BODY>'
        data += '<IMPORTDATA><REQUESTDESC><REPORTNAME>All Masters</REPORTNAME></REQUESTDESC><REQUESTDATA>'
        data += '<TALLYMESSAGE xmlns:UDF="TallyUDF"><LEDGER Action="Create"><NAME>'+led_name+'</NAME><PARENT>'+led_group
        data += '</PARENT><ADDRESS>'+led_address+'</ADDRESS><COUNTRYOFRESIDENCE>'+led_country+'</COUNTRYOFRESIDENCE>'
        data += '<LEDSTATENAME>'+led_state+'</LEDSTATENAME><LEDGERMOBILE>'+led_mobile+'</LEDGERMOBILE><PARTYGSTIN>'
        data += led_gst+'</PARTYGSTIN></LEDGER></TALLYMESSAGE></REQUESTDATA></IMPORTDATA></BODY></ENVELOPE>'
        req = requests.post(url=url, data=data)
        self.ShowDialog(req.text)

    @staticmethod
    def ShowDialog(msg):
        messagebox.showinfo("Information", msg)


root = Tk()
root.geometry("800x600")
root.title("Create Ledger")
MainWindow(root)
root.mainloop()
