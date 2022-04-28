from typing import List, Optional
from fastapi import Response
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from my_api.my_app import oauth2, models, schemas
from my_api.my_app.database import get_db


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("/all", response_model=List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                  limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                        models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).\
                        filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    return posts
    # return {"data": my_posts}  # fastApi serialized my_posts dict to JSON


@router.get("/user", response_model=List[schemas.PostOut])
def get_user_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                   limit=10):

    # user_posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).limit(limit).all()

    user_posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
             models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id). \
             filter(models.Post.user_id == current_user.id).limit(limit).all()

    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    return user_posts
    # return {"data": my_posts}  # fastApi serialized my_posts dict to JSON


@router.get("/{id}", response_model=schemas.PostOut)  # id path parameter
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):  # id take path parameter

    # SQLALCHEMY
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
             models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).\
             filter(models.Post.id == id).first()

    # PSYCOPG2
    # cursor.execute("""SELECT * FROM posts WHERE id= %s""", str(id))
    # post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} doesnt exist")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # SQLALCHEMY
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(current_user.email)
    new_post = models.Post(user_id=current_user.id, **post.dict())  # adding new post to db
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retrieve new post

    # PSYCOPG2
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # SQLALCHEMY
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # PSYCOPG2
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",  str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.UpdatePost, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # SQLALCHEMY
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # PSYCOPG2
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    post_query.update(updated_post.dict(), synchronize_session=False)  # pass the fields that we wanna update as a dict
    db.commit()

    return post_query.first()
