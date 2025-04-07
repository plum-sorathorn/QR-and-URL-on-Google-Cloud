# URL Shortener

A simple and responsive URL shortener built with Flask and hosted on Google Cloud Run. It allows users to shorten long URLs into short, shareable links, and automatically redirects them to the original destination.

For now, no domain has been registered for this project so the "short-urls" are not so short due to Google Cloud's URLs

## Live Demo

Visit the deployed site here:  
**[https://url-shortener-880303141262.us-central1.run.app](https://url-shortener-880303141262.us-central1.run.app)**

## Features

- Shorten long URLs with a random 6-character code
- Automatic redirection from short to long URLs
- Firestore-backed persistence
- Clean frontend built with Tailwind CSS

## Project Structure

|- app.py # Flask-based backend
|- static/
|  |- script.js # Frontend JavaScript
|  |- index.html # Web page
|- requirements.txt # Python dependencies
|- README.md

## Deployment Instructions

### Prerequisites

- Python 3.7+
- A Google Cloud project with billing enabled
- Firestore enabled in **Native mode**
- `gcloud` CLI installed and authenticated
- You are in the correct project (check with `gcloud config get-value project`)

### Deploy with Google Cloud Run

You can deploy the entire app (including building the Docker image) with a single command (done on Windows 10):

gcloud run deploy url-shortener --source . --platform managed --region us-central1 --allow-unauthenticated

This command will:
- Package your app and build it using Cloud Build
- Deploy it to Cloud Run
- Make it publicly accessible
After deployment, the terminal will display a live service URL — use this to access your app.
