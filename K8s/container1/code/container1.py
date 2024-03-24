from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
port = 6000

def store_file_in_storage(file_name, data):
    #parent_dir = os.path.dirname(app.root_path)  # Get the parent directory of the application root
    #data_dir = os.path.join(parent_dir, 'data')  # Get the path to the 'data' directory
    try:
        if not os.path.exists('/Shravanthi_PV_dir'):
            os.makedirs('/Shravanthi_PV_dir')
        file_path = os.path.join('/Shravanthi_PV_dir', file_name)     
        #os.makedirs('./data', exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(data)
        return True
    except Exception as e:
        print(e.message)  # Print the error for debugging purposes
        return False

@app.route('/store-file', methods=['POST'])
def store():
    if not request.is_json:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400
    request_data = request.json

    if 'file' not in request_data or 'data' not in request_data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    # Extract file name and data from JSON
    file_name = request_data['file']
    data = request_data['data']
    
    if file_name == None or file_name == "":
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    # Store file in GKE persistent storage
    if store_file_in_storage(file_name, data):
        return jsonify({"file": file_name, "message": "Success."}), 200
    else:
        return jsonify({"file": file_name, "error": "Error while storing the file to the storage."}), 500


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        inputJSON = request.json
        file = inputJSON.get('file')
        print(file)
        file_path = os.path.join('/Shravanthi_PV_dir', file)    
        print('file_path',file_path)
        print(file == None)
        if file != None:            
            if not os.path.exists(file_path):
                return jsonify({"file": file, "error": "File not found."})
            elif os.path.exists(file_path):
                print('calling container2')
                response = requests.post('http://app2-service:8000/calculate', json=inputJSON)
                return jsonify(response.json())
        else:
            return jsonify({"file": file, "error": "Invalid JSON input."})

    except Exception as error:
        return jsonify({"file": file, "error": "Invalid JSON input."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
