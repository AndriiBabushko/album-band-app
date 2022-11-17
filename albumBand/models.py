from flask_login import UserMixin
from albumBand import login_manager
import random


@login_manager.user_loader
def load_user(user_id):
    return User.id


class User(UserMixin):
    id = random.getrandbits(64)
    username: str
    email: str
    image_file: str
    password: str
    posts: None
    is_authenticated: bool = False


class Posts:
    def __init__(self, author: str, date_posted: str, title: str, album_date: str):
        self.author: str = author
        self.date_posted: str = date_posted
        self.title: str = title
        self.album_date: str = album_date
        self.post_id: int = random.getrandbits(64)
