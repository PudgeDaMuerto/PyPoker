import shelve


class Save:
    def __init__(self):
        self.file = shelve.open('data/data')

    def save_data(self, players: list, players_queue):
        self.file['Players'] = players
        self.file['Players queue'] = players_queue

    def get_data(self):
        try:
            return self.file['Players'], self.file['Players queue']
        except KeyError:
            return False

    def delete_data(self):
        self.file.clear()

    def __del__(self):
        self.file.close()
