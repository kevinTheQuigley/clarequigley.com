from flask import Flask, render_template, request
import requests
import smtplib
from arsewards import arsewards_dict
from flask_caching import Cache

app = Flask(__name__)

# Configure caching to store image data for quicker access
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Cached function to get photo data
@cache.cached(timeout=300)
def get_photo_data():
    return requests.get("https://api.npoint.io/af83026d4e0579fc5161").json()

@app.route("/")
def home():
    photoData = get_photo_data()  # Use the cached photo data
    return render_template("index.html", blog=photoData)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/publications/")
def publications():
    return render_template("publications.html")

@app.route("/book/")
def book():
    return render_template("book.html")


@app.route("/gallery/")
def gallery():
    photoData = get_photo_data()  # Use the cached photo data
    return render_template("gallery.html", blog=photoData)

@app.route("/contact/", methods=["GET"])
def contact():
    return render_template("contact.html")

@app.route("/contact", methods=["POST"])
def receive_data():
    error = None
    if request.method == 'POST':
        if request.form['name'] and request.form['phone']:
            data = request.form
            send_email(data["name"], data["email"], data["phone"], data["text"])
            return render_template("contact.html", result="1", message="Thank you for your message.")
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user="KevinsFancyTester12@gmail.com", password=arsewards_dict["KevinsFancyGmAppPassword"])
        connection.sendmail("KevinsFancyTester12@gmail.com", arsewards_dict["kevinsHiddenEmail"], email_message)
        connection.close()

@app.route("/blogPost/<int:id>")
def return_blogpost(id):
    photoData = get_photo_data()  # Use the cached photo data
    return render_template("post.html", blog=photoData[int(id)-1])

@app.route("/gallery/<int:id>")
def returnPhoto(id):
    photoData = get_photo_data()  # Use the cached photo data
    return render_template("post.html", blog=photoData[int(id)-1])

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
