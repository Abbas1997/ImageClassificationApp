from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
import os
import random

model = load_model('save_at_15.h5')

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('ui.html')

@app.route('/upload', methods=['POST'])
def upload_file(): 
    f = request.files['pic']
    fname = 'uploaded.jpg'
    #f.save('static/' + fname)
    f.save(fname)
    img = keras.preprocessing.image.load_img(
        fname, target_size=(256,256)
    )

    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) 

    predictions = model.predict(img_array)
    score = predictions[0]
    rs = "This image is likely to be  %.2f percent fake and %.2f percent real."%(100 * (1 - score), 100 * score)
    rdict = {
        "verdict": rs
    }
    return rdict

@app.route('/rurls')
def random_urls():
    l = os.listdir('./static/fake')
    furl1 = random.sample(l,2)
    lr = os.listdir('./static/real')
    rurl1 = random.sample(lr,2)
    rurls = {
        'furl1' : furl1[0],
        'furl1r': fake_check(furl1[0]),
        'furl2' : furl1[1],
        'furl2r': fake_check(furl1[1]),
        'rurl1' : rurl1[0],
        'rurl1r' : real_check(rurl1[0]),
        'rurl2' : rurl1[1],
        'rurl2r':real_check(rurl1[1])
    }
    return rurls


def fake_check(x):
    img = keras.preprocessing.image.load_img(
        './static/fake/'+x, target_size=(256,256)
    )

    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) 

    predictions = model.predict(img_array)
    score = predictions[0]
    rs = "This image is likely to be %.2f percent fake and %.2f percent real."%(100 * (1 - score), 100 * score)
    return rs

def real_check(x):
    img = keras.preprocessing.image.load_img(
        './static/real/'+x, target_size=(256,256)
    )

    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) 

    predictions = model.predict(img_array)
    score = predictions[0]
    rs = "This image is likely to be %.2f percent fake and %.2f percent real."%(100 * (1 - score), 100 * score)
    return rs

