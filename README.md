# QR Generator and URL Shortener with CI/CD on Google Cloud

A lightweight, responsive URL shortening service built with Flask, deployed on Google Cloud Run, and uses Firestore for data storage. Converts long URLs both QR codes and short links that automatically redirect to the original destination.

For now, no domain has been registered for this project so the "short-urls" are not so short due to Google Cloud's default URLs

## Live Demo

Visit the deployed site here:  
**[https://qr-generator-and-url-shortener-880303141262.us-central1.run.app](https://qr-generator-and-url-shortener-880303141262.us-central1.run.app)**

## Features

- Generate a QR codes and shorten long URLs with a random 6-character code
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
├──.github/workflows
│ ├── google-cloudrun-docker.yml # CI/CD Pipelining
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

## CI/CD Pipeline (Optional)

This project uses GitHub Actions for continuous integration and continuous deployment (CI/CD). Every time a change is pushed to the `main` branch, the pipeline automatically builds the Docker image, pushes it to Google Cloud Artifact Registry, and deploys it to Google Cloud Run.

1. Set up the necessary service accounts for Github on Google CLoud
2. Generate a key and copy to contents into the repository's secrets
3. Go to Github Actions and configure a Google Cloud Run workflow

The workflow/pipeline is configured in the [`.github/workflows/google-cloudrun-docker.yml`](.github/workflows/google-cloudrun-docker.yml) file and executes these steps:

1. **Authenticate to Google Cloud**: Uses a service account key to authenticate to Google Cloud.
2. **Build Docker Image**: Builds the application into a Docker image.
3. **Tag Docker Image**: Tags the Docker image with the appropriate project and repository information.
4. **Push Docker Image**: Pushes the Docker image to Google Cloud Artifact Registry.
5. **Deploy to Cloud Run**: Deploys the latest image to Google Cloud Run with public access.

