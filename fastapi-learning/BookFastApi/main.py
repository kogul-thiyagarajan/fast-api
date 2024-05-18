from typing import Annotated, Optional
from fastapi import FastAPI, Depends, HTTPException
import models
from models import Books
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class Bookrequest(BaseModel):
    id: Optional[int]=None
    title: str = Field(min_length=3)
    author: str = Field(min_lenght=3)
    description: str
    rating: int = Field(gt=0, lt=6)

class Updatebook(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_lenght=3)
    description: str
    rating: int = Field(gt=0, lt=6)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/')
async def return_all_books(db:db_dependency):
    """
    This method returns all the book entries available onto the database
    """
    return db.query(Books).all()

@app.get('/fetchbook/{bookid}', status_code= status.HTTP_200_OK)
async def fetch_book(db: db_dependency, bookid: int):
    
    """
    This method returns the book details based on the book id

    input:
        - Bookid as the input parameter to return the specific book

    output:
        - Returns the book information mapped to the specific book id
    """
    fetch_book_id = db.query(Books).filter(Books.id == bookid).first()
    if fetch_book is not None:
        return fetch_book_id
    raise HTTPException(status_code= 404, detail ="BOOK NOT FOUND")


@app.post('/', status_code = status.HTTP_201_CREATED)
async def create_books(db: db_dependency, bookrequest:Bookrequest):

    """
    This method allows to create a new details about the book into database

    Input:
        - Book details should be sent in a key value pair in the below format
              {
                "id": 1,
                "rating": 3,
                "author": "J.K. Rowling",
                "title": "Harry Potter",
                "description": "Harry Potter Series"
            }

    Output:
        - New book is added into DB
    """
    

    book_list = Books(**bookrequest.model_dump())
    db.add(book_list)
    db.commit()

@app.put('/update_book/{bookid}', status_code = status.HTTP_201_CREATED)
async def update_book(db: db_dependency, bookid:int, updaterequest:Updatebook):

    """
    This method updates/modify the book information based on the bookid

    Input:
        - Book id to be amended as the input parameter.
        - Along with the input book id, provide the details to be amended in a key value pair

    Output:
        - Details will be modified and commited into DB
    """


    book_id = db.query(Books).filter(Books.id == bookid).first()
    if book_id is not None:
        book_id.title = updaterequest.title
        book_id.author = updaterequest.author
        book_id.description = updaterequest.description
        book_id.rating = updaterequest.rating


    db.add(book_id)
    db.commit()

@app.delete('/delete_book/{bookid}', status_code= status.HTTP_200_OK)
async def delete_book(db: db_dependency, bookid: int):

    """
    This method deletes the details about the specfici book in Database based on the bookid.

    Input: Book id as the input parameter for this method.

    Output: Deletes the book or Raise an exception if book is not found in DB.

    """

    book_delete = db.query(Books).filter(Books.id == bookid).first()
    if book_delete is not None:
        db.query(Books).filter(Books.id == bookid).delete()
    else:
        raise HTTPException(status_code=404, detail= 'Book Not Found')
    
    db.commit()