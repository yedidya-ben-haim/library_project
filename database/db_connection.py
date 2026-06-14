import mysql.connector


class DbConnection:
    def __init__(self):
        self.user = user='root'
        self.password='secret'
        self.host='127.0.0.1'
        self.database='library_db'

    def get_connection(self):
        """
            Creates a connection to the database and returns it.
        """
        return mysql.connector.connect(user=self.user,
                                       password=self.password,
                                       host=self.host,
                                       database=self.database)


    def create_tables(self):
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

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(members_tables_query)
        cursor.execute(books_tables_query)

        conn.commit()

        cursor.close()
        conn.close()

