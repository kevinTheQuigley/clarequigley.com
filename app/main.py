from flask import Flask,render_template
import requests



app = Flask(__name__)

@app.route("/")
def home():
    blogData = requests.get("https://api.npoint.io/16c047af2b016b24c4fa").json()
    return(render_template("index.html",blog = blogData))

@app.route("/about/")
def about():
    return(render_template("about.html"))

@app.route("/gallery/")
def gallery():
    return(render_template("gallery.html"))

@app.route("/contact/")
def contact():
    return(render_template("contact.html"))

@app.route("/blogPost/<int:id>")
def returnBlogpost(id):
    blogData = requests.get("https://api.npoint.io/16c047af2b016b24c4fa").json()
    return(render_template("post.html",blog = blogData[int(id)-1]))

@app.route("/gallery/<int:id>")
def returnGalleryID(id):
    blogData = requests.get("https://api.npoint.io/16c047af2b016b24c4fa").json()
    return(render_template("post.html",blog = blogData[int(id)-1]))


while __name__ =="__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    blogData = requests.get("https://api.npoint.io/16c047af2b016b24c4fa")
    app.run(debug=True)


#<a href="{{url_for('about')}}">Read</a>
#          <a href="{{url_for('get_blog', id =blogPost['id'])}}">Read</a>
