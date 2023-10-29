from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing_extensions import Literal
from typing import List

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root() -> str:
    # ваш код здесь
    # {"message": 'Вы подключены к БД клиники'}
    return 'Вы подключены к БД клиники'


# ваш код здесь

@app.post('/post')
def get_post() -> Timestamp:
    post_db.append(Timestamp(id=post_db[-1].id + 1, timestamp=post_db[-1].timestamp + 1))
    return post_db[-1]


@app.get('/dog')
def get_dog(kind: Literal['terrier', 'bulldog', 'dalmatian']) -> List[Dog]:
    list_of_selected = []
    for i in dogs_db:
        if dogs_db[i].kind == kind:
            list_of_selected.append(dogs_db[i])
    return list_of_selected


@app.post('/dog')
def create_dog(dog: Dog) -> Dog:
    # pk = max(dogs_db.keys())
    try:
        dogs_db[dog.pk] = dog  # Dog(name='NewDog', pk=pk, kind='terrier')
        return dogs_db[dog.pk]
    except:
        raise HTTPException(status_code=422)


@app.get('/dog/{pk}')
def get_dog_by_pk(pk: int) -> Dog:
    if pk in list(dogs_db.keys()):
        return dogs_db[pk]
    else:
        raise HTTPException(status_code=422, detail='Dog not found')


@app.patch('/dog/{pk}')
def update_dog(pk: int, dog: Dog) -> Dog:
    dogs_db[pk] = dog
    return dogs_db[pk]
