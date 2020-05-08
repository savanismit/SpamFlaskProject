from flask import Flask,request,render_template,url_for
import pickle
import string
from nltk.corpus import stopwords
import os

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')

def msg_processor(mess):
    no_punc = [c for c in mess if c not in string.punctuation]
    no_punc = ''.join(no_punc)
    return [word for word in no_punc.split() if word.lower() not in stopwords.words('english')]

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        mess = request.form['message']
        mess = [mess]
        pickle_f = open('pipeline.pickle','rb')
        trans = pickle.load(pickle_f)
        pred = trans.predict(mess)
        pred = ''.join(pred)
        if pred == 'ham':
            my_prediction = "Normal Message"
        else:
            my_prediction = "It's a Spam Message"
    return render_template('result.html',prediction = my_prediction)
if __name__ == '__main__':
    app.run(debug=True)