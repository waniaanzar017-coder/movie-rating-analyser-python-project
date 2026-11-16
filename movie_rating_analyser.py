import csv
import os
from statistics import mean, median

FILE_NAME = "movies.csv"
FIELDS = ["title", "genre", "year", "rating"]


def load_movies():
    movies = []
    if not os.path.exists(FILE_NAME):
        return movies
    with open(FILE_NAME, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            movies.append({
                "title": row["title"],
                "genre": row["genre"],
                "year": int(row["year"]),
                "rating": float(row["rating"]),
            })
    return movies


def save_movies(movies):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(movies)


def read_rating():
    while True:
        try:
            r = float(input("Rating (0-10): "))
            if 0 <= r <= 10:
                return r
            print("Rating must be between 0 and 10.")
        except ValueError:
            print("Please enter a number.")


def read_year():
    while True:
        try:
            y = int(input("Release year: "))
            if 1888 <= y <= 2100:
                return y
            print("Enter a realistic year.")
        except ValueError:
            print("Please enter a valid year.")


def add_movie(movies):
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    genre = input("Genre: ").strip().title()
    year = read_year()
    rating = read_rating()
    movies.append({"title": title, "genre": genre, "year": year, "rating": rating})
    save_movies(movies)
    print(f"Added '{title}'.")


def show_all(movies):
    if not movies:
        print("No movies yet.")
        return
    print(f"\n{'No.':<4}{'Title':<28}{'Genre':<14}{'Year':<6}{'Rating'}")
    print("-" * 60)
    for i, m in enumerate(movies, 1):
        print(f"{i:<4}{m['title'][:26]:<28}{m['genre'][:12]:<14}{m['year']:<6}{m['rating']}")


def summary(movies):
    if not movies:
        print("No data to analyse.")
        return
    ratings = [m["rating"] for m in movies]
    best = max(movies, key=lambda m: m["rating"])
    worst = min(movies, key=lambda m: m["rating"])
    print("\n Summary ")
    print(f"Total movies   : {len(movies)}")
    print(f"Average rating : {mean(ratings):.2f}")
    print(f"Median rating  : {median(ratings):.2f}")
    print(f"Highest        : {best['title']} ({best['rating']})")
    print(f"Lowest         : {worst['title']} ({worst['rating']})")


def top_n(movies, n=5):
    ranked = sorted(movies, key=lambda m: m["rating"], reverse=True)[:n]
    print(f"\n Top {len(ranked)} movies")
    for i, m in enumerate(ranked, 1):
        print(f"{i}. {m['title']} ({m['year']}) - {m['rating']}")


def genre_analysis(movies):
    groups = {}
    for m in movies:
        groups.setdefault(m["genre"], []).append(m["rating"])
    print("\n Genre-wise average ")
    for genre, rs in sorted(groups.items(), key=lambda g: mean(g[1]), reverse=True):
        print(f"{genre:<15} avg {mean(rs):.2f}  ({len(rs)} movies)")


def distribution(movies):
    bands = {"0-2": 0, "2-4": 0, "4-6": 0, "6-8": 0, "8-10": 0}
    for m in movies:
        r = m["rating"]
        key = "0-2" if r < 2 else "2-4" if r < 4 else "4-6" if r < 6 else "6-8" if r < 8 else "8-10"
        bands[key] += 1
    print("\n--- Rating distribution ---")
    for band, count in bands.items():
        print(f"{band:<5}| {'#' * count} {count}")


def search(movies):
    term = input("Search title: ").strip().lower()
    found = [m for m in movies if term in m["title"].lower()]
    if not found:
        print("No match.")
    for m in found:
        print(f"{m['title']} | {m['genre']} | {m['year']} | {m['rating']}")


def delete_movie(movies):
    show_all(movies)
    try:
        idx = int(input("Number to delete: ")) - 1
        removed = movies.pop(idx)
        save_movies(movies)
        print(f"Deleted '{removed['title']}'.")
    except (ValueError, IndexError):
        print("Invalid choice.")


def main():
    movies = load_movies()
    menu = """ MOVIE RATING ANALYSER
1. Add movie          5. Genre-wise analysis
2. View all movies    6. Rating distribution
3. Summary stats      7. Search movie
4. Top 5 movies       8. Delete movie
0. Exit
"""


    while True:
        print(menu)
        choice = input("Choose: ").strip()
        if choice == "1":
            add_movie(movies)
        elif choice == "2":
            show_all(movies)
        elif choice == "3":
            summary(movies)
        elif choice == "4":
            top_n(movies)
        elif choice == "5":
            genre_analysis(movies)
        elif choice == "6":
            distribution(movies)
        elif choice == "7":
            search(movies)
        elif choice == "8":
            delete_movie(movies)
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()