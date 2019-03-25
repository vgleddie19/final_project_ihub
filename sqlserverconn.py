import pyodbc

class supports(object):
    conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=PC01\SQLEXPRESS;"
    "Database=python_db;"
    "Trusted_Connection=yes;"
    )
    def __init__(self):
        pass

    def getproduct():
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