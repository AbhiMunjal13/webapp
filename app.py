from flask import Flask,render_template,request,session,redirect,url_for
import database as db
import os
import pandas as pd
from werkzeug.utils import secure_filename
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'C:/Users/priya/Desktop/webapp/static/'

app.secret_key = "super secret key"
@app.route('/')
def home():
    try:
        session['email']
        
        list1 = pd.DataFrame(db.get_recepies())
        list1 = list1.rename(columns = {0:'recepies',1:'image'})
        return render_template('home.html',data = zip(list1.recepies,list1.image),login="Logout")
    except:
        
        list1 = pd.DataFrame(db.get_recepies())
        list1 = list1.rename(columns = {0:'recepies',1:'image'})
        return render_template('home.html',data = zip(list1.recepies,list1.image),login='Login/SingnUp')        



@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='POST':
        if len(db.search_email(request.form['email'])) == 1 and db.search_password(request.form['email'])==request.form['password']:
            session['email'] = request.form['email']
            return redirect(url_for('dashboard'))
           # print(request.form['password'])
        else :
                return render_template('login.html',message='****Credentials entered are wrong****')           
        
    if request.args.get('message')!=None:    
        return render_template('login.html',message=request.args.get('message'))
    else:
        return render_template('login.html')

@app.route('/login/add_user',methods=['GET','POST'])
def add_user():
    try:
       
            if len(db.search_email(request.form['sign_email']))==0:
                sign_username = request.form['sign_username']
                sign_email = request.form['sign_email']
                sign_password = request.form['sign_password']
                db.add_user(sign_username,sign_password,sign_email)
                return redirect(url_for('login'))
            else :
                return redirect(url_for('login',message='Email Already exist try with another one'))
       
    except  :
        return redirect(url_for('login.html',message='Opps looks like something went wrong'))

@app.route('/info/',methods=['GET','POST'])
def info():
    list1 = pd.DataFrame(db.get_recepies())
    list1 = list1.rename(columns = {0:'recepies',1:'image'})
    if request.args.get('info') !=None:
            instruction1 = db.get_recepies_info(request.args.get('info'))
            return render_template('info.html',data=request.args.get('info'),instruction = instruction1,pic=(db.get_food_image(request.args.get('info'))))

@app.route('/dashboard/',methods=['GET','POST'])
def dashboard():
    try:
        list1 = pd.DataFrame(db.get_recepies_email(session['email']))
        if len(list1!=0):
            list1 = list1.rename(columns = {0:'recepies',1:'image'})
        #if request.method == 'POST':
            if request.args.get('info') !=None:
                instruction1 = db.get_recepies_info(request.args.get('info'))
                return render_template('info.html',data=request.args.get('info'),instruction = instruction1,pic=(db.get_food_image(request.args.get('info'))))
        
            return render_template('dashboard.html',data = zip(list1.recepies,list1.image))
        else:
            return render_template('dashboard.html')
    except:
        return redirect(url_for('login'))

        

@app.route('/add/',methods=['GET','POST'])
def add():
    try:
        if session['email']!=None:
            if request.method=="POST":
                
                f = request.files['file']
                f.filename = str(request.form['title'])+'.jpg'
                file =secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'],file))
                db.add_food(request.form['title'],request.form['content'],session['email'],file)
                return redirect(url_for('home'))
            return render_template('blog.html')
        else:
                return redirect(url_for('login'))
    except:
        return redirect(url_for('login'))
    
@app.route("/edit/",methods=['GET','POST'])
def edit():
    old_title = request.args.get('edit')
    if request.method=="POST":
        new_title=(request.form['title'])
        new_instruction=(request.form['content'])
        f = request.files['file']
        if f.filename!="":
            f.filename = str(request.form['title'])+'.jpg'
            file =secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],file))
            db.update(new_title,new_instruction,file,session['email'],old_title)
            return redirect(url_for('dashboard'))
        
        else:
             db.update(new_title,new_instruction,f.filename,session['email'],old_title)
             return redirect(url_for('dashboard'))
           
    
    return render_template('blog_edit.html',title=old_title,content = db.get_recepies_info(old_title)) 

@app.route('/delete/',methods=['GET','POST'])         
def delete():
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'],db.get_food_image(request.args.get('delete'))))
    db.delete(request.args.get('delete'),session['email'])
    return redirect(url_for('dashboard')) 

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

if __name__=='__main__':
    app.run(debug=False)
    

