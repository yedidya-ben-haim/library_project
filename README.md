# library_project

---

## Project Description

The project is a library database management system, including book lending and subscription management. It is possible to add and delete books from the database, add and remove members, and run search queries.


---

## Technologies Used

- Python
- FastAPI
- MySQL
- Docker
- pydentic

---

## Folder Structure

```
library-api/
├── main.py
├── database/
│   ├── db_connection.py
│   ├── book_db.py
│   └── member_db.py
├── routes/
│   ├── book_routes.py
│   ├── member_routes.py
│   └── report_routes.py
├── logs/
│   └── app.log
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Docker Setup


```bash
docker run --name mysql -e MYSQL_ROOT_PASSWORD=yourpassword -e MYSQL_DATABASE=library_db -p 3306:3306 -d mysql:latest
```

---

## Database Information

**Database Name:** library_db


---

## Database Tables

### Table: `books`

| Column Name           | Data Type    | Constraints     | Description                            |
|-----------------------|--------------|-----------------|----------------------------------------|
| id                    | PRIMARY KEY  | AUTO_INCREMENT  | Primary key                            |
| title                 | VARCHAR(50)  | NOT NULL        | Book title                             |
| author                | VARCHAR(50)  | NOT NULL        | Author's name                          |
| genre                 | VARCHAR(50)  | ENUM            | Book genre                             |
| is_available          | BOOLEAN      | NOT NULL        | Book availability for borrow           |
| borrowed_by_member_id | INT          |                 | ID of the friend who borrowed the book |



---

### Table: `members`

| Column Name    | Data Type   | Constraints       | Description              |
|----------------|-------------|-------------------|--------------------------|
| id             | PRIMARY KEY | AUTO_INCREMENT    | Primary key              |
| name           | VARCHAR(50) | NOT NULL          | Member's name            |
| email          | VARCHAR(50) | UNIQUE, ,NOT NULL | Email address            |
| is_active      | BOOLEAN     | NOT NULL          | Is the member active     |
| total_borrows  | INT         | NOT NULL          | Total number of borrows  |


---

## System Rules

1. When creating a book: the system checks that the values entered in the columns meet the requirements, creates the book, and updates the database in the appropriate table.
2. The unique genre values allowed for a book must be one of these: Fiction | Non-Fiction | Science | History | Other
3. when creating a member: The system checks that the values match the field requirements, and creates a new row in the appropriate table.
4. Email uniqueness: All member email addresses must be unique, duplicate email addresses are not allowed.
5. members and borrowing: To borrow a book, the member must be active, and each time they borrow a book - the total_borrows field will increase by one.
6. already-borrowed books: Member be able to borrow a book, the book's status in the is_available field must be TRUE.
7. maximum books per member: A member cannot hold more than 3 books at a time.
8. Returning a book: A book can only be returned if it is lent to the same friend who is returning it.



---

## API Endpoints

### Books Endpoints

| Method | Endpoint                 | Description         | Request Body   | Response            |
|--------|--------------------------|---------------------|----------------|---------------------|
| POST   | /books                   | Creating a new book | JSON structure | 201, 400, 422, JSON |
| GET    | /books                   | All books           | None           | 200, 404, JSON      |
| GET    | /books/{id}              | Book by ID          | None           | 200, 404, JSON      |
| PUT    | /books/{id}              | Book update         | JSON structure | 200, 400, 422       |
| PUT    | /members/{id}/deactivate | Disabling a friend  | None           | 200, 400, 422       |
| PUT    | /members/{id}/activate   | Member activation   | None           | 200, 400            |



---

### Members Endpoints

| Method | Endpoint                 | Description                 | Request Body   | Response                         |
|--------|--------------------------|-----------------------------|----------------|----------------------------------|
| POST   | /members                 | Create a new friend         | JSON structure | Returns the created book with ID |
| GET    | /members                 | Brings all members          | None           | Returns all members              |
| GET    | /members/{id}            | Looking for a members by ID | None           | Returns the member details       |
| PUT    | /members/{id}            | Member update               | None           | 200, 400, 404, 422               |
| PUT    | /members/{id}/deactivate | Disactivate member          | None           | 200, 404                         |
| PUT    | /members/{id}/activate   | activate member             | None           | 200, 404                         |



---

### Reports Endpoints

| Method | Endpoint                | Description             | Request Body | Response                        |
|--------|-------------------------|-------------------------|--------------|---------------------------------|
| GET    | /reports/summary        | General report          | None         | Returns general report          |
| GET    | /reports/books-by-genre | List of books by genre  | None         | Returns books by genre          |
| GET    | /reports/top-member     | The most active member  |              | Returns the most active member  |


---

## System Flow


1. **Server Startup:**
   - The server connects to MySQL
   - Creates tables if they don't exist
   - Starts the FastAPI server

2. **Creating a Member:**
   - User sends POST request to `/members` with name and email
   - System validates the email is unique
   - System creates member with `is_active=True` and `total_borrows=0`
   - Returns the created member

3. **Borrowing a Book:**
   - User sends PUT request to `/books/{id}/borrow/{member_id}`
   - System checks if book exists
   - System checks if member exists and is active
   - System checks if book is available
   - System checks if member has less than 3 books
   - Updates book: `is_available=False`, `borrowed_by_member_id=member_id`
   - Increments member's `total_borrows` by 1
   - Returns success message

4. **Creating a Book:**
   - User sends POST request to `/books` with title,author and genre
   - System creates Book with `is_available=True` and `borrowed_by=NULL`
   - Returns the created Book


---

## Installation


1. Clone the repository:
```bash
https://github.com/yedidya-ben-haim/library_project.git
```

2. Navigate to the project directory

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
Run the container
docker run --name mysql \
-e MYSQL_ROOT_PASSWORD=secret \
-e MYSQL_DATABASE=library_db \
-p 3306:3306 \
-d mysql:latest
```

---

## Running the Project


1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Open your browser and go to:
```
http://localhost:8000/docs
```

---

## Testing the API


### Test 1: Create a Member
```
POST /members
{
  "name": "Sara Cohen",
  "email": "sara@example.com"
}
```

### Test 2: Create a Book
```
POST /books
{
  "title": "The Hitchhiker's Guide to the Galaxy",
  "author": "Douglas Adams",
  "genre": "Fiction"
}
```

### Test 3: Borrow a Book
```
PUT /books/1/borrow/1
```

### Test 4: Get all Books
```
GET /books/
{
  "title": "The Hitchhiker's Guide to the Galaxy",
  "author": "Douglas Adams",
  "genre": "Fiction"
}
{
  "title": "Harry Potter and the Philosopher's Stone",
  "author": "J.K. Rowling",
  "genre": "Fantasy"
}
```

---

