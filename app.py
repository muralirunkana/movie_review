from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
client = MongoClient("mongodb+srv://murali:murali2003@moviereviewdb.jdubn1d.mongodb.net/movie_db?retryWrites=true&w=majority&appName=MovieReviewDB")
db = client.movie_db
collection = db.reviews

# MongoDB connection
# client = MongoClient("mongodb://localhost:27017/")
# db = client["movie_db"]
# collection = db["reviews"]

@app.route("/")
def index():
    reviews = list(collection.find())
    return render_template("index.html", reviews=reviews)


@app.route("/add", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        review = request.form.get("review")
        rating = request.form.get("rating")  
        
        collection.insert_one({
            "title": title,
            "description": description,
            "review": review,
            "rating": rating
        })
        return redirect("/")
    
    return render_template("add.html")


@app.route("/delete/<id>")
def delete_review(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect("/")

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_review(id):
    from bson.objectid import ObjectId
    review = collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        review_text = request.form.get("review")
        rating = request.form.get("rating")
        
        collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "title": title,
                "description": description,
                "review": review_text,
                "rating": rating
            }}
        )
        return redirect("/")

    return render_template("edit.html", review=review)


if __name__ == "__main__":
    app.run(debug=True)
