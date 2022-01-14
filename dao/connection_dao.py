import psycopg2


class ConnectionDao:
    conn = None

    def connection_postgre(self):
        try:
            self.conn = psycopg2.connect(host="python-training.cvjyerl6whev.us-west-2.rds.amazonaws.com",
                                         database="WebUserManagement",
                                         user="postgres", password="00000000")
        except Exception as e:
            print(e)

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
