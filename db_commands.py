import sqlite3


class Database:
    def __init__(self, path_to_db="C:/Users/User/Documents/GitHub/AvtoSavdo/avtosavdo/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data


        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO products_user (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM products_user"
        return await self.execute(sql, fetch=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM products_user"
        print(sql)
        return await self.execute(sql, fetchval=True)

    async def add_product(
        self,
        category_code,
        category_name,
        subcategory_code,
        subcategory_name,
        productname,
        photo=None,
        price=None,
        description="",
    ):
        sql = "INSERT INTO products_product (category_code, category_name, subcategory_code, subcategory_name, productname, photo, price, description) VALUES($1, $2, $3, $4, $5, $6, $7, $8) returning *"
        return await self.execute(
            sql,
            category_code,
            category_name,
            subcategory_code,
            subcategory_name,
            productname,
            photo,
            price,
            description,
            fetchrow=True,
        )

    async def get_categories(self):
        sql = "SELECT DISTINCT category_name, category_code FROM products_product"
        return await self.execute(sql, fetch=True)

    async def get_subcategories(self, category_code):
        sql = f"SELECT DISTINCT subcategory_name, subcategory_code FROM products_product WHERE category_code='{category_code}'"
        return await self.execute(sql, fetch=True)

    async def count_products(self, category_code, subcategory_code=None):
        if subcategory_code:
            sql = f"SELECT COUNT(*) FROM products_product WHERE category_code='{category_code}' AND subcategory_code='{subcategory_code}'"
        else:
            sql = f"SELECT COUNT(*) FROM products_product WHERE category_code='{category_code}'"
        return await self.execute(sql, fetchval=True)

    async def get_products(self, category_code, subcategory_code):
        sql = f"SELECT * FROM products_product WHERE category_code='{category_code}' AND subcategory_code='{subcategory_code}'"
        return await self.execute(sql, fetch=True)

    async def get_product(self, product_id):
        sql = f"SELECT * FROM products_product WHERE id={product_id}"
        return await self.execute(sql, fetchrow=True)

    async def drop_products(self):
        await self.execute("DROP TABLE products_product", execute=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")