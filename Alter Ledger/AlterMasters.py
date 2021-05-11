from tkinter import Tk, Label, Entry, font, Radiobutton, StringVar, Button, messagebox
from tkinter.ttk import Combobox
from requests import request
from xml.etree import ElementTree as Et


class MainWindow:
    def __init__(self, parent):
        font_14 = font.Font(family='Roboto', size=14)
        self.master_selection = StringVar(parent, "0")
        item_radio = Radiobutton(parent, text="Stock Item", font=font_14, value="1", fg="green", indicator=0,
                                 variable=self.master_selection, command=self.item_click, width=15)
        item_radio.grid(row=0, column=2, padx=10, pady=10, ipadx=5, ipady=5)
        ledger_radio = Radiobutton(parent, text="Ledger", font=font_14, value="2", fg="green", indicator=0,
                                   variable=self.master_selection, command=self.led_click, width=15)
        ledger_radio.grid(row=0, column=3, padx=10, pady=10, ipadx=5, ipady=5)
        item_label = Label(parent, text="Select Item to alter : ", font=font_14)
        item_label.grid(row=1, column=2, padx=10, pady=15)
        self.item_combo = Combobox(parent, font=font_14)
        self.item_combo.grid(row=1, column=3, padx=15, pady=10, ipadx=5, ipady=5)
        ledger_label = Label(parent, text="Select Ledger to alter :", font=font_14)
        ledger_label.grid(row=2, column=2, padx=10, pady=10)
        self.ledger_combo = Combobox(parent, font=font_14)
        self.ledger_combo.grid(row=2, column=3, padx=15, pady=10, ipadx=5, ipady=5)
        altered_name = Label(parent, text="Enter Name to alter:", font=font_14)
        altered_name.grid(row=3, column=2, padx=10, pady=10)
        self.altered_entry = Entry(parent, font=font_14, bd=2, width=20)
        self.altered_entry.grid(row=3, column=3, padx=10, pady=10, ipadx=5, ipady=5)
        alter_button = Button(parent, text="Alter", bg="green", fg="white", bd=2, font=font_14, width=12,
                              command=self.alter_click)
        alter_button.grid(row=4, column=3, padx=10, pady=10, ipadx=5, ipady=5)

    def item_click(self):
        item_xml = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE>"
        item_xml += "<ID>ListOfStockItems</ID></HEADER><BODY><DESC><STATICVARIABLES><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT></STATICVARIABLES>"
        item_xml += "</DESC></BODY></ENVELOPE>"
        item_res = self.get_data(item_xml)
        items = []
        for item in item_res.findall("./BODY/DATA/COLLECTION/STOCKITEM"):
            items.append(item.get("NAME"))
        self.item_combo['values'] = items
        self.item_combo['state'] = "enabled"
        self.ledger_combo['state'] = "disabled"

    def alter_click(self):
        if self.master_selection.get() == "1":
            xml = "<ENVELOPE><HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER><BODY>"
            xml += "<IMPORTDATA><REQUESTDESC><REPORTNAME>All Masters</REPORTNAME></REQUESTDESC><REQUESTDATA>"
            xml += "<TALLYMESSAGE xmlns:UDF='TallyUDF'><STOCKITEM Action='Create' Name='" + self.item_combo.get().strip() + "'><NAME>" + self.altered_entry.get().strip() + "</NAME>"
            xml += "</STOCKITEM></TALLYMESSAGE></REQUESTDATA></IMPORTDATA></BODY></ENVELOPE>"
            res = self.get_data(xml)
            self.show_msg(str(res.find("ALTERED").text) + "  Stock Item Altered")

        elif self.master_selection.get() == "2":
            xml = "<ENVELOPE><HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER><BODY>"
            xml += "<IMPORTDATA><REQUESTDESC><REPORTNAME>All Masters</REPORTNAME></REQUESTDESC><REQUESTDATA>"
            xml += "<TALLYMESSAGE xmlns:UDF='TallyUDF'><LEDGER Action='Create' Name='" + self.ledger_combo.get().strip() + "'><NAME>" + self.altered_entry.get().strip() + "</NAME>"
            xml += "</LEDGER></TALLYMESSAGE></REQUESTDATA></IMPORTDATA></BODY></ENVELOPE>"
            res = self.get_data(xml)
            self.show_msg(str(res.find("ALTERED").text) + "  Ledger Altered")

    @staticmethod
    def show_msg(msg):
        messagebox.showinfo("Response", msg)

    def led_click(self):
        led_xml = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE>"
        led_xml += "<ID>ListOfLedgers</ID></HEADER><BODY><DESC><STATICVARIABLES><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT></STATICVARIABLES>"
        led_xml += "</DESC></BODY></ENVELOPE>"
        led_res = self.get_data(led_xml)
        ledgers = []
        for led in led_res.findall("./BODY/DATA/COLLECTION/LEDGER"):
            ledgers.append(led.get("NAME"))
        self.ledger_combo['values'] = ledgers
        self.ledger_combo['state'] = "enabled"
        self.item_combo['state'] = "disabled"

    @staticmethod
    def get_data(payload):
        req = request("GET", url="http://localhost:9000", data=payload)
        res = req.text.encode("UTF-8")
        return Et.fromstring(res)


if __name__ == "__main__":
    app = Tk()
    app.geometry("700x600")
    app.title("Altering Masters")
    MainWindow(app)
    app.mainloop()
