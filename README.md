# 📚 Library Management System

A Django-based Library Management System that allows users to view, borrow, and get AI-powered book recommendations based on their reading history.

## 🚀 Features

- 🔐 **User Session Management** – Track logged-in users and their borrowing activity.
- 📖 **View Books** – Beautifully styled UI showing available books using Bootstrap.
- ✅ **Borrow Books** – Borrow functionality with status handling and active borrow tracking.
- 💡 **Book Recommendation System** – Recommends books using content-based filtering (TF-IDF + Cosine Similarity).
- 🧠 **Machine Learning Integrated** – Uses Scikit-learn and Pandas to compute personalized recommendations.
- 🕵️ **Borrow History** – View a styled table of current and returned books.

## 🛠️ Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, Bootstrap 5
- **Database**: PostgreSQL (or default SQLite for development)
- **ML Libraries**: `scikit-learn`, `pandas`

## 💡 Recommendation Logic

- Combines the title, genre, and author fields into a single string.
- Vectorizes them using TF-IDF.
- Computes cosine similarity across all books.
- Recommends top `N` books not yet borrowed by the user, sorted by similarity.

## 📂 Project Structure

```
├── books/
│   ├── models.py
│   ├── views.py
│   ├── recommendation.py  ← ML logic for recommendations
│   ├── templates/
│   │   ├── view_books.html
│   │   ├── recommended_books.html
│   │   ├── borrow_history.html
│   └── urls.py
├── library/  ← Django settings and root config
├── static/   ← CSS, icons, etc.
└── manage.py
```

## 🖥️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/library-management.git
   cd library-management
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the server**
   ```bash
   python manage.py runserver
   ```

6. **Visit in browser**
   ```
   http://127.0.0.1:8000/
   ```

## 📌 To-Do / Future Scope

- 🔍 Full-text search for books
- 📘 Book detail pages with Open Library integration
- 📊 Admin dashboard and analytics
- 📦 Dockerize the project for deployment

## 🙌 Acknowledgements

- Bootstrap for frontend styling
- Scikit-learn for recommendation logic
- Django ORM and session management
