from flask import Flask, request, render_template
import json, string
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.Items_db
collection = db.extens

@app.route("/")
def datagrid():
    return render_template("Items.html")

@app.route("/Mongo_get", methods=['GET', 'POST'])
def Mongo_get():
    app.logger.info('Mongo_get')
    data = collection.find()
    rowscount = data.count()
    app.logger.info(rowscount)
    resultarray = {}
    resultarray["total"] = data.count()
    resultarray["rows"] = []
    for record in data: 
        record['_id'] = str(record['_id'])
        app.logger.info(record)
        resultarray["rows"].append(record)
    return json.dumps(resultarray)	
	
@app.route("/Mongo_save", methods=['GET', 'POST'])
def Mongo_save():
    app.logger.info('Mongo_save')
    save_data = {"ID": "1", "NAME": "%s" % request.form['NAME']}
    app.logger.info(request.form)
    collection.insert(save_data) 
    resultarray = {}
    return json.dumps(resultarray)		
	
@app.route("/Mongo_destroy", methods=['GET', 'POST'])
def Mongo_destroy():
    app.logger.info('Destroy')	
    id_row = request.form['_id']
    app.logger.info(request.form)
    collection.remove({"_id":ObjectId(id_row)})
    resultarray = {}
    resultarray["success"] = True
    return json.dumps(resultarray)		
	
@app.route("/Mongo_update", methods=['GET', 'POST'])
def Mongo_update():	
    app.logger.info('Mongo_update')
    id_row = request.args['_id']
    app.logger.info(request.args)
    collection.update({"_id":ObjectId(id_row)}, {'$set':{ "NAME": "%s" % request.form['NAME'] }})
    resultarray = {}
    return json.dumps(resultarray)	
	
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5010,debug=True)
