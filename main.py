from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)


# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',  # Replace with your MySQL host
        user='root',  # Replace with your MySQL username
        password='root',  # Replace with your MySQL password
        database='pythondb'  # Replace with your MySQL database name
    )
    return connection


# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    name = data['name']
    email = data['email']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'User created successfully'}), 201


# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(users), 200


# Get user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user), 200


# Update user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    name = data['name']
    email = data['email']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET name = %s, email = %s WHERE id = %s', (name, email, id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'User updated successfully'}), 200


# Delete user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'User deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
