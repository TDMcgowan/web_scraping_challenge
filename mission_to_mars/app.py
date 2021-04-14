from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)
 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars.find_one()
    # print(mars)
    return render_template("index.html", data=mars_data)

@app.route("/scrape")
def scrape():  
    mars_scrape = scrape_mars.scrape()
    print(mars_scrape)
    mongo.db.mars.update({}, mars_scrape, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)