#import required packages

import requests
import xml.etree.ElementTree as Et 
import tkinter.font as font
from tkinter import *


#MainWindow Class

class MainWindow():

    def __init__(self,root):
        #tallyIp
        self.url = "http://localhost:9000"
        #XMLbody
        self.xmlBody = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>COLLECTION</TYPE><ID>StockItems</ID></HEADER>"
        self.xmlBody += "<BODY><DESC><STATICVARIABLES><SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT></STATICVARIABLES><TDL><TDLMESSAGE><COLLECTION Name='StockItems'>"
        self.xmlBody += "<TYPE>StockItem</TYPE><FETCH>Name,ClosingBalance,BaseUnits</FETCH></COLLECTION></TDLMESSAGE></TDL></DESC></BODY></ENVELOPE>"
        self.font = font.Font(family='Verdana')
        button = Button(root,text="Get Items",bg="blue",fg="white",bd=2,height=2,width=20,command=self.getItems)
        button['font'] = self.font
        button.grid(row=1,column=1,padx=10,pady=10)

    def getItems(self):
        req = requests.post(url=self.url,data=self.xmlBody)
        res = req.text.strip()
        responseXML = Et.fromstring(res)

        #add headers
        h1 = Entry(width = 20,fg="green",font=self.font)
        h1.insert(0,'ITEM NAME')
        h1.grid(row=2,column=3,ipadx=5,ipady=5)

        h2 = Entry(width = 20,fg="green",font=self.font)
        h2.insert(0,'CLOSING')
        h2.grid(row=2,column=4,ipadx=5,ipady=5)

        h3 = Entry(width = 20,fg="green",font=self.font)
        h3.insert(0,'UNIT')
        h3.grid(row=2,column=5,ipadx=5,ipady=5)

        #actual data

        rowCount = 3
        for item in responseXML.findall('./BODY/DATA/COLLECTION/STOCKITEM'):
            r1 = Entry(width=20,font=self.font)
            r1.insert(0,item.get('NAME'))
            r1.grid(row=rowCount,column=3,ipadx=5,ipady=5)

            r2 = Entry(width=20,font=self.font)
            r2.insert(0,item.find('CLOSINGBALANCE').text)
            r2.grid(row=rowCount,column=4,ipadx=5,ipady=5)

            r3 = Entry(width=20,font=self.font)
            r3.insert(0,item.find('BASEUNITS').text)
            r3.grid(row=rowCount,column=5,ipadx=5,ipady=5)

            rowCount += 1

          


#Main Entry - initialize tk 
root = Tk()
root.geometry("1000x600")
MainWindow(root)
root.mainloop()
