from database.db_connection import DbConnection
from logs import log_config
connection_db = DbConnection()
import logging

logger = logging.getLogger(__name__)

class MemberDB:
    """
        Responsible for all SQL operations against the members table.
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

    def get_all_members(self):
        """
            Returns the list of all members
        """
        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """SELECT * FROM members;"""

        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    def get_member_by_id(self, id):
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

    def update_member(self, id, data):
        """
            Updates a member by ID and submitted fields
            Returns TRUE if updated
        """
        if not self.get_member_by_id(id):
            raise KeyError

        conn = connection_db.get_connection()
        cursor = conn.cursor(dictionary=True)

        in_part = [f"{key}=%s" for key in data.keys()]
        in_str = ", ".join(in_part)

        data_value = list(data.values()) + [id]

        query = f"UPDATE members SET {in_str} WHERE id = %s"

        cursor.execute(query, data_value)

        conn.commit()
        is_update = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return is_update

    def deactivate_member(self, id):
        is_update = self.update_member(id,{"is_active": 0})
        return is_update

    def activate_member(self, id):
        is_update = self.update_member(id, {"is_active": 1})
        return is_update

    def increment_borrows(self, id):
        """
            Increases total_borrows by 1
            Return true if updated
        """
        member = self.get_member_by_id(id)
        print(member)
        new_borrows = member["total_borrows"] + 1
        data = {"total_borrows": new_borrows}
        is_update = self.update_member(id, data)

        return is_update



    def count_active_members():
        pass

    def get_top_member():
        pass



data = {"name":"yedidya",
       "email":"bhyedidya@gmail.com"}

member_db = MemberDB()
print(member_db.activate_member(1))