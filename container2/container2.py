from flask import Flask, request, jsonify
import os

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
        print('file_path')
        
        with open(file_path, encoding='utf-8') as file:
            content = file.read()
            inputLines = content.split('\n')
            sum = 0
            for line in inputLines[1:]:  # Skip the header line
                values = line.split(',')                   
                product = values[0]
                amount = int(values[1])
                if product == inputProduct:
                    sum += amount
        
        print('file', fileName, 'sum', sum)
        return jsonify({"file": fileName, "sum": sum})
    except Exception:
        return jsonify({"file": fileName, "error": "Input file not in CSV format."})
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)