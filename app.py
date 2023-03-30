from pymongo import MongoClient
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)


def connect():
    connection_string = "mongodb+srv://duongtd:1234@cluster0.3s3sfxy.mongodb.net/test"
    client = MongoClient(connection_string)
    blog_db = client["blog"]
    return blog_db["post"]  # collection


"""
posts = {
    0: {
        "title": "Python",
        "content": " Learning python with Duong"
    }
}
 """

def get_posts():
    col = connect()
    posts = col.find()
    new_posts = {}

    for x in posts:
        for k in x:
            if k != '_id':
                new_posts[int(k)] = x[k]

    return new_posts


@app.route("/")
def home():
    new_posts = get_posts()
    return render_template("index.jinja2", posts=new_posts)


@app.route("/post/<int:post_id>")
def create_post(post_id):
    posts = get_posts()
    post = posts.get(post_id)
    if not post:
        return render_template("404.jinja2", msg=f"A post with id {post_id} was not found")
    return render_template("post.jinja2", post=post)


@app.route("/post/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        posts = get_posts()
        title = request.form.get("title")
        content = request.form.get("content")

        post_id = str(len(posts))
        col = connect()
        col.insert_one({post_id: {"title": title, "content": content}})
        return redirect(url_for('create_post', post_id=post_id))
    return render_template("create.jinja2")


if (__name__ == '__main__'):
    app.run(debug=True)
