# URL Shortener

A simple and responsive URL shortener built with Flask and hosted on Google Cloud Run. It allows users to shorten long URLs into short, shareable links, and automatically redirects them to the original destination.

For now, no domain has been registered for this project so the "short-urls" are not so short due to Google Cloud's default URLs

## Live Demo

Visit the deployed site here:  
**[https://qr-generator-and-url-shortener-880303141262.us-central1.run.app](https://qr-generator-and-url-shortener-880303141262.us-central1.run.app)**

## Features

- Shorten long URLs with a random 6-character code
- Automatic redirection from short to long URLs
- Firestore-backed persistence
- Clean frontend built with Tailwind CSS

## Project Structure
```
. 
├── app.py # Flask backend
├── Dockerfile # This is optional, see Deployment
├── requirements.txt # Python dependencies 
├── static/ 
│ ├── index.html # Frontend HTML 
│ └── script.js # Frontend JS 
└── README.md # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.7+
- A Google Cloud project 
- Google Cloud Firestore API
- Install Google Cloud SDK

### Clone the Repository

```bash
git clone https://github.com/plum-sorathorn/QR-and-URL-on-Google-Cloud.git
cd QR-and-URL-on-Google-Cloud
```

Install Dependencies

```
pip install -r requirements.txt
```

### Deployment (without Docker)

You can deploy the entire app with a single command (done on Windows 10):

```
gcloud run deploy qr-generator-and-url-shortener --source . --platform managed --region us-central1 --allow-unauthenticated
```

This command will:
- Package your app and build it using Cloud Build
- Deploy it to Cloud Run
- Make it publicly accessible

Done! Your web app should now be deployed!

### Deployment with Docker

- Get your PROJECT_ID from your Google Cloud project
- Install Docker Desktop, then run

```
docker build -t qr-generator-and-url-shortener .
docker tag qr-generator-and-url-shortener gcr.io/[PROJECT_ID]/qr-generator-and-url-shortener
docker push gcr.io/[PROJECT_ID]/qr-generator-and-url-shortener
```
*** NOTE: Make sure you've logged in on Google Cloud SDK and also authenticated Docker on it!

- Then, deploy on Google Cloud as an image (change the region accordingly) :

```
gcloud run deploy qr-generator-and-url-shortener --image gcr.io/[PROJECT_ID]/qr-generator-and-url-shortener --platform managed --region us-central1 --allow-unauthenticated
```

### Done! Now you should have this!

![demo](gifs/demo.gif)

### Future Improvements

- QR Code Generation: When a user inputs a long URL, both a short URL and a corresponding QR code will be generated for easy sharing and access.
- CI/CD Automation: Plans to automate the deployment process using CI/CD pipelines to streamline future updates and deployments.
