from flask import Flask, render_template_string, request
import datetime

app = Flask(__name__)

# -------------------------------
# Global Data Structures with Sample Data
# -------------------------------
library = {
    "B001": {"title": "Python Basics", "author": "John Doe", "genre": "Programming", "copies": 5, "borrowed": 2},
    "B002": {"title": "Data Science 101", "author": "Jane Smith", "genre": "Data Science", "copies": 3, "borrowed": 3},
    "B003": {"title": "Algorithms Unlocked", "author": "Thomas Cormen", "genre": "Computer Science", "copies": 4, "borrowed": 1},
    "B004": {"title": "Artificial Intelligence", "author": "Stuart Russell", "genre": "AI", "copies": 2, "borrowed": 0},
    "B005": {"title": "Database Systems", "author": "Abraham Silberschatz", "genre": "Database", "copies": 3, "borrowed": 2},
}

transactions = [
    {"book_id": "B001", "borrower": "Alice", "due_date": datetime.date.today() - datetime.timedelta(days=2), "returned": False},
    {"book_id": "B002", "borrower": "Bob", "due_date": datetime.date.today() + datetime.timedelta(days=5), "returned": False},
    {"book_id": "B005", "borrower": "Charlie", "due_date": datetime.date.today() - datetime.timedelta(days=1), "returned": False},
]

FINE_PER_DAY = 2.0

