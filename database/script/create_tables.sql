PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS "User" (
    ID_User INTEGER PRIMARY KEY AUTOINCREMENT,
    Login TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Registered_Date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Product (
    ID_Product INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Description TEXT,
    Active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS ProductTransaction (
    ID_Transaction INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_User INTEGER NOT NULL,
    ID_Product INTEGER NOT NULL,
    Type TEXT NOT NULL,
    Quantity INTEGER NOT NULL,
    Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Description TEXT,

    FOREIGN KEY (ID_User) REFERENCES User(ID_User),
    FOREIGN KEY (ID_Product) REFERENCES Product(ID_Product)
);

CREATE TRIGGER IF NOT EXISTS trg_validate_transaction_type
BEFORE INSERT ON ProductTransaction
FOR EACH ROW
BEGIN
    SELECT
        CASE
            WHEN NEW.Type NOT IN ('INPUT', 'OUTPUT') THEN
                RAISE(ABORT, 'Tipo de transação inválido. Use ENTRADA ou SAIDA.')
        END;
END;

CREATE TRIGGER IF NOT EXISTS trg_validate_transaction_quantity
BEFORE INSERT ON ProductTransaction
FOR EACH ROW
BEGIN
    SELECT
        CASE
            WHEN NEW.Quantity <= 0 THEN
                RAISE(ABORT, 'Quantidade deve ser maior que zero.')
        END;
END;

CREATE TRIGGER IF NOT EXISTS trg_check_product_active
BEFORE INSERT ON ProductTransaction
FOR EACH ROW
BEGIN
    SELECT
        CASE
            WHEN (
                SELECT Active
                FROM Product
                WHERE ID_Product = NEW.ID_Product
            ) = 0 THEN
                RAISE(
                    ABORT,
                    'Nao e possivel realizar transacoes para um produto inativo.'
                )
        END;
END;

CREATE TRIGGER IF NOT EXISTS trg_prevent_negative_stock
BEFORE INSERT ON ProductTransaction
FOR EACH ROW
WHEN NEW.Type = 'OUTPUT'
BEGIN
    SELECT
        CASE
            WHEN (
                COALESCE((
                    SELECT
                        SUM(
                            CASE
                                WHEN Type = 'INPUT' THEN Quantity
                                WHEN Type = 'OUTPUT' THEN -Quantity
                            END
                        )
                    FROM ProductTransaction
                    WHERE ID_Product = NEW.ID_Product
                ), 0) - NEW.Quantity < 0
            ) THEN
                RAISE(ABORT, 'Estoque insuficiente para realizar a saída.')
        END;
END;