from flask import Flask, request, jsonify
import os
import csv
import re

app = Flask(__name__)
port = 8000

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        inputJSON = request.json;
        fileName = inputJSON.get('file')
        inputProduct = inputJSON.get('product')
        print(fileName, inputProduct)
        #parent_dir = os.path.dirname(app.root_path)  # Get the parent directory of the application root
        #data_dir = os.path.join(parent_dir, 'data')  # Get the path to the 'data' directory
        file_path = os.path.join("/Shravanthi_PV_dir", fileName) 
        print('filepath in container2', file_path)
        #return jsonify({"file": fileName, "path exists": os.path.exists(file_path)})
        #return jsonify(response.json())
        with open(file_path, 'r') as file:
            sum = 0
            for line_number, line in enumerate(file, start=2):
                parts = line.strip().split(",")
                if len(parts) != 2:
                    return jsonify({"file": fileName, "error": "Input file not in CSV format."})
                else:
                    product, amount = parts
                    if product == inputProduct:
                        sum += int(amount.strip())
            print('file', fileName, 'sum', sum)
            return jsonify({"file": fileName, "sum": sum})
    except:
        return jsonify({"file": fileName, "error": "Input file not in CSV format."})
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)