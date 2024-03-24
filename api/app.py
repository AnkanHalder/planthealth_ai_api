from flask import Flask,jsonify,request as req
from flask_cors import CORS
from gradio_client import Client,file
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
CORS(app)


def get_predictions(image_file):
    client = Client("midknight2002/happy_leaf",hf_token=os.environ.get('HUGGINGFACE_TOKEN'))
    print("CLIENT LOADED")
    result = client.predict(
        file(image_file),
        api_name="/predict"
    )
    print("PREDICTION MADE")
    print(result)
    return {
            "type" : result[0],
            "disease" : result[1],
            "cure": result[2]
    }



@app.errorhandler(Exception)
def handle_error(err):
    print(err)
    message = str(err)
    code = 500  # Internal Server Error (adjust based on error type)
    return jsonify({'success': False, "error": message}), code

@app.route('/')
def index():
    return {
        "message": "Welcome to API for Planthealth AI"
    }

@app.route("/api/predict_image", methods=["POST"])
def predict_image():
    if req.method == 'POST':
        if 'image' not in req.files:
            return jsonify({'success': False, 'error': 'Missing image file'}), 400  # Bad Request
        image_file = req.files['image']
        filename = secure_filename(image_file.filename)
        path_ = os.path.join(app.config["UPLOAD_FOLDER"], filename )
        image_file.save(path_)
        res=get_predictions(path_)
        os.remove(path_)

        return jsonify({'success': True , "predictions" : res }), 200  # OK

    else:
        return jsonify({'error': 'Method Not Allowed'}), 405  # Method Not Allowed


app.run()
