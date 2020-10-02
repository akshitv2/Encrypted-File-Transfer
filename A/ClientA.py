#Working for Client A (1st client)
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.graphics import Color,Rectangle
from kivy.core.window import Window
import requests
import pyAesCrypt
from os import stat
import os
import hashlib
import binascii
import urllib
import time
#AES256-CBC

class pr2kvlogin(FloatLayout):
    username_text_input = ObjectProperty()
    def login(self):
        userx = self.username_text_input.text
        Token = userx
        url = url_base + "keys"
        bToken=bytes(Token, 'utf-8')
        dk = hashlib.pbkdf2_hmac('sha256', bToken, b'guessthis', 100000)
        global trip
        trip = (hashlib.md5(bToken).hexdigest())[-10:]
        print(trip)
        key=int(binascii.hexlify(dk),16)
        a=int(str(key)[:6])
        b=int(str(key)[-5:])
        fp = urllib.request.urlopen(url)
        mybytes = fp.read().decode("utf8")
        fp.close()
        x='';p=0
        for i in mybytes:
            if(i=='~'):p+=1;continue;
            if(p==1): x+=i
            if(p==2): break
        x=list(map(int,x.strip().split(',')))
        print(2)
        ################################################################################
        G=x[0];N=x[1]
        k=(((G**a)%N)**b)%N;
        global Keys
        Keys = [a,b,k,N]
        print(3)
        print(G)
        ################################################################################
        LOCUS=trip+','+str(k)
        data={'keyfile':LOCUS}
        print(LOCUS)
        r = requests.post(url,data=data)
        print(4)
        ################################################################################
        f = open('prmenu.kv','w')
        xrite = "# Reference ClientA.py\n#: import main ClientA\nprmenu:\n<Button>:\n\tfont_size: 30\n\tcolor:1,1,1,1\n<FloatLayout>:\n\tAsyncImage:\n\t\tsource: 'back.jpg'\n\t\tcanvas:" + "\n\t\t\tColor:\n\t\t\t\trgba: 0.478, 0.478, 0.478,0.6\n\t\t\tRectangle:\n\t\t\t\tpos: 430,100\n\t\t\t\tsize: 350,400\n\t\t\tRectangle:\n\t\t\t\tpos: 50,100\n\t\t\t\tsize: 300,400\n\t\t\tRectangle:\n\t\t\t\tpos: 385,100\n\t\t\t\tsize: 10,400"
        xrite+="\n\tLabel:\n\t\ttext: '"+trip+"'\n\t\tfont_size: 20\n\t\tpos: -200,0\n\t\tsize: 10,400\n\tButton:\n\t\ttext:'Send'\n\t\tsize_hint: 0.3, 0.08\n\t\tpos: 490,250\n\t\ton_release: root.Sendscreen()\n\tButton:\n\t\ttext: 'Receive'\n\t\tsize_hint: 0.3, 0.08\n\t\tpos: 490,350\n\t\ton_press: root.Receivescreen()"
        f.write(xrite)
        f.close()
        time.sleep(2)
        App.get_running_app().destroy_settings()
        App.get_running_app().stop()
        prmenuApp().run()

class pr2kvloginApp(App):
    pass

class prmenu(FloatLayout):
    def Sendscreen(self):
        App.get_running_app().stop()
        App.get_running_app().destroy_settings()
        #self.root_window.close()
        prSendApp().run()
    def Receivescreen(self):
        App.get_running_app().stop()
        App.get_running_app().destroy_settings()
        #self.root_window.close()
        prReceiveApp().run()

class prmenuApp(App):
    pass

class prReceive(FloatLayout):
    filesel_text_input = ObjectProperty()
    error_output = StringProperty()
    file_output = StringProperty()
    def __init__(self, **kwargs):
        super(prReceive, self).__init__(**kwargs)

        url = url_base + 'login'
        data={'username':trip}
        r = requests.post(url, data=data)
        x='';p=0
        global idlist
        idlist={}
        for i in r.text:
            if(i=='~'):p+=1;continue;
            if(p==1): x+=i
            if(p==2): break
        x=x.strip().split('|')
        MArr=[]
        for i in x:
            if(len(i)!=0):
                MArr.append(i)
        print(MArr)
        for i in MArr:
            psp =i.split(' ')
            idlist.update({psp[0]:psp[1]})
        self.file_output = ''
        for i in idlist.keys():
            print(i)
            self.file_output += str(i)+' - '

    def receive(self):
        filesel = self.filesel_text_input.text
        if(filesel not in idlist.keys()):
            self.error_output = 'Wrong File Selected'
        else:
            fname = filesel
            url = url_base + "diffie"
            sendto = idlist[fname]
            data={'key':sendto}
            r = requests.post(url,data=data)
            idpub = int(r.text)
            password = (((idpub**Keys[0])%Keys[3])**Keys[1])%Keys[3]
            ################################################################################
            password = str(password)
            print(password)
            bufferSize = 64 * 1024

            path = fname[:fname.index('.')]
            format = '.'+fname[fname.index('.')+1:]

            url = url_base + "selectfile"
            data={'filename':fname, 'userauth': trip}
            r = requests.post(url, data=data)
            time.sleep(1)

            open('filec/'+path+'.aes', 'wb').write(r.content)
            print(path+format)
            encFileSize = stat('filec/'+path+'.aes').st_size

            # decrypt
            with open('filec/'+path+'.aes', "rb") as fIn:
                with open('filed/'+path+format, "wb") as fOut:
                    try:
                        pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, encFileSize)
                    except ValueError:
                        remove('filed/'+path+format)

class prReceiveApp(App):
    pass


class prSend(FloatLayout):
    sendto_text_input = ObjectProperty()
    filepath_text_input = ObjectProperty()
    error_output = StringProperty()
    def __init__(self, **kwargs):
        super(prSend, self).__init__(**kwargs)
    def send(self):
        sendto = self.sendto_text_input.text
        FilePath = self.filepath_text_input.text
        print(FilePath)
        if(len(sendto)==0):
            self.error_output = 'Enter Sender'
        elif(len(FilePath)==0):
            self.error_output = 'Select File'
        else:
            self.error_output = ''
            url = url_base + "diffie"
            data={'key':sendto}
            r = requests.post(url,data=data)
            idpub = int(r.text)
            global Keys
            #try:
            password = (((idpub**Keys[0])%Keys[3])**Keys[1])%Keys[3]
            #except:
            #    password = 12345
            print(5)
            ################################################################################
            password=str(password)
            bufferSize = 64 * 1024
            path = FilePath
            pathx=path[path.index('.')+1:]
            with open("filea/"+path, "rb") as fIn:
                with open("fileb/"+path[:path.index('.')]+".aes", "wb") as fOut:
                    pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
            fin=open("filea/"+path, "rb")
            url = url_base + "uploader"
            a=path + ',' + trip + ',' + sendto
            fin = open('fileb/'+path[:path.index('.')]+'.aes', 'rb')
            files={'file': fin}
            data = {'idx':a}
            print(a)
            try:
              r = requests.post(url,files=files, data=data)
            finally:
            	fin.close()
            print(password)
            self.error_output = 'Success'
            #time.sleep(10)
            App.get_running_app().stop()
            pr2kvloginApp().run()
            ################################################################################


class prSendApp(App):
    pass

if __name__ == '__main__':
    url_base = 'http://127.0.0.1:5000/'
    #global userx

    pr2kvloginApp().run()
    #prSendApp().run()
