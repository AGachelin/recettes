import sys
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

# Create the connection
con = QSqlDatabase.addDatabase("QSQLITE")
con.setDatabaseName("../data/recettes.db")
# Open the connection
if not con.open():
    print("Database Error: %s" % con.lastError().databaseText())
    sys.exit(1)

# Create a query and execute it right away using .exec()
createTableQuery = QSqlQuery()
createTableQuery.exec(
    """CREATE TABLE recettes(id INTEGER PRIMARY KEY UNIQUE NOT NULL,nom TEXT,note DOUBLE default(0), duree DOUBLE default(0), duree1 DOUBLE default(0), duree2 DOUBLE default(0),nb INT default(0),t INT default(0))"""
)
createTableQuery.exec(
    """CREATE TABLE ingredients(nom TEXT PRIMARY KEY UNIQUE NOT NULL, arbitraire bool default(False), masse bool default(False), volume bool default(False), rho double default(0))"""
)
createTableQuery.exec(
    """CREATE TABLE unite(nom TEXT PRIMARY KEY UNIQUE NOT NULL,u_base TEXT)"""
)
createTableQuery.exec(
    """CREATE TABLE ing_bis(id INTEGER PRIMARY KEY UNIQUE NOT NULL)"""
)

createTableQuery.exec("""INSERT INTO unite (nom,u_base) VALUES ('masse','g')""")
createTableQuery.exec("""INSERT INTO unite (nom,u_base) VALUES ('volume','mL')""")