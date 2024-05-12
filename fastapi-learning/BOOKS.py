from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Books_list = [
    {
        "title": 'titleone', "author": 'author1', 'category': 'science'
    },
    {
        "title": 'titletwo', "author": 'author2', 'category': 'maths'
    },
    {
        "title": 'titlethree', "author": 'author3', 'category': 'maths'
    },
]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/getbooks')
async def get_books():
    return Books_list

@app.get('/getbooks/{author}')
async def getbooks(author: str):
    for book in Books_list:
        print((book))
        if(book.get('author') == author):
            print(type(book))
            return [book]
        

@app.get('/getbooks/')
async def getbooks(category: str):
    booklist =[]
    for book in Books_list:
        print(type(book))
        if(book.get('category') == category):
            print(book)
            booklist.append(book)
    return booklist

@app.post('/getbooks/create_book')
async def createbooks(newbook=Body()):
    Books_list.append(newbook)
    return(Books_list)

@app.delete('/delete_book/{author}')
async def delete_book(author:str):
    for i in range(len(Books_list)):
        if(Books_list[i].get('author') == author):
            print(author)
            Books_list.pop(i)

            return(Books_list)
    
@app.put('/updatebook/')
async def updatebook(updatebook=Body()):
    for i in range(len(Books_list)):
        if(Books_list[i].get('author') == updatebook.get('author')):
            Books_list[i] = updatebook


            return(Books_list)