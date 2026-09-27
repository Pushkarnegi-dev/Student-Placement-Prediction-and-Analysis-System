import pyodbc

SERVER = r"DESKTOP-N86S9T3\SQLEXPRESS"
DATABASE = "StudentPlacementDB"

def get_connection():
    connection = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"Trusted_Connection=yes;"
    )

    return connection

if __name__ == "__main__":
    conn = get_connection()
    print("SQL Server connection successful!")
    conn.close()