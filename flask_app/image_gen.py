from flask import Flask
from flask import request
from image_generator import process_image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/convert-image/<url>')
def convert_image(url):

    # Could do this later ...
    # if not url:
    #     render_template('error.html',500)

    converted_image = process_image(url)

    # process the file ...
    
    converted_image.seek(0)
    
    return send_file(
        converted_image,
        mimetype="image/jpeg",
        as_attachment=True,
        download_name="img.jpg"
    )


    
