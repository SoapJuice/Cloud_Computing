from flask import Flask, jsonify
import requests


app = Flask(__name__)

LIBRARY_API = "http://localhost:8080"
OPEN_LIBRARY_API = "https://openlibrary.org/api/books"
RANDOM_USER_API = "https://randomuser.me/api/"


@app.route('/api/books', methods=['GET'])
def get_books():
    try:
        response = requests.get(f"{LIBRARY_API}/books")
        if response.status_code != 200:
            return jsonify({"error": "Library service unavailable"}), 503

        books = response.json()

        for book in books:
            if 'isbn' in book:
                cover_response = requests.get(
                    f"{OPEN_LIBRARY_API}?bibkeys=ISBN:{book['isbn']}&format=json&jscmd=data"
                )
                if cover_response.status_code == 200:
                    cover_data = cover_response.json()
                    if f"ISBN:{book['isbn']}" in cover_data:
                        book['cover'] = cover_data[f"ISBN:{book['isbn']}"].get('cover', {}).get('medium', '')

        return jsonify(books)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/users/random', methods=['GET'])
def get_random_user():
    try:
        response = requests.get(f"{RANDOM_USER_API}?nat=us")
        if response.status_code != 200:
            return jsonify({"error": "Random user service unavailable"}), 503

        user_data = response.json()['results'][0]
        formatted_user = {
            "name": f"{user_data['name']['first']} {user_data['name']['last']}",
            "email": user_data['email']
        }

        save_response = requests.post(
            f"{LIBRARY_API}/users",
            json=formatted_user
        )

        if save_response.status_code != 201:
            return jsonify({"error": "Could not save user to library"}), 500

        return jsonify(formatted_user)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/loans', methods=['GET'])
def get_loans_with_details():
    try:
        loans_response = requests.get(f"{LIBRARY_API}/loans")
        if loans_response.status_code != 200:
            return jsonify({"error": "Library service unavailable"}), 503

        loans = loans_response.json()

        for loan in loans:
            user_response = requests.get(f"{LIBRARY_API}/users/{loan['user_id']}")
            if user_response.status_code == 200:
                loan['user'] = user_response.json()

            book_response = requests.get(f"{LIBRARY_API}/books/{loan['book_id']}")
            if book_response.status_code == 200:
                loan['book'] = book_response.json()

        return jsonify(loans)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)