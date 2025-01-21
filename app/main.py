from flask import Flask, render_template, request,jsonify
import requests
import smtplib
from arsewards import arsewards_dict
from flask_caching import Cache

from flask import jsonify
from datetime import datetime
import json
from functools import lru_cache
import os

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


# Cache the ORCID API response for 24 hours
@lru_cache(maxsize=1)
def get_orcid_data():
    orcid_id = '0000-0001-6914-7447'
    url = f'https://pub.orcid.org/v3.0/{orcid_id}/person'
    
    try:
        response = requests.get(url, headers={'Accept': 'application/json'})
        response.raise_for_status()
        data = response.json()
        # Store timestamp with the data
        return {
            'biography': data.get('biography', {}).get('content', ''),
            'timestamp': datetime.now().timestamp()
        }
    except Exception as e:
        print(f"Error fetching ORCID data: {e}")
        return None

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/api/orcid-bio')
def orcid_bio():
    data = get_orcid_data()
    if data:
        return jsonify(data)
    return jsonify({'error': 'Unable to fetch biography'}), 500




@lru_cache(maxsize=1)
def get_orcid_publications():
    orcid_id = '0000-0001-6914-7447'
    url = f'https://pub.orcid.org/v3.0/{orcid_id}/works'
    
    try:
        response = requests.get(url, headers={'Accept': 'application/json'})
        response.raise_for_status()
        data = response.json()
        
        # Extract and format publication data
        publications = []
        for work in data.get('group', []):
            work_summary = work['work-summary'][0]
            
            pub = {
                'title': work_summary.get('title', {}).get('title', {}).get('value', ''),
                'year': work_summary.get('publication-date', {}).get('year', {}).get('value', ''),
                'journal': work_summary.get('journal-title', {}).get('value', ''),
                'doi': work_summary.get('external-ids', {}).get('external-id', [{}])[0].get('external-id-value', ''),
                'type': work_summary.get('type', '')
            }
            publications.append(pub)
            
        # Sort by year, newest first
        publications.sort(key=lambda x: x['year'] or '0', reverse=True)
        return publications
        
    except Exception as e:
        print(f"Error fetching ORCID publications: {e}")
        return None

@app.route('/publications/')
def publications():
    return render_template('publications.html')

@app.route('/api/publications')
def get_publications():
    pubs = get_orcid_publications()
    if pubs:
        return jsonify(pubs)
    return jsonify({'error': 'Unable to fetch publications'}), 500


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
