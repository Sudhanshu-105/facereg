from genericpath import isfile
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS, cross_origin
import os
from PIL import Image
from camera import run

app = Flask(__name__)
cors = CORS(app)
app.config["UPLOAD_FOLDER"] = "static\\uploads"
app.config["CORS_HEADERS"] = "Content-Type"
HOME = "http://127.0.0.1:5000" 
@app.route('/')
def main():
    return "Hello Wjorld!"






@app.route('/save_image', methods=['POST'])
@cross_origin()
def save_image():
    '''
    Save the Blob Image data received in response to local folder
    '''
    if request.method == 'POST':

        # Get image from request as blob
        image_blob = request.files['file']
        image_name = "doc"
        img = Image.open(image_blob)
        img.save(image_name+".png")
        os.rename(image_name+".png", "static\\uploads\\"+image_name+".png")
        faces_paths = run("static\\uploads\\"+image_name+".png")
        os.remove("static\\uploads\\"+image_name+".png")
        return jsonify({'success': True, "faces" : [f for f in faces_paths]}), 200
    return jsonify({"success": False})

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    if request.method=="POST":
        img_path = request.form["image"]
        img_name = request.form['name']
        print(img_name, img_path)
        img_local_path = img_path.replace(HOME, "")[1:]
        if os.path.isfile("static\\saved\\"+img_name+".png"):
            os.remove("static\\saved\\"+img_name+".png")
        os.rename(img_local_path, "static\\saved\\"+img_name+".png")
        return jsonify({"success": True}), 200
    return jsonify({"success": False}), 400

@app.route("/fetch", methods=["GET"])
@cross_origin()
def fetch_image():
    """
    Fetch image from static folder and return URLs in JSON
    """
    if request.method == "GET":
        path = "static\\saved"
        
        images = os.listdir(path)
        image_urls = []
        for image in images:
            
            image_urls.append(HOME + url_for("static", filename="saved/" + image))
        print(image_urls)
        return jsonify({"success": True, "images": [ {"name" : images[i] , "url" : image_urls[i]} for i in range(len(images)) ]})
    return jsonify({"success": False})

app.run()