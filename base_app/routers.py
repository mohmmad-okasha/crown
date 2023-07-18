class Log_db_Router:
    books_db = "logs_db"
    default_db = "default"

    def db_for_read(self, model, **hints):
        model_name = model._meta.model_name
        if model_name == 'logs':
            return self.books_db
        else:
            return None

    def db_for_write(self, model, **hints):
        model_name = model._meta.model_name
        if model_name == 'logs':
            return 'logs_db'
        else:
            return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == 'logs':
            return db == 'logs_db'
        else:
            return db == 'default'
