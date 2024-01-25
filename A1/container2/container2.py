from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)
port = 8000

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        inputJSON = request.json;
        fileName = inputJSON.get('file')
        inputProduct = inputJSON.get('product')
        print(fileName, inputProduct)
        file_path = os.path.join('./data/', fileName)
        print(file_path)
        
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  
            if header == ['product', 'amount']:
                sum = 0
                for line in reader:
                    product, amount = line
                    if product == inputProduct:
                        sum = sum + int(amount)
                print('file', fileName, 'sum', sum)
                return jsonify({"file": fileName, "sum": sum})
            else:
                return jsonify({"file": fileName, "error": "Input file not in CSV format."})
    except Exception as e:
        return jsonify({"file": fileName, "error": "Input file not in CSV format."})
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)