# -------------------------------
# HTML Template with Bootstrap
# -------------------------------
TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Library Manager</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="p-4">
<div class="container">
  <h1 class="mb-4">Library Manager</h1>

  {% if message %}
  <div class="alert alert-info">{{ message }}</div>
  {% endif %}

  <h2>Inventory</h2>
  <table class="table table-striped">
    <thead>
      <tr>
        <th>ID</th><th>Title</th><th>Author</th><th>Genre</th><th>Available</th><th>Borrowed</th>
      </tr>
    </thead>
    <tbody>
      {% for book_id, book in library.items() %}
      <tr>
        <td>{{ book_id }}</td>
        <td>{{ book.title }}</td>
        <td>{{ book.author }}</td>
        <td>{{ book.genre }}</td>
        <td>{{ book.copies }}</td>
        <td>{{ book.borrowed }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  <div class="row mt-4">
    <div class="col-md-6">
      <h3>Add / Update Book</h3>
      <form method="post" action="/add_update">
        <input class="form-control mb-2" type="text" name="book_id" placeholder="Book ID" required>
        <input class="form-control mb-2" type="text" name="title" placeholder="Title" required>
        <input class="form-control mb-2" type="text" name="author" placeholder="Author" required>
        <input class="form-control mb-2" type="text" name="genre" placeholder="Genre" required>
        <input class="form-control mb-2" type="number" name="copies" placeholder="Number of Copies" min="1" required>
        <button class="btn btn-primary" type="submit">Add / Update</button>
      </form>
    </div>

    <div class="col-md-6">
      <h3>Checkout Book</h3>
      <form method="post" action="/checkout">
        <input class="form-control mb-2" type="text" name="book_id" placeholder="Book ID" required>
        <input class="form-control mb-2" type="text" name="borrower" placeholder="Borrower Name" required>
        <input class="form-control mb-2" type="number" name="due_days" placeholder="Due Days" min="1" required>
        <button class="btn btn-success" type="submit">Checkout</button>
      </form>

      <h3 class="mt-4">Return Book</h3>
      <form method="post" action="/return">
        <input class="form-control mb-2" type="text" name="book_id" placeholder="Book ID" required>
        <input class="form-control mb-2" type="text" name="borrower" placeholder="Borrower Name" required>
        <button class="btn btn-warning" type="submit">Return</button>
      </form>

      <h3 class="mt-4">Search Books</h3>
      <form method="post" action="/search">
        <input class="form-control mb-2" type="text" name="keyword" placeholder="Title, Author, Genre" required>
        <button class="btn btn-info" type="submit">Search</button>
      </form>
    </div>
  </div>

  <div class="mt-4">
    <h3>Reports</h3>
    <form method="get" action="/popular">
      <button class="btn btn-secondary mb-2" type="submit">Popular Books</button>
    </form>
    <form method="get" action="/overdue">
      <button class="btn btn-danger mb-2" type="submit">Overdue Books</button>
    </form>
  </div>
</div>
</body>
</html>
"""

# -------------------------------
# Routes
# -------------------------------

@app.route("/", methods=["GET"])
def home():
    return render_template_string(TEMPLATE, library=library, message="")

@app.route("/add_update", methods=["POST"])
def add_update():
    book_id = request.form["book_id"]
    title = request.form["title"]
    author = request.form["author"]
    genre = request.form["genre"]
    copies = int(request.form["copies"])

    if book_id in library:
        library[book_id]["copies"] += copies
        message = f"Book {title} updated successfully."
    else:
        library[book_id] = {"title": title, "author": author, "genre": genre, "copies": copies, "borrowed": 0}
        message = f"Book {title} added successfully."
    return render_template_string(TEMPLATE, library=library, message=message)

@app.route("/checkout", methods=["POST"])
def checkout():
    book_id = request.form["book_id"]
    borrower = request.form["borrower"]
    due_days = int(request.form["due_days"])
    if book_id not in library:
        message = "Book not found."
    elif library[book_id]["copies"] <= 0:
        message = "No copies available."
    else:
        due_date = datetime.date.today() + datetime.timedelta(days=due_days)
        library[book_id]["copies"] -= 1
        library[book_id]["borrowed"] += 1
        transactions.append({"book_id": book_id, "borrower": borrower, "due_date": due_date, "returned": False})
        message = f"Book checked out successfully. Due date: {due_date}"
    return render_template_string(TEMPLATE, library=library, message=message)

@app.route("/return", methods=["POST"])
def return_book():
    book_id = request.form["book_id"]
    borrower = request.form["borrower"]
    message = "Transaction not found."
    for transaction in transactions:
        if transaction["book_id"] == book_id and transaction["borrower"] == borrower and not transaction["returned"]:
            transaction["returned"] = True
            library[book_id]["copies"] += 1
            today = datetime.date.today()
            overdue_days = (today - transaction["due_date"]).days
            if overdue_days > 0:
                fine = overdue_days * FINE_PER_DAY
                message = f"Book returned late. Fine: {fine}"
            else:
                message = "Book returned on time. No fine."
            break
    return render_template_string(TEMPLATE, library=library, message=message)

@app.route("/search", methods=["POST"])
def search():
    keyword = request.form["keyword"].lower()
    results = []
    for book_id, book in library.items():
        if (keyword in book["title"].lower() or
            keyword in book["author"].lower() or
            keyword in book["genre"].lower()):
            results.append(f"{book_id}: {book['title']} by {book['author']} - {book['genre']} (Available: {book['copies']})")
    message = "<br>".join(results) if results else "No matching books found."
    return render_template_string(TEMPLATE, library=library, message=message)

@app.route("/popular", methods=["GET"])
def popular():
    results = []
    for book in library.values():
        if book["borrowed"] >= 3:
            results.append(f"{book['title']} borrowed {book['borrowed']} times")
    message = "<br>".join(results) if results else "No popular books yet."
    return render_template_string(TEMPLATE, library=library, message=message)

@app.route("/overdue", methods=["GET"])
def overdue():
    today = datetime.date.today()
    results = []
    for t in transactions:
        if not t["returned"] and t["due_date"] < today:
            book = library[t["book_id"]]
            results.append(f"{book['title']} borrowed by {t['borrower']} (Due: {t['due_date']})")
    message = "<br>".join(results) if results else "No overdue books."
    return render_template_string(TEMPLATE, library=library, message=message)

# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
