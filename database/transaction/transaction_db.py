from database.connection import connection_factory

def get_connection():
    return connection_factory.get_db_connection()

def get_product_balance(product_id: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            COALESCE(SUM(
                CASE 
                    WHEN Type = 'INPUT' THEN Quantity
                    WHEN Type = 'OUTPUT' THEN -Quantity
                END
            ), 0)
        FROM ProductTransaction
        WHERE ID_Product = ?
    """, (product_id,))

    balance = cursor.fetchone()[0]
    conn.close()
    return balance

def get_transactions_by_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.ID_Transaction,
            t.Date,
            t.Type,
            t.Quantity,
            u.Login AS User,
            t.Description
        FROM ProductTransaction t
        JOIN User u ON u.ID_User = t.ID_User
        WHERE t.ID_Product = ?
        ORDER BY t.Date DESC
    """, (product_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def create_transaction(user_id, product_id, t_type, quantity, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ProductTransaction
        (ID_User, ID_Product, Type, Quantity, Description)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, product_id, t_type, quantity, description))

    conn.commit()
    conn.close()