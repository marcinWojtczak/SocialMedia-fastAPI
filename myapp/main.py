from fastapi import FastAPI
from myapp import models
from myapp.database import engine
from routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# SQLAlchemy should check whether a table already exists before trying to create it
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello Fast API"}



