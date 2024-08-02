from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/generate-matchups', methods=['GET'])
def get_matchups():
    return jsonify({'message': 'Hello from Flask!'})

@app.route('/get-schedule', methods=['GET'])
def run_solver():
    return jsonify({'message': 'Hello again'})

if __name__ == '__main__':
    app.run(debug=True)
