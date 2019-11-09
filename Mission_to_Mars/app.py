from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#establish connection Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    collection = mongo.db.collection.find_one()
    # Find one record of data from the mongo database

    # Return template and data
    return render_template("index.html", mars=collection)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    collection = mongo.db.collection    
    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    collection.replace_one({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
