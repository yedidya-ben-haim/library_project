from db_connection import DbConnection

connection_db = DbConnection()


class BookDB:
    """
    Responsible for all SQL operations against the books table.
    """

    def create_book(self, data: dict):
        """
        Creates a new book and inserts it into the table,

        Sets is_available=True

        Returns TRUE if the book was created and inserted into the table
        """
        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)

        data_value = (data["title"], data["author"], data["genre"])


        query = f"INSERT INTO books (title, author, genre, is_available) VALUES (%s, %s, %s, TRUE);"

        cursor.execute(query, data_value)

        conn.commit()
        is_create = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return is_create

    def get_all_books(self):
        """
            Returns the list of all books
        """
        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """SELECT * FROM books;"""

        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    def get_book_by_id(self, id):
        """
            Returns one book by ID or None
        """
        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = f"SELECT * FROM books WHERE id = {id}"

        cursor.execute(query)
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row

    def update_book(self, id, data: dict):
        """
            Updates a book by ID and submitted fields
            Returns TRUE if updated
        """

        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)

        in_part = [f"{key}=%s" for key in data.keys()]
        in_str = ", ".join(in_part)

        data_value = list(data.values()) + [id]


        query = f"UPDATE books SET {in_str} WHERE id = %s"

        cursor.execute(query, data_value)

        conn.commit()
        is_update = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return is_update

    def set_available(self, id, val, member_id):
        """
        Updates the is_available and borrowed_by_member_id fields,
        based on the book ID ang member ID sent,
        Checking if available,
        returns TRUE if done
        """
        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)
        is_update = False

        cursor.execute("SELECT is_available FROM books WHERE id = %s;", (id,))
        row = cursor.fetchone()
        is_available = row["is_available"]


        if val != is_available:
            query = f"UPDATE books SET is_available=%s, borrowed_by_member_id=%s WHERE id = %s"
            cursor.execute(query, (val, member_id, id))

            conn.commit()
            is_update = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return is_update

    def count_total_books(self):
        """
            Returns the total number of books in the database.
        """
        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = f"SELECT COUNT(*) as total_book FROM books;"

        cursor.execute(query)
        rows = cursor.fetchone()
        total_book = rows["total_book"]

        cursor.close()
        conn.close()

        return total_book

    def count_available_books(self):
        """
            Returns the number of books with is_available=True
        """
        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """SELECT COUNT(*) as total_available 
                    FROM books
                    WHERE is_available=True;
                """
        cursor.execute(query)
        row = cursor.fetchone()
        total_available = row["total_available"]

        cursor.close()
        conn.close()

        return total_available

    def count_borrowed_books(self):
        """
            Returns the number of books with is_available=False
        """
        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """SELECT COUNT(*) as total_borrowed
                            FROM books
                            WHERE is_available=False;
                        """
        cursor.execute(query)
        row = cursor.fetchone()
        total_borrowed = row["total_borrowed"]

        cursor.close()
        conn.close()

        return total_borrowed

    def count_by_genre(self, genre):
        """
            Returns the number of books by genre
        """
        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """SELECT genre,COUNT(*) as total_genre
                                    FROM books
                                    WHERE genre=%s;
                                """
        cursor.execute(query, (genre,))
        row = cursor.fetchone()
        total_genre = row["total_genre"]

        cursor.close()
        conn.close()

        return total_genre

    def count_active_borrows_by_member(self, member_id):
        """
            Count how many books the member currently owns to enforce the 3-book rule
        """
        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """SELECT COUNT(*) as borrowed_books
                    FROM books
                    WHERE borrowed_by_member_id=%s;
                """
        cursor.execute(query, (member_id,))
        row = cursor.fetchone()
        borrowed_books = row["borrowed_books"]

        cursor.close()
        conn.close()

        return borrowed_books



data = {"title":"book2", "genre":"Science", "author":"harry"}

book_db = BookDB()
print(book_db.count_active_borrows_by_member(2))
