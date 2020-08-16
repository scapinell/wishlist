import sys

from PyQt5.QtSql import (QSqlDatabase, QSqlQuery)


class CreateWLDATA:
    database = QSqlDatabase.addDatabase('QSQLITE')  # specify the SQL driver
    database.setDatabaseName('w_list.db')
    if not database.open():
        print("Unable to open")
        sys.exit(1)

    query = QSqlQuery()
    query.exec_("DROP TABLE w_list")

    query.exec_("""CREATE TABLE w_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                title VARCHAR(30) NOT NULL,
                price DECIMAL(8, 2),
                comment VARCHAR(30) NOT NULL,
                website VARCHAR(30))""")
    query.prepare("""INSERT INTO w_list (title, price, comment, website) VALUES (?, ?, ?, ?)""")

    titles = ["bike", "game"]
    prices = ["12000", "500"]
    comment = ["want red", "without add on"]
    websites = ["www.mysite.com", "www.random.com"]

    for i, t in enumerate(titles):
        query.addBindValue(t)
        query.addBindValue(prices[i])
        query.addBindValue(comment[i])
        query.addBindValue(websites[i])
        query.exec_()

    # sys.exit(0)


if __name__ == "__main__":
    CreateWLDATA()

    # sys.exit(0)

