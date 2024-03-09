from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

write_db_config = {
    'host': 'database-1-instance-1.c14me2g0yet1.us-east-1.rds.amazonaws.com', #endpoint of writer instance
    'user': 'admin', #user
    'password': 'admin123456', #password
    'db': 'clouddatabase', #db name
    'port': 3306
}

read_db_config = {
    'host': 'database-1-instance-1.c14me2g0yet1.us-east-1.rds.amazonaws.com', #endpoint of writer instance
    'user': 'admin', #user
    'password': 'admin123456', #password
    'db': 'clouddatabase', #db name
    'port': 3306
}

def execute_query(config, query, read=True):
    connection = pymysql.connect(**config) #connects to the configurations
    cursor = connection.cursor() #get cursor
    cursor.execute(query) #execute usiong the cursor
    if read:
        result = cursor.fetchall() #for read
    else:
        result = None # for write
    connection.commit()
    connection.close() #close connection 
    return result

'''def create_table(): #for testing purpose only
    query = """
    CREATE TABLE IF NOT EXISTS products (
        name VARCHAR(100),
        price VARCHAR(100),
        availability BOOLEAN
    );
    """
    execute_query(write_db_config, query, read=False)

create_table()'''

@app.route('/store-products', methods=['POST']) #to store the values in db
def write_data():
    data = request.get_json()['products'] #list
    insert_queries = []

    try: 
        for product in data:
            name = product['name']
            price = product['price']
            availability = product['availability']
            query = f"INSERT INTO products (name, price, availability) VALUES ('{name}', '{price}', {availability});" #create insert statements
            insert_queries.append(query)

        for query in insert_queries: #execute each insert statement
            execute_query(write_db_config, query, read=False)
        return jsonify({'message': 'Success.'})
    
    except Exception as e:
        return jsonify({'message': 'Error: ' + str(e)}), 500

@app.route('/list-products', methods=['GET']) #get details from table
def read_data():
    query = "SELECT * FROM products;"
    result = execute_query(read_db_config, query)
    expected_output = []
    for item in result:
        name = item[0]
        price = item[1]
        availability = bool(item[2]) #because it is stored as 0 or 1 -> converting to false or true
        formatted_product = {'name': name, 'price': price, 'availability': availability} #make dict
        expected_output.append(formatted_product) #add to list
    return jsonify({'products': expected_output})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
