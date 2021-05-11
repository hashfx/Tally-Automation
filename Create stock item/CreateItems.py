from tkinter import Button, Label, Entry, font, Tk, messagebox
import requests


class MainWindow:
    def __init__(self, main):
        font_14 = font.Font(family='Sans serif', size=14)
        font_18 = font.Font(family='Sans serif', size=18)

        # item name
        item_name = Label(main, text="Item Name : ", font=font_14, fg='green')
        item_name.grid(row=1, column=2, ipadx=10, ipady=20)
        self.item_name_entry = Entry(main, font=font_18, bd=2, width=20)
        self.item_name_entry.grid(row=1, column=3, ipadx=10)

        # item unit
        item_unit = Label(main, text="Item Unit : ", font=font_14, fg='green')
        item_unit.grid(row=2, column=2, ipadx=10, ipady=20)
        self.item_unit_entry = Entry(main, font=font_18, bd=2, width=20)
        self.item_unit_entry.grid(row=2, column=3, ipadx=10)

        # item hsn
        item_hsn = Label(main, text="Item HSN : ", font=font_14, fg='green')
        item_hsn.grid(row=3, column=2, ipadx=10, ipady=20)
        self.item_hsn_entry = Entry(main, font=font_18, bd=2, width=20)
        self.item_hsn_entry.grid(row=3, column=3, ipadx=10)

        # item gst
        item_gst = Label(main, text="Item GST % : ", font=font_14, fg='green')
        item_gst.grid(row=4, column=2, ipadx=10, ipady=20)
        self.item_gst_entry = Entry(main, font=font_18, bd=2, width=20)
        self.item_gst_entry.grid(row=4, column=3, ipadx=10)

        # item Opening
        item_opening = Label(main, text="Item Opening : ", font=font_14, fg='green')
        item_opening.grid(row=5, column=2, ipadx=10, ipady=20)
        self.item_opening_entry = Entry(main, font=font_18, bd=2, width=20)
        self.item_opening_entry.grid(row=5, column=3, ipadx=10)

        # Submit button
        submit_button = Button(main, text="Submit", font=font_18, bd=2, fg='white', bg='green', width=10, padx=5,
                               pady=5, command=self.Submit)
        submit_button.grid(row=7, column=3)

    def Submit(self):
        name = self.item_name_entry.get()
        unit = self.item_unit_entry.get()
        hsn = self.item_hsn_entry.get()
        gst = int(self.item_gst_entry.get())
        opening = self.item_opening_entry.get()
        xml_body = '<ENVELOPE><HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER><BODY><IMPORTDATA><REQUESTDESC><REPORTNAME>All Masters</REPORTNAME></REQUESTDESC><REQUESTDATA>';
        xml_body += '<TALLYMESSAGE xmlns:UDF="TallyUDF"><STOCKITEM Action="Create"><NAME>' + name + '</NAME><BASEUNITS>' + unit + '</BASEUNITS><OPENINGBALANCE>' + opening + '</OPENINGBALANCE>'
        xml_body += '<GSTAPPLICABLE>&#4; Applicable</GSTAPPLICABLE><GSTDETAILS.LIST><APPLICABLEFROM>20200401</APPLICABLEFROM><CALCULATIONTYPE>On Value</CALCULATIONTYPE><HSNCODE>' + hsn + '</HSNCODE>'
        xml_body += '<TAXABILITY>Taxable</TAXABILITY><STATEWISEDETAILS.LIST><STATENAME>&#4; Any</STATENAME><RATEDETAILS.LIST><GSTRATEDUTYHEAD>Central Tax</GSTRATEDUTYHEAD>'
        xml_body += '<GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE><GSTRATE>' + str(gst / 2) + '</GSTRATE></RATEDETAILS.LIST><RATEDETAILS.LIST><GSTRATEDUTYHEAD>State Tax</GSTRATEDUTYHEAD>'
        xml_body += '<GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE><GSTRATE>' + str(gst / 2) + '</GSTRATE></RATEDETAILS.LIST><RATEDETAILS.LIST><GSTRATEDUTYHEAD>Integrated Tax</GSTRATEDUTYHEAD>'
        xml_body += '<GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE><GSTRATE>' + str(gst) + '</GSTRATE></RATEDETAILS.LIST><RATEDETAILS.LIST><GSTRATEDUTYHEAD>Cess</GSTRATEDUTYHEAD>'
        xml_body += '<GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE></RATEDETAILS.LIST></STATEWISEDETAILS.LIST></GSTDETAILS.LIST></STOCKITEM></TALLYMESSAGE></REQUESTDATA>'
        xml_body += '</IMPORTDATA></BODY></ENVELOPE>'
        req = requests.post(url="http://localhost:9000", data=xml_body)
        messagebox.showinfo("Response", req.text)


root = Tk()
root.geometry("800x600")
root.title("Creating Stock Items")
MainWindow(root)
root.mainloop()
