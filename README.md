# Library Manager Web Application

A **Python Flask** web application that simulates a campus library management system. This project allows librarians to **manage inventory, checkout/return books, search for books, and generate reports** — all via a web browser.  

---

## Features

- **Inventory Management**
  - Add or update books
  - Track available copies and borrowed counts
- **Transaction Processing**
  - Checkout books with borrower name and due date
  - Return books with overdue fine calculation
- **Search Functionality**
  - Search books by title, author, or genre
- **Reports**
  - Popular books report
  - Overdue books report
- **Web Interface**
  - Built with **Flask** and **Bootstrap** for a clean, user-friendly interface
- **Sample Data**
  - Preloaded books and transactions for testing

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Justina2-tech/Library_project.git
2. Install Dependency
   pip install flask
3. Run the web application
  py web_library_manager_full.py
4. open  Browser and Go to
   http://127.0.0.1:5000/

**Usage**

Add / Update Books: Fill in Book ID, Title, Author, Genre, and number of copies.

Checkout Books: Enter Book ID, Borrower Name, and Due Days.

Return Books: Enter Book ID and Borrower Name. Fines are calculated automatically for overdue books.

Search Books: Enter a keyword to find books by title, author, or genre.

**Technologies**

Python 3.12

Flask (Web framework)

Bootstrap 5 (Frontend styling)

HTML / CSS / Jinja2 Templates

Reports: Click buttons to view popular or overdue books.

cd Library_project
