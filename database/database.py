import os

import clickhouse_connect 


class Client:

    def __init__(self):
        self.client = clickhouse_connect.get_client(host='localhost', port=18123, username='default')

    def test(self):
        result = self.client.query("SELECT 'HELLO WORLD'")
        print(result.result_rows)

