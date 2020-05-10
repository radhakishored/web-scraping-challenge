from flask import Flask, render_template, redirect
import pymongo
import scrape_mars
from flask_cors import CORS



# Create an instance of Flask
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.MARS

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_info = db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)


# Route that will trigger the scrape function
@app.route("/scrape")
# Run the scrape function
def scrape():

    db_mars_info = db.mars_info
    mars_info = scrape_mars.scrape()
    print(mars_info)
    # Update the Mongo database using update and upsert=True
    db_mars_info.update({}, mars_info, upsert=True)
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)