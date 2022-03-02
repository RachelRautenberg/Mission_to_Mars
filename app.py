from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

add = Flask(__name__)

# Use flask_pymongo to set up mongo collection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    return rediret('/', code=320)

if __name__ = "__main--":
    app.run()