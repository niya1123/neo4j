from flask import Flask, jsonify
import sys
sys.path.append("/dic/neo4j")

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return jsonify({'message': 'Hello world'})
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7878, debug=True)