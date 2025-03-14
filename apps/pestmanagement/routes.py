from flask import request, jsonify, current_app
from apps.pestmanagement import blueprint
from apps.pestmanagement.pestmanagement import inference_pests
import os

@blueprint.route('/pests', methods=['POST'])
def pests():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image = request.files['image']
    
    # Ensure the uploads directory exists
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    image_path = os.path.join(upload_folder, image.filename)
    image.save(image_path)
    
    result = inference_pests(image_path)
    return jsonify({"pest": result})