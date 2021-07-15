# Importing Requires Libraries

from flask import Flask , render_template,redirect,request
from flask_cors import cross_origin
# import logging # logging libraries is used to make log file 

import numpy as np
from keras.models import load_model
from keras.preprocessing import image 
from werkzeug.utils import secure_filename
import os
import datetime
import warnings
warnings.filterwarnings("ignore")

UPLOAD_FOLDER = 'static\\img\\upload'
# initialization of flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Initializing the log file
# logging.basicConfig(filename='log.txt', level = logging.DEBUG)



# creating index url

# index() takes get method by default and it will render the index.html template
@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/result',methods = ['POST'])
@cross_origin()
def result():
    if request.method == 'POST':


        file = request.files['img']
        if file:
            filename = secure_filename(file.filename)
            x = datetime.datetime.now()
            print(str(x)+filename)
            filename = str(x.year)+str(x.minute)+str(x.second)+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        images = image.load_img('static/img/upload/'+filename,target_size=(150,150))
        images = image.img_to_array(images)# changing in array
        images = np.expand_dims(images,axis = 0)
        images = images/255 # scaling the data
        model = load_model("dog_cat_model.h5")
        predicted = model.predict_classes(images)
        
        if predicted[0][0]==1:
            result = 'Dog'
        else:
            result = "Cat"
        
        img = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
                     
        return render_template('result.html',result = {"result":result,"image":img})

    else:
        return redirect('index.html')




# This is the main function of the python file...
if __name__ == '__main__':
    app.run(debug=True)