import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, Response)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import json
import sys
import logging

if os.path.exists("env.py"):
    import env


#app = Flask(__name__)

app=Flask(__name__,template_folder='templates')


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    tasks = list(mongo.db.testBooks.find())
    return render_template("tasks.html", tasks=tasks)
    #return render_template("base.html", tasks=tasks)

@app.route("/get_biography")
def get_biography():
    result_bio = mongo.db.testBooks.find({
    "Category" : { "$eq" : "Biography"}})
    return render_template("book_by_category.html", result_1=result_bio)


@app.route("/get_history")
def get_history():

    result_hist = mongo.db.testBooks.find({
    "Category" : { "$eq" : "History"}})
    return render_template("book_by_category.html", result_1=result_hist)

@app.route("/get_scifi")
def get_scifi():

    result_scifi = mongo.db.testBooks.find({
    "Category" : { "$eq" : "SciFi"}})
    return render_template("book_by_category.html", result_1=result_scifi)

@app.route("/get_fantasy")
def get_fantasy():
    result_fantasy = mongo.db.testBooks.find({
    "Category" : { "$eq" : "Fantasy"}})
    return render_template("book_by_category.html", result_1=result_fantasy)

@app.route("/get_thriller")
def get_thriller():
    result_thriller = mongo.db.testBooks.find({
    "Category" : { "$eq" : "Thriller"}})
    if len(list(result_thriller))==0:
       result_thriller=" "
    return render_template("book_by_category.html", result_1=result_thriller)


@app.route("/delete_bk")
def delete_bk():
    lists = list(mongo.db.testBooks.find())
    return render_template("delete_book.html", lists=lists)

@app.route("/add_or_delete_bk" ,methods=['GET', 'POST'])
def add_or_delete_bk():

    if request.method == "POST":
       
        task = {
            "Category": request.form.get("Category"),
            "book_name": request.form.get("book_name"),
            "book_summary": request.form.get("book_summary"),
            "Author": request.form.get("Author"),
            "book_cover": request.form.get("book_cover"),
            "Number_of_Reviews": 0,
            "review": []
        }
        added_new_rec = mongo.db.testBooks.insert_one(task)
        if  added_new_rec:
            try:
        
                flash("Book has been added")


            except Exception as ex:
                print("*********")
                print(ex)
                print("******")
                return Response(
                    response= json.dumps(
                        {"message":"sorry cannot add record"}),
                    status=500,
                    mimetype="application/json"
            )
            return redirect("/")
          
    
    return render_template('upload_delete_books.html')

  
@app.route('/view_add_review', methods=['GET', 'POST'])
def view_add_review():
    if request.method == 'GET':
        return render_template("view_add_review.html")

    if request.method == 'POST':
        book_id = request.form['book_id']
        book = list(mongo.db.testBooks.find({"_id" : ObjectId(book_id)}))
        
        return render_template("view_add_review.html", bk=book)

@app.route("/write_review", methods=['GET','POST'])
def write_review():  
    if request.method == 'GET':
        return render_template("write_review.html")

    if request.method == 'POST':
        bookid = request.form['bookid']
       
        return render_template("write_review.html", bkid=bookid)

@app.route("/delete_book", methods=['POST'])
def delete_book():
    test1='inside start of delete book function'
    try:
        delbkid = request.form['book_id']
        dbResponse = mongo.db.testBooks.delete_one({"_id" : ObjectId(delbkid)})
        if dbResponse.deleted_count == 1:
            lists = list(mongo.db.testBooks.find())
            return render_template("delete_book.html", lists=lists)
    
            #return render_template("tasks.html")
           # return Response(
           #     response= json.dumps(
           #     {"message":"book deleted"}),
           #     status=200,
           #     mimetype="application/json"
           # )     
           # return Response(
           #     response= json.dumps(
           #     {"message":"book not found"}),
           #     status=200,
           #     mimetype="application/json"
           # )
    except Exception as ex:
        print(ex)
        return Response( 
            response= json.dumps(
            {"message":"sorry cannot delete the book"}),
            status=500,
            mimetype="application/json"
        )
    #return render_template("delete_book.html")
    lists = list(mongo.db.testBooks.find())
    return render_template("delete_book.html", lists=lists)
    delete_bk()


@app.route("/submit_review", methods=['GET','POST'])
def submit_review():
    if request.method == 'POST':

        bkid = request.form['bkid']
        bookreview = request.form['writeReviewForm']
        review_add_id = mongo.db.testBooks.find({"_id" : ObjectId(bkid)})
        if  review_add_id:
            try:
                #got the update review array using $push from site https://docs.mongodb.com/manual/reference/operator/update/push/
                dbResponse = mongo.db.testBooks.update_one({"_id" : ObjectId(bkid)},{"$push" : {"review": bookreview}})

                flash("Review has been added")

            except Exception as ex:
                print("*********")
                print(ex)
                print("******")
                return Response(
                    response= json.dumps(
                        {"message":"sorry cannot update record"}),
                    status=500,
                    mimetype="application/json"
            )
 
            return redirect('/')

 
@app.route("/check_selected", methods=['GET','POST'])
def check_selected():
    global selected
    getbkid = request.form['booksid']
    #if getbkid == 0:
    post = request.args.get('post', 0, type=int)
    return json.dumps({'selected post': str(post)});


@app.route('/update/<id>/<review>' , methods=['GET', 'POST'])
def update(id,review):

    review_bk_id = id
    review_bk_update = review
    review_bk_update1 = request.form.get("review")
    if request.method == "POST":
     
        review_bkid = mongo.db.books.find({"_id" : ObjectId(review_bk_id)})
        
        if review_bkid:
        
            try:
                
                print(review_bk_id)
                print(review_bk_update1)
             
                
                #mongo.db.testBooks.update_one({'_id': review_bk_id, 'review': { "$elemMatch": {"$set": {"review.$": review_bk_update1}}}})
                #mongo.db.testBooks.update_one({'_id': ObjectId("625d5030e92aadbab8e547bb"), 'review': { "$elemMatch": {"$set": {"review.$": review_bk_update1}}}})
                #$set: { "grades.$[element]"
                #mongo.db.testBooks.update_one({'_id': ObjectId("625d5030e92aadbab8e547bb")},{"$set": {"review.$[element]": review_bk_update1}} , {'arrayFilters': [{'element._id': 3}]},update=True)
                #mongo.db.testBooks.update_one({'_id': ObjectId("625d5030e92aadbab8e547bb") },submit)
                mongo.db.testBooks.update_one({'_id': ObjectId(id), 'review': review},{"$set": {"review.$": review_bk_update1}})
         
                return redirect('/view_add_review')
     
               #db.employees.updateMany({_id:5},{$set:{ skills:["Sales Tax"]}})
               #db.testBooks.update_one({"_id" : review_bk_id},{"$set": { "review":["Sales Tax"]}})

                #db.testBooks.updateMany({"_id" : review_bk_id},{"$set": { "review":["Sales Tax"]}})
                
                #db.testBooks.arrays.update({'_id': review_bk_id, 'review': { $['1']: {"$set": {"review.$": review_bk_update}}}})
                #db.testBooks.arrays.update({'_id': review_bk_id, 'review[1]': { "$elemMatch": {"$set": {"review.$": review_bk_update}}}})
            except:
                return "There was a problem updating that record"
    else:
        return render_template('update.html', review_bk_id=review_bk_id, review_bk_update=review_bk_update)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
            