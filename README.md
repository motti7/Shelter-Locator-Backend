# Real-Time Shelter Locator (Backend)

## Problem & Vision
Identifying a critical need during emergency situations, this project aims to provide users with a fast, reliable, and accessible tool to locate the nearest available shelter based on their real-time location.

## Key Features
- **Real-time Location:** Uses client-side (Base44) location data to find the closest shelter.
- **Municipal Data Integration:** Automated data scraping from Petah Tikva municipality sources.
- **API-Based:** Exposes a RESTful API endpoint for seamless integration.

## Architecture
- **Web Scraper:** Independently developed Python script to scrape municipal data.
- **Backend Service:** Implements matchmaking logic and exposes the API.
- **Containerization:** Deployed using Docker on Google Cloud Platform (GCP).
- **Frontend Integration:** Connects with a Base44-based UI (Link below).

## Links
- **Live UI (Base44):** [https://findnearestshelter.base44.app]

## Recognition
- Developed as a final project for Object-Oriented Programming (OOP) course, exceeding requirements.# Shelter-Locator-Backend
Backend for real-time nearest emergency shelter locator
