# התחברות ל-Google Cloud
gcloud auth login

# התחברות ל-Google Cloud
gcloud auth login

# בניית הדוקר והעלאה ל-GCR
gcloud builds submit --tag gcr.io/miklat-now/miklat-server

# פריסת Cloud Run
gcloud run deploy miklat-server `
    --image gcr.io/miklat-now/miklat-server `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated
