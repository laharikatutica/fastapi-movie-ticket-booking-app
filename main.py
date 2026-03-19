from fastapi import FastAPI, Query, Response, status, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ══════════════════════════════════ MODELS ══════════════════════════════════════
# Q6 -----BookingRequest model
class BookingRequest(BaseModel):
    customer_name: str = Field(min_length=2) # customer name must have at least 2 characters
    movie_id: int = Field(gt=0) # movie id must be greater than 0
    seats: int = Field(gt=0, le=10) # seats must be >0 and <=10    
    phone: str = Field(min_length=10) # phone number must have at least 10 digits
    seat_type: str = "standard" 

    # Q9 --- add new field: promo_code
    promo_code: str = ""

# Q11 ------NewMovie model
class NewMovie(BaseModel):
    title: str = Field(min_length=2)
    genre: str = Field(min_length=2)
    language: str = Field(min_length=2)
    duration_mins: int = Field(gt=0)
    ticket_price: int = Field(gt=0)
    seats_available: int = Field(gt=0)

# Q14 ------HoldRequest model
class HoldRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    movie_id: int = Field(gt=0)
    seats: int = Field(gt=0, le=10)

# ══════════════════════════════════ DATA ══════════════════════════════════════
# Q2 ---- add movies data
movies = [
    {
        "id": 1,
        "title": "RRR",
        "genre": "Action",
        "language": "Telugu",
        "duration_mins": 182,
        "ticket_price": 250,
        "seats_available": 120
    },
    {
        "id": 2,
        "title": "Baahubali 2",
        "genre": "Action",
        "language": "Telugu",
        "duration_mins": 171,
        "ticket_price": 300,
        "seats_available": 100
    },
    {
        "id": 3,
        "title": "Dangal",
        "genre": "Drama",
        "language": "Hindi",
        "duration_mins": 161,
        "ticket_price": 200,
        "seats_available": 80
    },
    {
        "id": 4,
        "title": "3 Idiots",
        "genre": "Comedy",
        "language": "Hindi",
        "duration_mins": 170,
        "ticket_price": 180,
        "seats_available": 90
    },
    {
        "id": 5,
        "title": "KGF Chapter 2",
        "genre": "Action",
        "language": "Kannada",
        "duration_mins": 168,
        "ticket_price": 250,
        "seats_available": 110
    },
    {
        "id": 6,
        "title": "Vikram",
        "genre": "Action",
        "language": "Tamil",
        "duration_mins": 175,
        "ticket_price": 220,
        "seats_available": 95
    },
    {
        "id": 7,
        "title": "Drishyam",
        "genre": "Drama",
        "language": "Malayalam",
        "duration_mins": 160,
        "ticket_price": 150,
        "seats_available": 70
    },
    {
        "id": 8,
        "title": "Jailer",
        "genre": "Action",
        "language": "Tamil",
        "duration_mins": 158,
        "ticket_price": 240,
        "seats_available": 85
    },
    {
        "id": 9,
        "title": "Pushpa",
        "genre": "Action",
        "language": "Telugu",
        "duration_mins": 179,
        "ticket_price": 230,
        "seats_available": 105
    },
    {
        "id": 10,
        "title": "PK",
        "genre": "Comedy",
        "language": "Hindi",
        "duration_mins": 153,
        "ticket_price": 190,
        "seats_available": 75
    },
    {
        "id": 11,
        "title": "Kantara",
        "genre": "Horror",
        "language": "Kannada",
        "duration_mins": 150,
        "ticket_price": 210,
        "seats_available": 88
    },
    {
        "id": 12,
        "title": "Premam",
        "genre": "Drama",
        "language": "Malayalam",
        "duration_mins": 156,
        "ticket_price": 160,
        "seats_available": 92
    }
]

# list to store all bookings
bookings = []

# counter to generate booking id
booking_counter = 1

# seat hold storage
holds = []
hold_counter = 1

# ══════════════════════════════════ HELPERS ══════════════════════════════════════

# Q7 ----- helper functions
# helper function to find movie by id
def find_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return None

