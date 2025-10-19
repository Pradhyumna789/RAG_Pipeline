import argparse
import json
import string
import nltk
from nltk.stem import PorterStemmer

porter_stemmer = PorterStemmer()

def stemming(movie_title):
    stemmed_words = []
    for word in movie_title:
        stemmed_words.append(porter_stemmer.stem(word))
    return stemmed_words

def filter_stop_words(movie_title):
    with open ("data/stopwords.txt", "r") as file:
        file_content = file.read()
        stop_words = file_content.splitlines()

    filtered_words = []
    for word in movie_title:
        if word not in stop_words:
            filtered_words.append(word)
    return filtered_words

def tokenization(movie_title):
    movie_title_tokenized = movie_title.split(" ")
    return movie_title_tokenized

def punctuation_removal(movie_title):
    text = movie_title.lower()
    text_without_punctuation = text.translate(str.maketrans('', '', string.punctuation))
    return text_without_punctuation

def main() -> None:
    with open("data/movies.json", "r") as file:
        movies_data = json.load(file)

    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")

            search_query = args.query
            results = []

            movies = movies_data["movies"]
            query_words = stemming(filter_stop_words(tokenization(punctuation_removal(search_query))))

            for movie in movies:
                title_processed = stemming(filter_stop_words(tokenization(punctuation_removal(movie["title"]))))

                all_found = True
                all_found_2 = False
                for q in query_words:
                    if q not in title_processed:    
                        all_found = False
                        break

                for q in query_words:
                    for processed_word in title_processed:
                        if q in processed_word:
                            all_found_2 = True
                            break

                if all_found:
                    results.append(movie["title"])

                if all_found_2:
                    results.append(movie["title"])

            for i in range(len(results)):
                print(f"{i + 1}. {results[i]}")

        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
