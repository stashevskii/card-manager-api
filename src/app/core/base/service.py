class Service:
    def __init__(self, repository):
        self.repository = repository

    def admin_get_all(self):
        return self.repository.get_all()
