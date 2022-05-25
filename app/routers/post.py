from .. import models, schema, utils, oauth2
from fastapi import FastAPI , Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db, engine
from typing import List, Optional

router= APIRouter(
    prefix="/posts",
    tags=['Posts'],
)



@router.get("/", response_model=List[schema.PostOut])
def get_all_posts(db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return  posts

@router.get("/my", response_model=List[schema.Post])
def get_posts_by_login_user(db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return  post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_new_post(post:schema.PostCreate, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schema.PostOut)
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id of {id} not found")
#    if post.owner_id != current_user.id:
#        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized to perform operation")   
    return post

@router.put("/{id}", response_model=schema.Post)
def update_post_by_id(id: int, updated_post:schema.PostCreate, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Posts with ID #{id} was not found.")
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized to perform operation")    
    post_query.update(updated_post.dict() , synchronize_session=False)
    db.commit()
    return post_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Posts with ID #{id} was not found.")
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized to perform operation")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

