from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS, cross_origin
import os
from PIL import Image
from local_db import flush_database
from local_db import verify_or_create_folders
from local_db import save_face
from camera import run
import json

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
        verify_or_create_folders()
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
        img_data = request.form
        t = save_face(img_data)
        if t  == True:
            return jsonify({"success": True}), 200
        return jsonify({"success": False, "resp" : t}), 403
    return jsonify({"success": False}), 400

@app.route("/fetch", methods=["GET"])
@cross_origin()
def fetch_image():
    """
    Fetch image from static folder and return URLs in JSON
    No Maximum Cap as of now
    """
    if request.method == "GET":
        path = "static\\saved"
        
        images = os.listdir(path)
        images.remove("data.json")
        image_urls = []
        for image in images:    
            image_urls.append(HOME + url_for("static", filename="saved/" + image))
        with open("static\\saved\\data.json", "r") as f:
            data = json.load(f)
        
        if len(data["face"]) != len(image_urls):
            return jsonify({"success": False}), 504
        return jsonify({"success": True, "images": [ {"name" : data["face"][i]["person_name"] , "url" : image_urls[i]} for i in range(len(images)) ]})
    return jsonify({"success": False})


@app.route("/remove", methods=["GET"])
@cross_origin()
def remove_face():
    if request.method == "GET":
        face_id = int(request.args.get("face_id"))
        with open("static\\saved\\data.json", "r") as f:
            data = json.load(f)
        temp_data = data.copy()
        status = 0
        try:
            for i in range(len(data["face"])):
                if data["face"][i]["face_id"] == face_id:
                    data["face"].pop(i)
                    status = 1
                    break
            with open("static\\saved\\data.json", "w") as f:
                json.dump(data, f, indent=4)
            return jsonify({"success": True, "status" : status}), 200
        except Exception as e:
            print(e)
            with open("static\\saved\\data.json", "w") as f:
                json.dump(temp_data, f, indent=4)
            return jsonify({"success": False}), 400

@app.route("/annihilate", methods=["GET"])
@cross_origin()
def flush_db():
    if request.method == "GET":
        flush_database()
        return jsonify({"success": True}), 200
    return jsonify({"success": False}), 400
app.run()