from database.connection import connection_factory

def get_connection():
    return connection_factory.get_db_connection()

def get_products(active_only):
    conn = get_connection()
    cursor = conn.cursor()
    if active_only:
        cursor.execute("SELECT ID_Product, Name, Description, Active FROM Product WHERE Active = ?;", (active_only,))
    else:
        cursor.execute("SELECT ID_Product, Name, Description, Active FROM Product;")
    rows = cursor.fetchall()
    conn.close()
    return rows


def create_product(name, description, active):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Product (Name, Description, Active) VALUES (?, ?, ?);",
        (name, description, active)
    )
    conn.commit()
    conn.close()


def update_product(product_id, name, description, active):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Product SET Name = ?, Description = ?, Active = ? WHERE ID_Product = ?;",
        (name, description, active, product_id)
    )
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   DELETE
                   FROM Product
                   WHERE ID_Product = ?
                   """, (product_id,))

    conn.commit()
    conn.close()
