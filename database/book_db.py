from db_connection import get_connection




class BookDB:
    """
    Responsible for all SQL operations against the books table.
    """
    def __init__(self):
        pass

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



book_db = BookDB()
print(book_db.get_all_books())