import os
import json

HOME = "http://127.0.0.1:5000" 

def save_face(image_data):
    img_name = image_data["name"]
    img_path = image_data["image"]
    #Further data can be extracted here and added to a dict
    img_id = get_id(image_data)
    img_local_path = img_path.replace(HOME, "")[1:]
    
    image_dict = {
        "face_id": img_id,
        "person_name" : img_name,
        "headshot" : "static\\saved\\"+img_name+".png"
    }
    # Save this to data.json
    with open("static\\saved\\data.json", "r") as f:
        data = json.load(f)
    temp_data = data.copy()
    try:
        
        data["face"].append(image_dict)
        
        if os.path.isfile("static\\saved\\"+str(img_id)+".png"):
            os.remove("static\\saved\\"+str(img_id)+".png")
        os.rename(img_local_path, "static\\saved\\"+str(img_id)+".png")
        with open("static\\saved\\data.json", "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        with open("static\\saved\\data.json", "w") as f:
            json.dump(temp_data, f, indent=4)
        return e.__str__()
    

def get_id(image_data):
    # Temporary assigned incremental indexing, can be replaced with a hash function
    with open("static\\saved\\data.json", "r") as f:
        data = json.load(f)
    if len(data["face"]) == 0:
        return 1
    return data["face"][-1]["face_id"]+1