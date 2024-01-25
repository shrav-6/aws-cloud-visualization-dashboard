from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
port = 6000

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        inputJSON = request.json
        file = inputJSON.get('file')
        print(file)
        file_path = os.path.join('./data/', file)
        print('file_path',file_path)
        print(file == None)
        if file != None:            
            if not os.path.exists(file_path):
                return jsonify({"file": file, "error": "File not found."})
            elif os.path.exists(file_path):
                print('calling container2')
                response = requests.post('http://container2:8000/calculate', json=inputJSON)
                return jsonify(response.json())
        else:
            return jsonify({"file": file, "error": "Invalid JSON input."})

    except Exception as error:
        return jsonify({"file": file, "error": "Invalid JSON input."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
