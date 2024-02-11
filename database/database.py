import clickhouse_connect

class Client:

    def __init__(self):
        self.client = clickhouse_connect.get_client(host='clickhouse-server', port=8123, username="default"
        )

    def test(self):
        result = self.client.query("SELECT 'HELLO WORLD'")
        print(result.result_rows)

    def init_db(self):
        self.client.command(
            cmd="create table if not exists default.taxbot_users(id String DEFAULT generateUUIDv4(), chat_id UInt32, username String, firstname String, logged Datetime) Engine = MergeTree() PRIMARY KEY (id);"
        )
        print('DB Created')

    def add_new_user(self, **kwargs):
        username = kwargs.get('username', None)
        chat_id = kwargs.get('chat_id')
        logged = kwargs.get('logged')
        firstname = kwargs.get('firstname')

        
        result = self.client.query(
            "SELECT chat_id FROM default.taxbot_users WHERE chat_id = %(chat_id)s",
            parameters={"chat_id": chat_id},
        )
        print(type(kwargs["chat_id"]), kwargs["chat_id"])
        if len(result.result_set) == 0:
            self.client.command(
                "INSERT INTO default.taxbot_users(chat_id, username, firstname, logged) VALUES (%(chat_id)s, %(username)s, %(firstname)s, %(logged)s)",
                parameters={"chat_id": chat_id, "username": username, 'firstname':firstname, 'logged':logged},
            )
        else:
            print("User already exists")
        return result.result_set