# helper function to calculate ticket cost
def calculate_ticket_cost(base_price, seats, seat_type, promo_code):
    multiplier = 1
    if seat_type == "premium":
        multiplier = 1.5

    elif seat_type == "recliner":
        multiplier = 2

    elif seat_type == "standard":
        multiplier = 1

    # original cost
    price_per_ticket = base_price * multiplier
    original_cost = price_per_ticket * seats

    # Q9 --- apply promo
    final_cost = original_cost
    if promo_code == "SAVE10":
        final_cost = original_cost * 0.9

    elif promo_code == "SAVE20":
        final_cost = original_cost * 0.8

    return original_cost, final_cost

# Q10 --- helper function to filter movies
def filter_movies_logic(genre=None, language=None, max_price=None, min_seats=None):
    result = []
    for movie in movies:
        if genre is not None and movie["genre"].lower() != genre.lower():
            continue
        
        if language is not None and movie["language"].lower() != language.lower():
            continue

        if max_price is not None and movie["ticket_price"] > max_price:
            continue

        if min_seats is not None and movie["seats_available"] < min_seats:
            continue

        result.append(movie)
    return result

# ══════════════════════════════════ Endpoints ══════════════════════════════════
# Endpoint - Q1 --------home
@app.get('/')
def home():
    return {
        'message': 'Welcome to CineStar Booking'
        }

# Endpoint - Q2 -------GET /movies
@app.get("/movies")
def get_all_movies():
    total_movies = len(movies)
    total_seats_available = sum(
        movie["seats_available"] for movie in movies
    )
    return {
        "movies": movies,
        "total": total_movies,
        "total_seats_available": total_seats_available
    }

# Endpoint - Q5 -------GET /movies/summary
@app.get("/movies/summary")
def movies_summary():
    total_movies = len(movies)

    # highest ticket price
    most_expensive_ticket = max(
        movie["ticket_price"] for movie in movies
    )

    # lowest ticket price
    cheapest_ticket = min(
        movie["ticket_price"] for movie in movies
    )

    # total seats across all movies
    total_seats = sum(
        movie["seats_available"] for movie in movies
    )

    # count movies by genre
    movies_by_genre = {}
    for movie in movies:
        genre = movie["genre"]
        if genre in movies_by_genre:
            movies_by_genre[genre] += 1
        else:
            movies_by_genre[genre] = 1
    return {
        "total_movies": total_movies,
        "most_expensive_ticket": most_expensive_ticket,
        "cheapest_ticket": cheapest_ticket,
        "total_seats": total_seats,
        "movies_by_genre": movies_by_genre
    }

# Endpoint - Q10 -------GET /movies/filter
@app.get("/movies/filter")
def filter_movies(
    genre: str = None,
    language: str = None,
    max_price: int = None,
    min_seats: int = None
):
    filtered = filter_movies_logic(
        genre,
        language,
        max_price,
        min_seats
    )
    return {
        "count": len(filtered),
        "movies": filtered
    }

# Endpoint - Q16 -------GET /movies/search
@app.get("/movies/search")
def search_movies(keyword: str = Query(...)):
    result = []
    key = keyword.lower()
    for movie in movies:
        if (
            key in movie["title"].lower()
            or key in movie["genre"].lower()
            or key in movie["language"].lower()
        ):
            result.append(movie)
    if len(result) == 0:
        return {
            "message": "No movies found",
            "total_found": 0,
            "movies": []
        }
    return {
        "total_found": len(result),
        "movies": result
    }

# Endpoint - Q17 -------GET /movies/sort
@app.get("/movies/sort")
def sort_movies(
    sort_by: str = Query("ticket_price"),
    order: str = Query("asc")
):
    allowed_sort = [
        "ticket_price",
        "title",
        "duration_mins",
        "seats_available"
    ]
    allowed_order = ["asc", "desc"]
    if sort_by not in allowed_sort:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_by value"
        )
    # validate order
    if order not in allowed_order:
        raise HTTPException(
            status_code=400,
            detail="Invalid order value"
        )
    reverse_sort = False
    if order == "desc":
        reverse_sort = True
    sorted_list = sorted(
        movies,
        key=lambda x: x[sort_by],
        reverse=reverse_sort
    )
    return {
        "sorted_by": sort_by,
        "order": order,
        "movies": sorted_list
    }

