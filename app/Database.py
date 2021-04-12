import psycopg2
import psycopg2.extras
from typing import Optional, Tuple
from settings import DB_CONFIG
from models import User, PartialUser


class Database:
    __DB = None

    @classmethod
    def getDB(cls):
        if cls.__DB is None:
            cls.__DB = psycopg2.connect(
                host=DB_CONFIG.host,
                database=DB_CONFIG.database,
                user=DB_CONFIG.user,
                password=DB_CONFIG.password,
                port=DB_CONFIG.port,
            )
        return cls.__DB

    @classmethod
    def query(cls, query: str, args: Optional[Tuple] = tuple()):
        print("args ===>", args)
        print("length args ===>", len(args))
        with cls.getDB() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(query, args)
            conn.commit()
            return cur


class UserTable():

    def get_users(self, limit=10, offset=1, sort="id:asc"):
        attr, order = sort.split(':')
        query = f"""SELECT *
        FROM person
        ORDER BY {attr} {order}
        LIMIT {limit}
        offset {offset}"""
        with Database.query(query) as cur:
            users = [dict(u) for u in cur.fetchall()]
            return users

    def get_user_by_id(self, user_id):
        query = f"""SELECT *
            FROM person
            WHERE id=%s;"""
        with Database.query(query, (user_id,)) as cur:
            user = cur.fetchone()
            return dict(user) if user is not None else None

    def post_user(self, user_data: PartialUser):
        prepare_data = (
            user_data.first_name, user_data.last_name,
            user_data.gender.value, user_data.email,
            user_data.date_of_birth.isoformat(),
            user_data.country_of_birth)
        query = """INSERT INTO person(
                first_name,
                last_name,
                gender,
                email,
                date_of_birth,
                country_of_birth
            ) VALUES(%s,%s,%s,%s,%s,%s);"""
        with Database.query(query, args=prepare_data) as cur:
            return {"success": True}

    def patch_user(self, user_id: int, user_data: PartialUser):
        prepare_data = (
            user_data.first_name, user_data.last_name,
            user_data.gender.value, user_data.email,
            user_data.date_of_birth.isoformat(),
            user_data.country_of_birth, str(user_id))
        query = """UPDATE person set 
                first_name=%s,
                last_name=%s,
                gender=%s,
                email=%s,
                date_of_birth=%s,
                country_of_birth=%s
            WHERE id=%s;"""
        with Database.query(query, prepare_data) as cur:
            return cur.rowcount

    # def update_user(self, new_data):
    #     query = """UPDATE TABLE person set
    #     pass

    # def delete_user(self, id):
    #     query = "DELETE FROM person WHERE id=$1"
    #     Database.query(query, (id,))