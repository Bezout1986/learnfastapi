from fastapi import Depends, FastAPI, HTTPException,status

blogs={
"1":"hello",
"2":"darkness",
"3":"my",
"4":"old",
"5":"friend",
"6":"i",
"7":"have",
"8":"come",
"9":"to",
"10":"talk",
"11":"to",
"12":"you",
"13":"again"
}

users={
"a":"john",
"b":"paul",
"c":"george",
"d":"ringo",
"e":"simon",
"f":"garfunkel"
}

app = FastAPI(title="injecting a dependency")

def get_object_by_id_from_relevanuserst_dict_or_error(indict: dict ,id:str):
  obj=indict.get(id)
  if not obj:
    raise HTTPException(detail= f"obj with the id {id} does not exist in dictionary {indict}", status_code=status.HTTP_404_NOT_FOUND)
  return obj



def get_blog_by_id_or_error(id:str):
  blog = get_object_by_id_from_relevanuserst_dict_or_error(blogs, id)
  if not blog:
    raise HTTPException(detail= f"blog with the id {id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
  return blog


def get_user_by_id_or_error(id:str):
  user= get_object_by_id_from_relevanuserst_dict_or_error(users, id)
  if not user:
    raise HTTPException(detail= f"user with the id {id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
  return user

@app.get("/blog/{id}")
def get_blog(blogname:str = Depends(get_blog_by_id_or_error)):
    return blogname


@app.get("/user/{id}")
def get_blog(username:str = Depends(get_user_by_id_or_error)):
    return username