# Endpoint - Q18 -------GET /movies/page
@app.get("/movies/page")
def get_movies_page(
    page: int = Query(1, gt=0),
    limit: int = Query(3, gt=0)
):
    total = len(movies)
    total_pages = (total + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    data = movies[start:end]
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "movies": data
    }

# Endpoint - Q20 -------GET /movies/browse
@app.get("/movies/browse")
def browse_movies(
    keyword: Optional[str] = None,
    genre: Optional[str] = None,
    language: Optional[str] = None,
    sort_by: str = Query("ticket_price"),
    order: str = Query("asc"),
    page: int = Query(1, gt=0),
    limit: int = Query(3, gt=0)
):
    result = movies.copy()

    # keyword filter
    if keyword is not None:
        key = keyword.lower()
        result = [
            m for m in result
            if key in m["title"].lower()
            or key in m["genre"].lower()
            or key in m["language"].lower()
        ]

    if genre is not None or language is not None:
        result = [
            m for m in result
            if m in filter_movies_logic(
                genre=genre,
                language=language
            )
        ]
    # sort
    allowed_sort = [
        "ticket_price",
        "title",
        "duration_mins",
        "seats_available"
    ]

    if sort_by not in allowed_sort:
        raise HTTPException(400, "Invalid sort_by")

    if order not in ["asc", "desc"]:
        raise HTTPException(400, "Invalid order")

    reverse_sort = order == "desc"
    result = sorted(
        result,
        key=lambda x: x[sort_by],
        reverse=reverse_sort
    )

    # pagination
    total = len(result)
    total_pages = (total + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    page_data = result[start:end]

    return {
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "limit": limit,
        "movies": page_data
    }

# Endpoint - Q4 -------GET /bookings
@app.get("/bookings")
def get_all_bookings():
    total_bookings = len(bookings)

    # total revenue from all bookings
    total_revenue = sum(
        booking.get("final_cost", 0)
        for booking in bookings
    )
    return {
        "bookings": bookings,
        "total": total_bookings,
        "total_revenue": total_revenue
    }

# Endpoint - Q8 -------POST /bookings
@app.post("/bookings", status_code=201)
def create_booking(data: BookingRequest):
    global booking_counter

    # check movie exists using helper
    movie = find_movie(data.movie_id)
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    # check seats availability
    if movie["seats_available"] < data.seats:
        raise HTTPException(
            status_code=400,
            detail="Not enough seats available"
        )

    # Q9 --- updated after adding promo_code
    original_cost, final_cost = calculate_ticket_cost(
    movie["ticket_price"],
    data.seats,
    data.seat_type,
    data.promo_code
    )

    # reduce seats after booking
    movie["seats_available"] -= data.seats

    # create booking
    booking = {
    "booking_id": booking_counter,
    "movie_id": data.movie_id,
    "movie_title": movie["title"],
    "customer_name": data.customer_name,
    "seats": data.seats,
    "seat_type": data.seat_type,
    "promo_code": data.promo_code,
    "original_cost": original_cost,
    "final_cost": final_cost
}
    bookings.append(booking)
    booking_counter += 1
    return booking

# Endpoint - Q19 -------GET /bookings/search
@app.get("/bookings/search")
def search_bookings(customer_name: str = Query(...)):
    result = []
    key = customer_name.lower()
    for b in bookings:
        name = str(b.get("customer_name", "")).lower()
        if key in name:
            result.append(b)
    return {
        "total": len(result),
        "bookings": result
    }

# Endpoint - Q19 -------GET /bookings/sort
@app.get("/bookings/sort")
def sort_bookings(
    sort_by: str = Query("final_cost"),
    order: str = Query("asc")
):
    allowed_sort = ["final_cost", "seats"]
    allowed_order = ["asc", "desc"]
    if sort_by not in allowed_sort:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort_by"
        )
    if order not in allowed_order:
        raise HTTPException(
            status_code=400,
            detail="Invalid order"
        )
    reverse_sort = False
    if order == "desc":
        reverse_sort = True

    sorted_list = sorted(
        bookings,
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse_sort
    )
    return {
        "sorted_by": sort_by,
        "order": order,
        "bookings": sorted_list
    }

