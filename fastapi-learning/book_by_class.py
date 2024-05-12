from fastapi import Body, FastAPI,Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int


    def __init__(self,id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        
class Bookrequest(BaseModel):
    id: Optional[int]=None
    title: str = Field(min_length=3)
    author: str = Field(min_lenght=3)
    description: str
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(eq=4)


BOOKS = [
        Book(1,"Harry Potter-1","J-K-Rowling","Harry Potter Book One", 5,2012),
        Book(2,"Harry Potter-2","J-K-Rowling","Harry Potter Book Two", 5,2013)
]

@app.get('/getbooks')
async def get_all_books():
    return BOOKS

@app.get('/getbook_by_rating/{rating}')
async def get_book_by_rating(rating:int):
    booklist = []
    for book in BOOKS:
        print((book.rating))
        if(book.rating == rating):
            booklist.append(book)
    return booklist

@app.get('/getbook/publishedyear/')
async def getbook_by_publishedyear(year:int):
    booklist = []
    for book in Book:
        print((book.published_date))
        if(book.published_date == year):
            booklist.append(book)
    return booklist

@app.post('/create_new_book/post')
async def create_newbook(new_book: Bookrequest):
    add_book = Book(**new_book.dict())
    print(add_book.id)
    print(add_book.author )
    BOOKS.append((add_book))
    print(add_book)
    return(BOOKS)
    
@app.put('/update_book/by_id/put/')
async def update_book( updatebook: Bookrequest):
    for i in range(len(BOOKS)):
        if (BOOKS[i].id == updatebook.id):
            BOOKS[i] = Book(**updatebook.dict())
    return(BOOKS)

def fetch_book_id(book: Bookrequest):
    print(BOOKS[-1].id)
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id+ 1
    print(id)

@app.delete('/delete_by_id/{id}')
async def delete_by_id(id: int):
    for i in range(len(BOOKS)):
        if(BOOKS[i].id==id):
            print("i")
            BOOKS.pop(i)
            break;
    return(BOOKS)