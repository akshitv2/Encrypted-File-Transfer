
import os
import pickle
from flask import Flask, flash, request, redirect, url_for, render_template, make_response,current_app,send_from_directory,session,escape
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'uploads'

###################################################################################################
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','aes'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return filename[-3:].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        idf = request.form['idx']
        print(idf)
        #div=idf.strip().split(',')
        with open("xexe.txt", "a") as myfile:
            myfile.write(idf+'\n')
        if file and allowed_file(file.filename):
            print ('**found file', file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # for browser, add 'redirect' function on top of 'url_for'
            return url_for('upload_file')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
      <p><input type=text name=idx>
      <p><input type=submit value=Upload>
    </form>
    '''
#id= request.form['id']

#################################################################################
@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/yolo')
def yolo():
    if 'username' in session:
        fobj = open("xexe.txt", "r")
        #x=fobj.read()
        k=[]
        x=''
        for i in fobj:
            k=i
            k=k.split(',')
            print(k)
            if (k[1]==(session['username']+'\n')):
                x+=k[0]+'\n'
        print(x)
        fobj.close()
        return 'Logged in as'+escape(session['username'])+x

    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('selectfile'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Upload>
        </form>
    '''

@app.route('/selectfile', methods=['GET', 'POST'])
def selectfile():
    Tokenname='koala'
    try:
        Tokenname=session['username']
    except: pass

    fobj = open("xexe.txt", "r")
    k=[]
    x='~'

    for i in fobj:
        if (Tokenname=='koala'): break
        k=i.strip().split(',')
        if (k[2]==(Tokenname)):
            x+= k[0] + ' ' + k[1] + '|'
    x+='~'
    if request.method == 'POST':
        session['username'] = request.form['userauth']
        filename= request.form['filename']

        return redirect(url_for('download',filename=filename))
    return x+'''<form action="" method="post">
    <p><input type=text name=filename>
    <p><input type=text name=userauth>
    <p><input type=submit value=Login></form>'''

@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path,'uploads')
    filename=filename[:filename.index('.')]+'.aes'
    fobj = open("xexe.txt", "r")
    k=[]
    x=''
    for i in fobj:
        k=i.strip().split(',')
        if (k[0]==filename):
            break
    print(k[1])
    if(session['username']==k[2]):
        return send_from_directory(directory=uploads, filename=filename)
    else:
        return send_from_directory(directory=uploads, filename='IMG.jpg')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('yolo'))
################################################################################
@app.route('/keys',methods=['GET','POST'])
def keys():
    g = 7
    n = 2860486313
    z='~'+str(g)+','+str(n)+'~'
    if request.method == 'POST':
        keydata = request.form['keyfile'].split(',')
        keyx={}
        keyx[keydata[0]] = keydata[1]
        file_Name = "testfile"
        print(keyx)

        fileObject = open(file_Name,'rb')
        keyauth = pickle.load(fileObject)
        keyauth.update(keyx)
        fileObject.close()

        fileObject = open(file_Name,'wb')
        pickle.dump(keyauth,fileObject)
        fileObject.close()

        print(keyauth)
        return url_for('keys')

    return z+'''<form action="/keys" method="post">
    <p><input type=text name=keyfile>
    <p><input type=submit value=Login></form>'''
################################################################################
@app.route('/diffie',methods=['GET','POST'])
def diffie():
    if request.method == 'POST':
        getreq = request.form['key']
        file_Name = "testfile"
        fileObject = open(file_Name,'rb')
        keyauth = pickle.load(fileObject)
        fileObject.close()
        pubkey = keyauth[getreq]
        return pubkey
    return('<form action="" method="post"><p><input type=text name=key><p><input type=submit value=Login></form>')

################################################################################
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#################################################################################

if __name__ == '__main__':
	app.run(debug=True)
keydict=dict()
print('yes')