# Endpoint - Q19 -------GET /bookings/page
@app.get("/bookings/page")
def bookings_page(
    page: int = Query(1, gt=0),
    limit: int = Query(3, gt=0)
):
    total = len(bookings)
    total_pages = (total + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    data = bookings[start:end]
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "bookings": data
    }

# Endpoint - Q11 -------POST /movies
@app.post("/movies", status_code=201)
def add_movie(data: NewMovie):
    # check duplicate title
    for movie in movies:
        if movie["title"].lower() == data.title.lower():
            raise HTTPException(
                status_code=400,
                detail="Movie already exists"
            )
    # create new id
    new_id = len(movies) + 1
    new_movie = {
        "id": new_id,
        "title": data.title,
        "genre": data.genre,
        "language": data.language,
        "duration_mins": data.duration_mins,
        "ticket_price": data.ticket_price,
        "seats_available": data.seats_available
    }
    movies.append(new_movie)
    return new_movie

# Endpoint - Q14 -------POST /seat-hold
@app.post("/seat-hold", status_code=201)
def create_hold(data: HoldRequest):
    global hold_counter
    movie = find_movie(data.movie_id)
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    if movie["seats_available"] < data.seats:
        raise HTTPException(
            status_code=400,
            detail="Not enough seats"
        )

    # reduce seats temporarily
    movie["seats_available"] -= data.seats
    hold = {
        "hold_id": hold_counter,
        "customer_name": data.customer_name,
        "movie_id": data.movie_id,
        "movie_title": movie["title"],
        "seats": data.seats
    }
    holds.append(hold)
    hold_counter += 1
    return hold

# Endpoint - Q14 -------GET /seat-hold
@app.get("/seat-hold")
def get_holds():
    return {
        "total_holds": len(holds),
        "holds": holds
    }

# Endpoint - Q3 -------GET /movies/{movie_id}
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return {"error": "Movie not found"}

# Endpoint - Q12 -------PUT /movies/{movie_id}
@app.put("/movies/{movie_id}")
def update_movie(
    movie_id: int,
    ticket_price: int = Query(None, gt=0),
    seats_available: int = Query(None, gt=0)
):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )
    if ticket_price is not None:
        movie["ticket_price"] = ticket_price

    if seats_available is not None:
        movie["seats_available"] = seats_available
    return {
        "message": "Movie updated",
        "movie": movie
    }

# Endpoint - Q13 -------DELETE /movies/{movie_id}
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Not found")

    for b in bookings:
        if b["movie_id"] == movie_id:
            raise HTTPException(status_code=400, detail="Movie has bookings")

    movies.remove(movie)
    return {"message": "Deleted successfully"}

# Endpoint - Q15 -------POST /seat-confirm/{hold_id}
@app.post("/seat-confirm/{hold_id}")
def confirm_hold(hold_id: int):
    global booking_counter
    hold = None

    # find hold
    for h in holds:
        if h.get("hold_id") == hold_id:
            hold = h
            break

    if hold is None:
        raise HTTPException(
            status_code=404,
            detail="Hold not found"
        )

    movie = find_movie(hold["movie_id"])
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    # Q9 version -> returns original, final_cost
    original, final_cost = calculate_ticket_cost(
        movie["ticket_price"],
        hold["seats"],
        "standard",
        ""   # no promo
    )
    booking = {
        "booking_id": booking_counter,
        "movie_id": hold["movie_id"],
        "movie_title": movie["title"],
        "customer": hold["customer_name"],
        "seats": hold["seats"],
        "seat_type": "standard",
        "total_cost": final_cost
    }
    bookings.append(booking)
    booking_counter += 1
    holds.remove(hold)
    return {
        "message": "Booking confirmed",
        "booking": booking,
        "original_cost": original,
        "final_cost": final_cost
    }

# Endpoint - Q15 -------DELETE /seat-release/{hold_id}
@app.delete("/seat-release/{hold_id}")
def release_hold(hold_id: int):
    hold = None
    for h in holds:
        if h["hold_id"] == hold_id:
            hold = h
            break
    if not hold:
        raise HTTPException(
            status_code=404,
            detail="Hold not found"
        )
    movie = find_movie(hold["movie_id"])
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )
    movie["seats_available"] += hold["seats"]
    holds.remove(hold)
    return {
        "message": "Hold released"
    }
