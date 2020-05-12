from flask import Flask,request,render_template,url_for,flash
import pickle
import string
from flask_bootstrap import Bootstrap
from nltk.corpus import stopwords
import os

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(25)

@app.route('/',methods=['GET','POST'])
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
            mode = 'success'
        else:
            my_prediction = "It's a Spam Message"
            mode = 'danger'
        flash(my_prediction, mode)
    return render_template('index.html')

def msg_processor(mess):
    no_punc = [c for c in mess if c not in string.punctuation]
    no_punc = ''.join(no_punc)
    return [word for word in no_punc.split() if word.lower() not in stopwords.words('english')]

if __name__ == '__main__':
    app.run(debug=True)