import json
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flaskext.mysql import MySQL

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST')

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def get_start():
    return jsonify({"msg": "Hello world!"})

@app.route('/map/markers', methods=['GET'])
def get_markers():
    worldName = request.args.get('world')

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grnMarkerFiles")
    rows = cursor.fetchall()

    worldChoose = list(filter(lambda item: item[0] == worldName, rows))
    worldChooseTuple = worldChoose[0][1]
    world = json.loads(worldChooseTuple)
    print(type(world))
    # data = json.loads(json_string)
    return jsonify(world['sets'])


if __name__ == '__main__':
    app.run(debug=True)
