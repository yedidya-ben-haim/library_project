from database.db_connection import DbConnection

connection_db = DbConnection()


class MemberDB:
    """
    Responsible for all SQL operations against the member table.
    """

    def create_member(self, data: dict):
        """
        Creates a new members and inserts it into the table,

        Sets is_active=True, total_borrows=0

        Returns TRUE if the members was created and inserted into the table
        """
        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)

        data_value = (data["name"], data["email"])
        is_create = False

        query = f"INSERT INTO members (name, email, is_active, total_borrows) VALUES (%s, %s, TRUE, 0);"


        try:
            cursor.execute(query, data_value)
            conn.commit()
            is_create = cursor.rowcount > 0
        except Exception as e:
            raise KeyError

        finally:
            cursor.close()
            conn.close()

        return is_create


    def get_all_members():
        pass

    def get_member_by_id(id):
        """
            Returns one member by ID or None
        """
        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = f"SELECT * FROM members WHERE id = {id}"

        cursor.execute(query)
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row

    def update_member(id, data):
        pass

    def deactivate_member(id):
        pass

    def count_active_members():
        pass

    def get_top_member():
        pass

    def

data = {"name":"yedidya",
       "email":"bhyedidya@gmail.com"}

member_db = MemberDB()
print(member_db.create_member(data))