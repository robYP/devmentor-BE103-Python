from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import repository.post
from infrastructure.mysql import get_db
from schema.database.post import PostCreate

router = APIRouter(
    tags=["events"],
    prefix="/events"
)