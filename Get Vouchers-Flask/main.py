from flask import Flask, render_template, url_for, request
import requests
from xml.etree import ElementTree as Et

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/listOfVouchers', methods=['POST'])
def vouchers():
    vch_type = request.form['voucherType']
    from_dt = request.form['fromDt']
    to_dt = request.form['toDt']
    res = Et.fromstring(get_data(get_payload(vch_type,from_dt,to_dt)))
    voucher_models = []
    for vch in res.findall("./BODY/DATA/TALLYMESSAGE/VOUCHER"):
        if len(vch.findall("ALLLEDGERENTRIES.LIST")) == 0:
            amount = vch.findall("LEDGERENTRIES.LIST").__getitem__(0).find("AMOUNT").text
        else:
            amount = vch.findall("ALLLEDGERENTRIES.LIST").__getitem__(0).find("AMOUNT").text
        voucher_models.append(
            VoucherModel(vch.find("DATE").text, vch.find("VOUCHERTYPENAME").text, vch.find("VOUCHERNUMBER").text,
                         vch.find("PARTYLEDGERNAME").text, amount))

    return render_template('Vouchers.html', vch_type=vch_type, from_dt=from_dt, to_dt=to_dt, data=voucher_models)


def get_data(payload):
    req = requests.post(url="http://localhost:9000", data=payload)
    res = req.text.encode("UTF-8")
    print(res)
    return res


def get_payload(v_type, from_dt, to_dt):
    xml = "<ENVELOPE><HEADER><VERSION>1</VERSION><TALLYREQUEST>EXPORT</TALLYREQUEST><TYPE>DATA</TYPE>"
    xml += "<ID>VoucherRegister</ID></HEADER><BODY><DESC><STATICVARIABLES>"
    xml += "<SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT><SVFROMDATE Type='DATE'>"+from_dt+"</SVFROMDATE><SVTODATE Type='DATE'>"+to_dt+"</SVTODATE><VOUCHERTYPENAME>" + v_type + "</VOUCHERTYPENAME></STATICVARIABLES>"
    xml += "</DESC></BODY></ENVELOPE>"
    return xml


class VoucherModel:
    def __init__(self, date, v_type, v_no, party_ledger, amount):
        self.date = date
        self.v_type = v_type
        self.v_no = v_no
        self.party_ledger = party_ledger
        self.amount = amount


if __name__ == "__main__":
    app.run(debug=True)
