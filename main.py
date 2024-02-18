from sklearn.pipeline import Pipeline
from flask import Flask , render_template,request,redirect,url_for,session,send_file
import pandas as pd
import numpy as np
import pickle


cleandata = pd.read_csv('firstclean.csv')
modle_pre = pickle.load(open('LrModle.pkl','rb'))

area =  sorted(set(cleandata['Area']))
bhk = sorted(set(cleandata['BHK']))
Bathroom = sorted(set([int(i) for i in cleandata['Bathroom']]))
Furnishing = sorted(set(cleandata['Furnishing']))
Locality = sorted(set(cleandata['Locality']))
Parking = sorted(set([int(i) for i in cleandata['Parking']]))
Status = sorted(set(cleandata['Status']))
Transaction = sorted(set(cleandata['Transaction']))
Type = sorted(set(cleandata['Type']))

class list_of_data():
    def __init__(self, area, bhk,Bathroom,Furnishing,Locality,Parking,Status,Transaction,Type):
        self.area =  area
        self.bhk = bhk
        self.Bathroom = Bathroom
        self.Furnishing = Furnishing
        self.Locality = Locality
        self.Parking = Parking
        self.Status = Status
        self.Transaction = Transaction
        self.Type = Type


app = Flask(__name__)

SECRET_KEY = 'dsaf0897sfdg45sfdgfdsaqzdf98sdf0a'

def create_object():
    object = {"key": "value"}
    return object

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/main', methods=['GET', 'POST'])
def datatack():
    if request.method == 'POST':
        area_ = float(request.form.get("area"))
        bhk_ = request.form.get("bhk")
        Bathroom_ = float(request.form.get("bathroom"))
        Furnishing_ = request.form.get("Furnishing")
        Locality_ = str(request.form.get("Locality"))
        Parking_ = float(request.form.get("Parking"))
        Status_ = request.form.get("Status")
        Transaction_ = request.form.get("Transaction")
        Type_ = request.form.get("Type")
        global data
        data = list_of_data(area=area_, bhk=bhk_, Bathroom=Bathroom_, Furnishing=Furnishing_, Locality=Locality_, Parking=Parking_, Status=Status_, Transaction=Transaction_, Type=Type_)
        return redirect(url_for("Result"))
    else:
        return render_template("main.html", area=area, bhk=bhk, Bathroom=Bathroom, Furnishing=Furnishing,
                               Locality=Locality, Parking=Parking, Status=Status, Transaction=Transaction,
                               Type=Type)


@app.route('/Result', methods=['GET', 'POST'])
def Result():
    
    global dataset
    dataset = pd.DataFrame([[data.area, data.bhk, data.Bathroom, data.Furnishing, data.Locality, data.Parking, data.Status, data.Transaction, data.Type]], columns=['Area', 'BHK', 'Bathroom', 'Furnishing', 'Locality', 'Parking', 'Status', 'Transaction', 'Type'])
    global pre_data
    pre_data = modle_pre.predict(dataset)
    pre_data = pre_data.round(0)
    return render_template("result.html", data=pre_data, info=data)
  

@app.route("/download")
def download():
    dataName = create_bill(dataset)
    return send_file(dataName, as_attachment=True)

def create_bill( items):
    df = dataset
    df['price'] = pre_data
    txt_file_path = 'data.txt'  # Replace with the desired TXT file path
    df.to_csv(txt_file_path, sep='\t', index=False)
    return txt_file_path

if __name__ =="__main__":
    app.run(debug=False,host = '0.0.0.0')