from db import db


class OdooURLModel(db.Model):
    __tablename__ = 'odooURLs'
    id              = db.Column(db.Integer, primary_key=True)
    url             = db.Column(db.String(80))
    username        = db.Column(db.String(80))
    password        = db.Column(db.String(80))

    connected_at_least_once \
                    = db.Column(db.Boolean)
    endpoint        = db.Column(db.String(30))

    def __init__(self, url, username, password):
        self.url  = url
        self.username = username
        self.password = password

        self.connected_at_least_once = False
        self.endpoint = None

    def json(self):
        return {    'url': self.url,
                    'username': self.username,
                    'connected_at_least_once': self.connected_at_least_once}

    @classmethod
    def find_by_url(cls, url):
        return cls.query.filter_by(url=url).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
