# mongo.py

from flask import Flask, render_template
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from pygelf import GelfTcpHandler, GelfUdpHandler, GelfTlsHandler, GelfHttpHandler
import logging




app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(GelfTcpHandler(host='127.0.0.1', port=12201))
logger.addHandler(GelfUdpHandler(host='127.0.0.1', port=12201))
logger.addHandler(GelfTlsHandler(host='127.0.0.1', port=12201))
logger.addHandler(GelfHttpHandler(host='127.0.0.1', port=12201))

logger.info('hello gelf')


app.config['MONGO_DBNAME'] = 'db_teste_itau1'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/db_teste_itau1'

mongo = PyMongo(app)

@app.route('/tweets', methods=['GET'])
def get_all_tweets():
  teste4 = mongo.db.teste4
  output = []
  for s in teste4.find():
    output.append({'user' : s['user'], 'date' : s['date']})
  return jsonify({'result' : output})

@app.route('/tweets/<user>', methods=['GET'])
def get_one_user(user):
  teste4 = mongo.db.teste4
  s = teste4.find_one({'user' : user})
  if s:
    output = {'user' : s['user'], 'date' : s['date']}
  else:
    output = "No such user"
  return jsonify({'result' : output})

@app.route('/followersmax', methods=['GET'])
def get_max_follower():
  teste4 = mongo.db.teste4
  s = teste4.find_one(sort=[("followers", -1)])
  if s:
    output = {'user' : s['user'], 'date' : s['date']}
  else:
    output = "No such user"
  return jsonify({'result' : output})

@app.route('/followersmax5', methods=['GET'])
def get_max_follower5():
  teste4 = mongo.db.teste4
  s = teste4.find(sort=[("followers", -1)])
  if s:
    output = {'user' : s['user'], 'date' : s['date']}
  else:
    output = "No such user"
  return jsonify({'result' : output})

@app.route('/star', methods=['POST'])
def add_star():
  star = mongo.db.stars
  name = request.json['name']
  distance = request.json['distance']
  star_id = star.insert({'name': name, 'distance': distance})
  new_star = star.find_one({'_id': star_id })
  output = {'name' : new_star['name'], 'distance' : new_star['distance']}
  return jsonify({'result' : output})


@app.route("/")
def home():
  return render_template("home.html")


@app.route("/about")
def about():
  return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)