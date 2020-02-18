import redis


class ShelfRedis:
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.db = kwargs['db']
        self.password = kwargs['password']
        self.r = redis.Redis(host=self.host, port=self.port, db=self.db, password=self.password)
        self.filepath = kwargs['file_path']
        self.set_name = kwargs['set_name']

    def add_value(self):
        try:
            with open(self.filepath, 'r') as fp:
                lines = fp.readlines()
                for line in lines:
                    value = line.strip()
                    self.r.sadd(self.set_name, value)  # sadd(name, values)
        except FileNotFoundError as err:
            raise err

    def __repr__(self):
        return "%s" % (type(self).__name__,)


def main():
    connect = {
        "host": '45.34.33.156',
        "port": 12112,
        "db": 9,
        "password": "513f21fbc55d446186c7f1daa9dae626",
        'file_path': r'D:\work\code\workcode\ebay_spider\总类目2.txt',
        'set_name': "test",
    }
    redis_test = ShelfRedis(**connect)
    redis_test.add_value()
    print(redis_test.r.smembers(redis_test.set_name))
    print(redis_test.__repr__())


if __name__ == '__main__':
    main()
