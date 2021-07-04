from app import db


class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()


class ShortUrl(BaseModel):
    __tablename__ = 'short_url'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_url = db.Column(db.String(256), nullable=False)
    shorted_key = db.Column(db.String(256), nullable=False, unique=True)
    expires_at = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            'original_url': self.original_url,
            'shorted_key': self.shorted_key,
            'expires_at': self.expires_at,
        }

short_url_shorted_key_idx = db.Index('ShortUrl_shorted_key_idx', ShortUrl.shorted_key)
