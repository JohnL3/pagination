import os
from flask import Flask, request, render_template
from flask_pymongo import PyMongo

from helper_functions.pagination import paginate, filtering


app = Flask(__name__)
app.config['SECRET_KEY']=os.environ.get("SECRET_KEY")
app.config["MONGO_DBNAME"]=os.environ.get("MONGO_DBNAME")
app.config['MONGO_URI']=os.environ.get("MONGO_URI")

mongo=PyMongo(app)


# route showing how to do things if only pagination is required.
# This has no html template as it is only an example of what has to be done.
@app.route('/blog/posts')
def blog_posts():
    
    context = paginate(mongo, "posts", 2, 2, 'DESC')

    return render_template('blog.html', context=context)


# route showing how to do things if both pagination and filtering is required.
@app.route('/videos')
def videos():
    filtered = filtering(mongo, request, 'videos')
    
    if filtered[1]:
        return render_template('videos.html',  context=filtered[0], **filtered[2])
    else:
        return render_template("videos.html", context=filtered[0])