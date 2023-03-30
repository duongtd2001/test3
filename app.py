from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

posts = {
    0: {
        "title": "Python",
        "content": " Learning python with Duong"
    }
}


@app.route("/")
def home():
    return render_template("index.jinja2", posts=posts)


@app.route("/post/<int:post_id>")
def create_post(post_id):
    post = posts.get(post_id)
    if not post:
        return render_template("404.jinja2", msg=f"A post with id {post_id} was not found")
    return render_template("post.jinja2", post=post)


@app.route("/post/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        post_id = len(posts)
        posts[post_id] = {"title": title, "content": content}
        return redirect(url_for('create_post', post_id=post_id))
    return render_template("create.jinja2")


if (__name__ == '__main__'):
    app.run(debug=True)
