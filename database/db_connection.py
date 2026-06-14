import mysql.connector

def get_connection():
    """
        Creates a connection to the database and returns it.
    """
    return mysql.connector.connect(user='root',
                                   password='secret',
                                   host='127.0.0.1',
                                   database='library_db')


def create_tables():
    """
        Creates the 'members' and 'books' tables if they do not exist
        — runs at server startup, at the beginning of the main function
    """
    members_tables_query = """CREATE TABLE IF NOT EXISTS members (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                name VARCHAR(50) NOT NULL,
                                email VARCHAR(50) UNIQUE NOT NULL,
                                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                                total_borrows INT NOT NULL DEFAULT 0
                                );
                            """

    books_tables_query = """CREATE TABLE IF NOT EXISTS books (
                                    id INT PRIMARY KEY AUTO_INCREMENT,
                                    title VARCHAR(50) NOT NULL,
                                    author VARCHAR(50) NOT NULL,
                                    genre ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other') NOT NULL,
                                    is_available BOOLEAN NOT NULL DEFAULT TRUE,
                                    borrowed_by_member_id INT NULL
                                    );
                                """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(members_tables_query)
    cursor.execute(books_tables_query)

    conn.commit()

    cursor.close()
    conn.close()

