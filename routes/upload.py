from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
import uuid
from services.cloudinary_service import upload_image

upload_bp = Blueprint("upload",__name__)

UPLOAD_FOLDER = "uploads" 
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS ={'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/upload", methods=["POST"])
def upload_file():

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file= request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):

        try:
            #Subir a Cloudinary
            cloudinary_url = upload_image(file)

            return jsonify({"url": cloudinary_url}),200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            

    return jsonify({"error": "File type not allowed"}), 400



