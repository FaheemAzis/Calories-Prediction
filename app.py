# import libraires
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from flask import Flask , render_template , request
import gunicorn
import PreProcessing
import plotly.express as px
import pandas as pd


#load model
model = pickle.load(open('Calories_model', "rb"))

#load scaler
scalerfile = 'scaler.save'
scaler = pickle.load(open(scalerfile, 'rb'))
pp = PreProcessing

app = Flask(__name__)

@app.route('/')

@app.route('/main_template',methods=["GET"])
def main_template():

    #render form
    return render_template('Index.html')

@app.route('/data',methods=["GET","POST"])
def datas():

    #render form
    return render_template('data.html')

@app.route('/visual',methods=["GET","POST"])
def visual():

    #render form
    return render_template('visual.html')


@app.route('/class',methods=["GET","POST"])
def classifier():

    #render form
    return render_template('class.html')

#get form regression from caloriers.html
@app.route('/predict',methods=['GET','POST'])
def predict():

    #checking request type
    str_req_type = request.method

    #convert string value into numeric value
    if request.method == str(str_req_type):

        if request.args.get('gender') == 'Male':
            gender = 1

        else:
            gender = 0

        age = request.form.get('age')
        duration = request.form.get('duration')
        heart_Rate = request.form.get('heart_Rate')
        temp = request.form.get('temp')
        height = request.form.get('height')
        weight = request.form.get('weight')

        #store form values into set
        values = [float(gender), float(age), float(height), float(weight), float(duration), float(heart_Rate), float(temp)]

        #turn into array & reshape array for prediction
        input_array = np.asarray(values)
        input_array_reshape = input_array.reshape(1, -1)

        #sclae the inputed reshaped data
        scaled_set = scaler.transform(input_array_reshape)

        # predict with inputed values
        predicted = model.predict(scaled_set)

        #display predicted valuesin result.html file
        return  render_template('result.html', predicted_value=predicted[0])

    else:

        return render_template('Index.html')

#get form classification from caloriers.html
@app.route('/predict2',methods = ['GET','POST'])
def predict2():
    grains = float (request.form['grains'])
    vegetables = float (request.form['vegetables'])
    fruits = float (request.form['fruits'])
    protein = float (request.form['protein'])

    predictedResult = pp.healthy_diet(grains,vegetables,fruits,protein)
    print('Experience is ',predictedResult)
    return render_template('result2.html', PredictedResult = predictedResult,)


if __name__ == '__main__':
    app.run(debug=True)
