from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import database, models, oauth2, schemas


router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(user_vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends
    (oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == user_vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {user_vote.post_id} "
                                                                          "does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == user_vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if user_vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} "
                                                                             f"has already voted on post {user_vote.post_id}")
        new_vote = models.Vote(post_id=user_vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}