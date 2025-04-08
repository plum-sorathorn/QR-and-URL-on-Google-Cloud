import os
import random
import string
from flask import Flask, request, redirect, jsonify, send_from_directory
from google.cloud import firestore

app = Flask(__name__, static_folder='webpage')
db = firestore.Client()


# Firestore collection where we store the short URL mappings
URL_COLLECTION = 'url_mappings'

@app.route('/')
# function to let us know if the API is running
def home():
    return send_from_directory('webpage', 'index.html')

# takes a JSON body and generates an ID, saves the ID in firestone, and then return it as a short URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json.get('url')
    if not long_url:
        return jsonify({'error': 'No URL provided'}), 400

    # Check if the long_url already exists in the database
    existing_doc = db.collection(URL_COLLECTION).where('long_url', '==', long_url).limit(1).get()
    
    if existing_doc:
        # If the URL already exists, return the existing short code
        short_code = existing_doc[0].id
    else:
        # If the URL is not in the database, generate a new short code
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        db.collection(URL_COLLECTION).document(short_code).set({
            'long_url': long_url,
            'time_created': firestore.SERVER_TIMESTAMP
        })
    
    return jsonify({'short_url': request.host_url + short_code})

# finds the shortened URL in firestone, if found, redirect to the matched long (original) link, else, return 404
@app.route('/<short_code>')
def redirect_to_url(short_code):
    doc = db.collection(URL_COLLECTION).document(short_code).get()
    if not doc.exists:
        return jsonify({'error': 'URL not found'}), 404
    
    long_url = doc.to_dict()['long_url']
    return redirect(long_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
