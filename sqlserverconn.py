import pyodbc

class supports(object):
    def __init__(self, conn):
        self.conn = conn

    def getproduct(self):
        cursor = self.conn.cursor()
        cursor.execute("Select * From [base_product]")
        count = 0
        products = {}
        for row in cursor:
            product = {
                'prodindex':row[0],
                'productcode':row[1],
                'description':row[2],
                'category':row[3],
            }
            products.update(product)            
        return products

    # def create(conn):
    #     print "======================== CREATE ========================"
    #     cursor = conn.cursor()
    #     cursor.execute(
    #         "INSERT INTO [user](f_name,l_name,m_name,age) values(?,?,?,?);",
    #         (
    #             "Eddie",
    #             "Cabellon",
    #             "Ocariza",
    #             33
    #         )
    #     )
    #     conn.commit()
    #     read(conn)

    # def update(conn):
    #     print "======================== UPDATE ========================"
    #     cursor = conn.cursor()
    #     cursor.execute(
    #         'UPDATE [user] SET l_name = ?,m_name = ?,age = ? WHERE f_name = ?;',
    #         (            
    #             'Cabellon',
    #             'Ocariza',
    #             33,
    #             'Eddie'
    #         )
    #     )
    #     conn.commit()
    #     read(conn)

    # def delete(conn):
    #     print "======================== DELETE ========================"
    #     cursor = conn.cursor()
    #     cursor.execute(
    #         "DELETE FROM [user];"
    #     )
    #     conn.commit()
    #     read(conn)

# conn = pyodbc.connect(
#     "Driver={SQL Server Native Client 11.0};"
#     "Server=DESKTOP-JRNF2CG\SQLEXPRESS;"
#     "Database=python_db;"
#     "Trusted_Connection=yes;"
# )

# create(conn)
# read(conn)
# update(conn)
# delete(conn)