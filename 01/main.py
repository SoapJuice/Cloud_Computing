from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3

# Initialize Database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

class LibraryAPI(BaseHTTPRequestHandler):

    def _send_response(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        if self.path == "/books":
            cursor.execute("SELECT * FROM books")
            books = [{"id": row[0], "name": row[1], "author": row[2], "genre": row[3]} for row in cursor.fetchall()]
            self._send_response(200, books)

        elif self.path.startswith("/books/"):
            book_id = self.path.split("/")[-1]
            cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
            book = cursor.fetchone()

            if book:
                self._send_response(200, {"id": book[0], "name": book[1], "author": book[2], "genre": book[3]})
            else:
                self._send_response(404, {"error": "Book not found"})
        elif self.path == "/users":
            cursor.execute("SELECT * FROM users")
            users = [{"id": row[0], "name": row[1], "e-mail": row[2]} for row in cursor.fetchall()]
            self._send_response(200, users)

        elif self.path.startswith("/users/"):
            user_id = self.path.split("/")[-1]
            cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
            user = cursor.fetchone()

            if user:
                self._send_response(200, {"id": user[0], "name": user[1], "email": user[2]})
            else:
                self._send_response(404, {"error": "User not found"})
        elif self.path == "/loans":
            cursor.execute("SELECT * FROM loans")
            loans = [{"id": row[0], "user_id": row[1], "book_id": row[2], "loan_date": row[3], "return_date": row[4]} for row in cursor.fetchall()]
            self._send_response(200, loans)

        elif self.path.startswith("/loans/"):
            loan_id = self.path.split("/")[-1]
            cursor.execute("SELECT * FROM loans WHERE id=?", (loan_id,))
            loan = cursor.fetchone()

            if loan:
                self._send_response(200, {"id": loan[0], "user_id": loan[1], "book_id": loan[2], "loan_date": loan[3], "return_date": loan[4]})
            else:
                self._send_response(404, {"error": "User not found"})
        else:
            self._send_response(404, {"error": "Invalid endpoint"})

        conn.close()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data)
            if self.path == "/books":
                name, author, genre = data["name"], data["author"], data["genre"]

                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO books (name, author, genre) VALUES (?, ?, ?)", (name, author, genre))
                conn.commit()
                conn.close()
                self._send_response(201, {"message": "Book added successfully"})

            elif self.path == "/users":
                name, email = data["name"], data["email"]

                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
                conn.commit()
                conn.close()
                self._send_response(201, {"message": "User added successfully"})

            elif self.path == "/loans":
                user_id, book_id, loan_date, return_date = data["name"], data["book_id"], data["loan_date"], data["return_date"]

                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO loans (user_id, book_id, loan_date, return_date) VALUES (?, ?, ?, ?)", (user_id, book_id, loan_date, return_date))
                conn.commit()
                conn.close()
                self._send_response(201, {"message": "Loan added successfully"})
            else:
                self._send_response(404, {"error": "Invalid endpoint"})
        except Exception as e:
            self._send_response(400, {"error": str(e)})

    def do_PUT(self):
        if self.path.startswith("/books/"):
            book_id = self.path.split("/")[-1]
            content_length = int(self.headers["Content-Length"])
            put_data = self.rfile.read(content_length)

            try:
                data = json.loads(put_data)
                name, author, genre = data.get("name"), data.get("author"), data.get("genre")

                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE books SET name=?, author=?, genre=? WHERE id=?", (name, author, genre, book_id))
                conn.commit()

                if cursor.rowcount == 0:
                    self._send_response(404, {"error": "Book not found"})
                else:
                    self._send_response(200, {"message": "Book updated successfully"})

                conn.close()

            except Exception as e:
                self._send_response(400, {"error": str(e)})
        elif self.path.startswith("/users/"):
            user_id = self.path.split("/")[-1]
            content_length = int(self.headers["Content-Length"])
            put_data = self.rfile.read(content_length)

            try:
                data = json.loads(put_data)
                name, email = data.get["name"], data.get["email"]

                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET name=?, email=? WHERE id=?", (name, email, user_id))
                conn.commit()

                if cursor.rowcount == 0:
                    self._send_response(404, {"error": "User not found"})
                else:
                    self._send_response(200, {"message": "User updated successfully"})

                conn.close()

            except Exception as e:
                self._send_response(400, {"error": str(e)})
        elif self.path.startswith("/loans/"):
            loan_id = self.path.split("/")[-1]
            content_length = int(self.headers["Content-Length"])
            put_data = self.rfile.read(content_length)

            try:
                data = json.loads(put_data)
                user_id, book_id, loan_date, return_date = data["user_id"], data["book_id"], data["loan_date"], data[
                    "return_date"]
                # name, email = data.get["name"], data.get["email"]

                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE loans SET user_id=?, book_id=?, loan_date=?, return_date=? WHERE id=?", (user_id, book_id, loan_date, return_date, loan_id))
                conn.commit()

                if cursor.rowcount == 0:
                    self._send_response(404, {"error": "Loan not found"})
                else:
                    self._send_response(200, {"message": "Loan updated successfully"})

                conn.close()

            except Exception as e:
                self._send_response(400, {"error": str(e)})

    def do_DELETE(self):
        if self.path.startswith("/books/"):
            book_id = self.path.split("/")[-1]

            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
            conn.commit()

            if cursor.rowcount == 0:
                self._send_response(404, {"error": "Book not found"})
            else:
                self._send_response(200, {"message": "Book deleted successfully"})

            conn.close()
        elif self.path.startswith("/users/"):
            user_id = self.path.split("/")[-1]

            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
            conn.commit()

            if cursor.rowcount == 0:
                self._send_response(404, {"error": "User not found"})
            else:
                self._send_response(200, {"message": "User deleted successfully"})

            conn.close()
        elif self.path.startswith("/loans/"):
            loan_id = self.path.split("/")[-1]

            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id=?", (loan_id,))
            conn.commit()

            if cursor.rowcount == 0:
                self._send_response(404, {"error": "Loan not found"})
            else:
                self._send_response(200, {"message": "Loan deleted successfully"})

            conn.close()


def run(server_class=HTTPServer, handler_class=LibraryAPI, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Running on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
