import psycopg2
from psycopg2.extensions import AsIs

class Database:


    def __init__(self, db_name):
        self.conn = psycopg2.connect("dbname=" + db_name)


    def selectNumberOfUsers(self):
        cur = self.conn.cursor()
        cur.execute('select count(*) from users;')
        result = cur.fetchone()
        cur.close()
        return result[0]

    def selectAllTables(self):
        cur = self.conn.cursor()
        cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
        result_tuple = cur.fetchall()
        result = []
        for row in result_tuple:
            result.append(row[0])
        cur.close()

        return result

    def generateTableData(self, table):
        cur = self.conn.cursor()
        #PRONE FOR SQL INJECTION; DO NOT USE WITH SEARCH FIELDS!
        cur.execute("SELECT * FROM %(table)s LIMIT 1000", {"table": AsIs(table)})
        colnames = [desc[0] for desc in cur.description]
        result_tuple = cur.fetchall()
        cur.close()
        results = {}
        results['table'] = table
        results['cols'] = colnames
        print (results)
        all_tuples = []
        for result in result_tuple:
            res_list = []
            for i in range(len(colnames)):
                res_list.append(result[i])
            all_tuples.append(res_list)
        results['entries'] = all_tuples
        return results

