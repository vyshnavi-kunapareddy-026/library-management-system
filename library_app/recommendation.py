# recommendation.py
from django.db import connection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from .models import Book, BorrowedBooks

def get_recommendations_for_user(user_id, top_n=5):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title, author, genre, year, description FROM books")
        rows = cursor.fetchall()

    books = [
        {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "genre": row[3],
            "year": row[4],
            "description": row[5],
        }
        for row in rows
    ]

    df = pd.DataFrame(books)

    # Combine features for similarity
    df["combined"] = df["title"].fillna('') + " " + \
                     df["genre"].fillna('') + " " + \
                     df["author"].fillna('')

    # Vectorize
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df["combined"])

    # Cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix)

    # Books the user already borrowed
    borrowed_ids = list(
        BorrowedBooks.objects.filter(member_id=user_id).values_list('book_id', flat=True)
    )

    sim_scores = {}
    for book_id in borrowed_ids:
        try:
            idx = df.index[df['id'] == book_id].tolist()[0]
            scores = list(enumerate(cosine_sim[idx]))
            for i, score in scores:
                if df.iloc[i]["id"] not in borrowed_ids:
                    sim_scores[df.iloc[i]["id"]] = sim_scores.get(df.iloc[i]["id"], 0) + score
        except IndexError:
            continue

    # Normalize scores to percentages
    if sim_scores:
        max_score = max(sim_scores.values())
    else:
        max_score = 1  # Avoid division by zero

    sorted_books = sorted(sim_scores.items(), key=lambda x: x[1], reverse=True)

    # Get top N and match percent
    top_book_ids = [book_id for book_id, _ in sorted_books[:top_n]]
    id_to_percent = {book_id: round((score / max_score) * 100, 1) for book_id, score in sorted_books[:top_n]}

    # Fetch books and enrich with match %
    recommended_books = []
    for book in Book.objects.filter(id__in=top_book_ids):
        recommended_books.append({
            'title': book.title,
            'author': book.author,
            'match_percent': id_to_percent.get(book.id, 0),
        })

    return recommended_books