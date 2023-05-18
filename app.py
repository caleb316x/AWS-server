from flask import Flask, render_template, request, redirect, url_for, send_from_directory,session
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
import os
import base64
from waste_classify import AWS
from AWSdatabase import UserDB

app = Flask(__name__)
bootstrap = Bootstrap5(app)


# Route to upload image
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    try:
        if request.method == 'POST':
            print("POST request")
            
            file = request.files['imageFile']
            file_size = file.content_length
            print(f"The file size is {file_size} bytes.")
            
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                print("Image uploaded successfully")
                return aws.classify_image("uploads/esp32-cam.jpg")

                return "Image uploaded successfully"
            else:
                print("No Image")
                return "No Image"

        else:
            print("GET request")
            db = UserDB()
            data = db.getStatusall()
            d = data[0]

            binfull = False

            if d[2] == "100.00" or d[3] == "100.00" or d[4] == "100.00" or d[5] == "100.00":
                binfull = True
                
            # return render_template('upload.html')
            return render_template('index.html',data=data, binfull=binfull)
    
    except Exception as e: print(e); return "Has Error"

# Route to show uploaded image
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/predict', methods=['GET'])
def image_predict():
    waste_class = aws.classify_image("uploads/esp32-cam.jpg")
    return(waste_class)

@app.route('/newaws/<id>', methods=['GET'])
def add_aws(id):
    db = UserDB()
    data = db.addNewAWS(id)
    # print("New AWS added")
    return data

@app.route('/updateaws/<id>', methods=['GET'])
def update_aws(id):
    args = request.args
    db = UserDB()
    data = db.UpdateData((args.get("plastic"),args.get("waste"),args.get("paper"),args.get("metal"),args.get("battery"),str(id)))
    print("Record Updated successfully")
    return data

@app.route('/updateaws/<id>/<bin>', methods=['GET'])
def update_single_aws(id,bin):
    args = request.args
    db = UserDB()
    data = db.UpdateSingleData((args.get(bin),args.get("battery"),str(id)),bin)
    print("Record Updated successfully")
    return data

@app.route('/list', methods=['GET'])
def list_aws():
    db = UserDB()
    return db.getStatusall()

@app.route('/awsget/<id>', methods=['GET'])
def get_aws(id):
    db = UserDB()
    data = db.getStatus(id)
    return data

if __name__ == '__main__':
    aws = AWS()
    db = UserDB()

    # Define the folder to store uploaded images
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(host='192.168.254.105', port=80,debug=True)
