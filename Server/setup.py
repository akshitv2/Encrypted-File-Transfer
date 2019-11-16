import pickle

keyauth={}
keyauth['angel']='death'
file_Name = "testfile"
fileObject = open(file_Name,'wb')
pickle.dump(keyauth,fileObject)
fileObject.close()
