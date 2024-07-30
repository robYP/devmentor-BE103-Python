from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import repository.post
from infrastructure.mysql import get_db
from schema.database.post import PostCreate

router = APIRouter(
    tags=["post"],
    prefix="/posts"
)


@router.get("/")
def list_post(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = repository.post.lists(db, skip=skip, limit=limit)
    return posts

@router.get("/{post_id}")
def get_post(post_id:int, db: Session= Depends(get_db)):
    post = repository.post.get_post_by_id(db, post_id=post_id)
    return post
    

@router.post("/")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    return repository.post.create(db=db, post=post)

@router.delete("/{post_id}")
def delete_post(post_id:int, db: Session= Depends(get_db)):
    post = repository.post.delete_post_by_id(db=db, post_id=post_id)
    if post == None:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return post

@router.put("/{post_id}")
def update_post(post: PostCreate, post_id:int, db: Session = Depends(get_db)):
    post = repository.post.update_post_by_id(db=db, post_id=post_id, post=post)
    if post == None:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return post