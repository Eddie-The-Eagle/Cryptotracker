from flask import Flask
from flask_restful import Resource, Api
import io
import json

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
	def get(self):
		with io.open('/home/ExchangeData/APIData.json', 'r', encoding='utf8') as outfile:
			outfileRead = outfile.read() 
			ShortList = json.loads(outfileRead)
			return ShortList

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0',port=5000)