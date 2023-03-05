from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    if request.method == 'POST':
        video_url = request.form['url']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        video_id = video_url.split('v=')[-1]
        embedded_video_url = f'https://www.youtube.com/embed/{video_id}?start={start_time}&end={end_time}'

        return render_template('demo.html', video_url=embedded_video_url)

    return render_template('demo.html')

if __name__ == '__main__':
    app.run(debug=True)
