from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix= "/posts", 
    tags = ['Posts']
    # +/id /posts/{id}
    )

@router.get("/", response_model= List[schemas.PostOut])
def get_posts (db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), 
limit: int = 10, skip: int = 0, search: Optional[str] = ""): #ha definido un query parameter llamado limit con un valor por defecto
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #aqui usa el query parameter
    # con el %20 añadimos un espacio en la url para buscar un string que contenga espacio
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter =True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # def get_posts():
    # cursor.execute ("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print (posts)
    return posts
@router.post("/",status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
# def cretate_posts(payload: dict = Body(...)):
#   print(payload)
#   return {"new post": f"{payload['title']}:{payload['content']}"}
def cretate_posts(post: schemas.PostCreate,db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)): #este post viene cargado en el body
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() #si no haemos esto los cambios anteriores no se guardarán en postgres. De stage hay que pasar a commit
    # print(new_post)
    # new_post = models.Post(title = post.title, content= post.content, published = post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
#@app.get("/posts/{id}")
#def get_post(id: int, response: Response): #validamos que sea un integer
#    post = find_post(int(id)) #lo toma como un string el parámetro pasado por url, así que habrá que convertirlo a integuer para que funcione
 #   if not post:
#        response.status_code = status.HTTP_404_NOT_FOUND
#        return {"message": f"post with id: {id} is not found"}
#    return{"post_detail": post}

@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #validamos que sea un integer
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id== id).first()

    post  = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter =True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, 
                           detail = f"post with id: {str(id)} is not found")
    #print (post)
    return post


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s  RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id== id)
    post =post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                           detail = f"post with id: {str(id)} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)
#    index = find_index_post(id)
#    my_posts.pop(index)
#    return Response(stauts_code= status.HTTP_204_NO_CONTENT)
@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #                 (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id== id) #está accediendo a los elementos en la BBDD,es la query
    post = post_query.first() #toma el valor de la BBDD y lo guarda en una variable
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                           detail = f"post with id: {str(id)} does not exist")
    post_query.update(updated_post.dict(),synchronize_session = False) #actualiza el elemento de la BBDD en cuestión
   
    db.commit()
   
    return post_query.first()