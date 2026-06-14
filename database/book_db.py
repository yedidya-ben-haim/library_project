from db_connection import get_connection




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
        conn = get_connection()
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
        conn = get_connection()
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
        conn = get_connection()
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

        conn = get_connection()
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
        conn = get_connection()
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
        conn = get_connection()
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
        conn = get_connection()
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



data = {"title":"book", "genre":"Science"}

book_db = BookDB()
print(book_db.count_available_books())