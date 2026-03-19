Project chosen — I am building project #5 - Movie Ticket Booking

# fastapi-movie-ticket-booking-app
FastAPI-powered application for movie listings and ticket booking, enabling movie browsing, fetching movie details and booking management.

## What I built
The application provides the following functionality:
- **Browse movies:** Users can browse available movies by movie title, genre or language.
- **View movie details:** Each movie displays information like duration, genre, language, and ticket price.
- **Book tickets:** Users can book tickets for a movie based on seat availability.
- **Manage bookings:** Users can view, update, or cancel their existing bookings.
  
## Key FastAPI features implemented
- **Routing:** Defined both fixed and variable routes for movies and bookings
- **Data validation:** Used Pydantic models for request validation
- **Request handling:** GET and POST endpoints for retrieving and creating bookings
- **Dependency injection:** Handled shared logic and reusable components
- **Server & testing:** Uvicorn server for running the application and live testing
- **Error handling:** Returned Proper HTTP status codes and responses for invalid requests.

## Tech Stack
- **Backend:** FastAPI
- **Data Validation:** Pydantic
- **Server:** Uvicorn

## To install dependencies:
pip install fastapi uvicorn

## To run the server:
uvicorn main:app --reload

## To open in browser:
http://127.0.0.1:8000/
