from flask import Flask, render_template, request, redirect

import mysql.connector



app = Flask(__name__)

conn=mysql.connector.connect(
    host='localhost',
    user='root',
    password="your_password",
    database="movie_review_db"
)
cursor=conn.cursor()

@app.route("/")
def index():
    cursor.execute("select * from movie_reviews")
    reviews=cursor.fetchall()
    return render_template("index.html", reviews=reviews)


@app.route("/add", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        review = request.form.get("review")
        rating = request.form.get("rating")  
        
        cursor.execute(
          
               "insert into movie_reviews(title,description,review,rating) values(%s,%s,%s,%s)",(title,description,review,rating)
        )
        conn.commit()
        return redirect("/")
    
    return render_template("add.html")


@app.route("/delete/<int:id>")
def delete_review(id):
    cursor.execute(
        "delete from movie_reviews where id=%s",(id,)
    )
    conn.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_review(id):
    cursor.execute("select * from movie_reviews where id=%s",(id,) )
    review = cursor.fetchone()

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        review_text = request.form.get("review")
        rating = request.form.get("rating")
        
        cursor.execute("update movie_reviews set title=%s,description=%s,review=%s,rating=%s where id=%s",(title,description,review_text,rating,id))
        conn.commit()
        return redirect("/")

    return render_template("edit.html", review=review)


if __name__ == "__main__":
    app.run(debug=True)
