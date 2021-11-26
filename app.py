import os
from flask import Flask,render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
import string
# from flask import Flask
# import flask.ext.sqlalchemy
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_UR1I'] = 'sqlite:///site.db'
# db = flask.ext.sqlalchemy.SQLAlchemy(app)

app=Flask(__name__)
##########  SQL ALCHEMY CONFIGURATION  #######
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+ os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
Migrate(app,db)


@app.before_first_request
def create_table():
    db.create_all()


##########  CREATE A MODEL  ##################
1
2
3
class url(db.Model):
    __tablename__= 'urls'
    id=db.Column(db.Integer,primary_key=True)
    user_url=db.Column(db.Text)
    short_url=db.Column(db.Text)
    def __init__(self, user_url, short_url):
        self.user_url = user_url
        self.short_url = short_url
    def __repr__(self):
        return "{} -- {}".format(self.user_url,self.short_url)

duplicate_list =["A","B", "C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

data ={}

@app.route('/', methods=['GET', 'POST'])
def home_post():
    if request.method == 'POST':
        
        original_url = request.form.get('in_1')
        short_url = random.choice(duplicate_list) + random.choice(duplicate_list) +  random.choice(duplicate_list) + random.choice(duplicate_list)
        data[short_url] = original_url
        new_original= url(original_url,short_url)
        db.session.add(new_original)
        db.session.commit()
        return render_template('index.html', original_url = original_url, short_url = short_url)
    return render_template('index.html')
    

@app.route('/history')
def histroy():
    URL  = url.query.all()
    return render_template('history.html', data= data, URL = URL)

@app.route('/sh/<short>')
def fun(short):
    if short in data:
        return redirect(data[short])
    return "inncorect url"


if __name__=="__main__":
    app.run(debug=True)