from flask import Flask, render_template, request, redirect, url_for, Response
import requests
import os
import keras
import cv2
import numpy as np
import pafy
from models import preds

app = Flask(__name__)

global url
global best
url = ""

copyrighted = False
print(os.getcwd())
k_model = keras.models.load_model('.\model\model.h5')

def gen_frames():
    # cap = cv2.VideoCapture(best.url)
    cap = cv2.VideoCapture(url)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    global url
    global best
    if request.method == 'POST':
        video_url = request.form['url']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        video_id = video_url.split('v=')[-1]
        url = 'https://www.youtube.com/watch?v=' + video_id
        
        # videoitem = pafy.new(url)
        # best = videoitem.getbest(preftype="mp4")

        embedded_video_url = f'https://www.youtube.com/embed/{video_id}?start={start_time}&end={end_time}'


        print(url)
        copyright = preds[max(k_model.predict(np.array([int(start_time), int(end_time)])))]


        return render_template('demo.html', video_url=embedded_video_url, copyright=copyright)

    return render_template('demo.html')

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")



if __name__ == '__main__':
    app.run(debug=True)
