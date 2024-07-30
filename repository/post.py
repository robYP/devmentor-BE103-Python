from sqlalchemy.orm import Session

from database.post import Post
from schema.database.post import PostCreate


def lists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()


def create(db: Session, post: PostCreate):
    db_user = Post(title=post.title, content=post.content)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def delete_post_by_id(db: Session, post_id: int):
    db_post = db.query(Post).filter(Post.id==post_id).first()
    if not db_post:
        return None
    db.delete(db_post)
    db.commit()
    return db_post


def update_post_by_id(db: Session, post_id: int, post: PostCreate):
    db_post = db.query(Post).filter(Post.id==post_id).first()
    if not db_post:
        return None
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post