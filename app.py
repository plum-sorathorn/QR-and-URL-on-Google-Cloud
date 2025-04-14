import os
import random
import string
from io import BytesIO
from flask import Flask, request, redirect, jsonify, send_from_directory
from google.cloud import firestore, storage
import qrcode


app = Flask(__name__, static_folder='webpage')
firestore_database = firestore.Client()


# Firestore collection where we store the short URL mappings
URL_COLLECTION = 'url_mappings'
GCS_BUCKET_NAME = "qr-url-storage"

@app.route('/')
# function to let us know if the API is running
def home():
    return send_from_directory('webpage', 'index.html')

# function to shorten a URL
def create_short_url(long_url, host_url):
    # Check if the long_url already exists in the database
    existing_doc = firestore_database.collection(URL_COLLECTION).where('long_url', '==', long_url).limit(1).get()

    if existing_doc:
        short_code = existing_doc[0].id
    else:
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        firestore_database.collection(URL_COLLECTION).document(short_code).set({
            'long_url': long_url,
            'time_created': firestore.SERVER_TIMESTAMP
        })

    short_url = host_url + short_code
    return short_url, short_code

# function to generate a QR code from a URL
def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_data = buffer.read()
    return img_data

# function to upload the generated QR to Google Cloud Storage
def upload_qr(short_code, img_data, bucket_name="GCS_BUCKET_NAME"):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    data = bucket.blob(f"qr_codes/{short_code}.png")
    
    # Upload the image data
    data.upload_from_string(img_data, content_type='image/png')
    
    return data.public_url

# POST endpoint: shorten + generate QR
@app.route('/generate', methods=['POST'])
def generate_url_and_qr():
    long_url = request.json.get('url')
    if not long_url:
        return jsonify({'error': 'No URL provided'}), 400

    short_url, short_code = create_short_url(long_url, request.host_url)

    # Generate QR code as image binary
    img_data = generate_qr_code(long_url)

    # Upload to GCS
    qr_url = upload_qr(short_code, img_data, bucket_name=GCS_BUCKET_NAME)

    # Save the QR URL to Firestore
    firestore_database.collection(URL_COLLECTION).document(short_code).update({
        'qr_url': qr_url
    })

    return jsonify({
        'short_url': short_url,
        'qr_url': qr_url
    })

# retrieves the shortened URL in firestore, if found, redirect to the matched long (original) link, else, return 404
@app.route('/<short_code>')
def redirect_to_url(short_code):
    retrieved_data = firestore_database.collection(URL_COLLECTION).document(short_code).get()
    if not retrieved_data.exists:
        return jsonify({'error': 'URL not found'}), 404
    
    long_url = retrieved_data.to_dict()['long_url']
    return redirect(long_url)

# retrieves the qr code from Google Cloud Storage
@app.route('/qr/<short_code>')
def get_qr_code(short_code):
    # first, retrieve the QR's url from firestore
    doc = firestore_database.collection(URL_COLLECTION).document(short_code).get()
    if not doc.exists:
        return jsonify({'error': 'QR code not found'}), 404

    qr_url = doc.to_dict().get('qr_url')
    if not qr_url:
        return jsonify({'error': 'QR code not generated yet'}), 404

    return redirect(qr_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 443)))
