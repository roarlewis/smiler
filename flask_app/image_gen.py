from flask import Flask
from flask import request
from flask import send_file
from image_generator import process_image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/convert-image/')
def convert_image():

    # Could do this later ...
    # if not url:
    #     render_template('error.html',500)

    target_url = request.args.get('url')

    converted_image = process_image.process_image(target_url)

    # process the file ...
    
    # converted_image.seek(0)

    thing = BytesIO(converted_image)

    return send_file(
        thing,
        mimetype="image/jpeg",
        as_attachment=False
    )