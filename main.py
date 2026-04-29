from fastapi import FastAPI, status,HTTPException, Query
from pydantic import BaseModel
import os
import json

app = FastAPI()
TASK_FILE ="tasks.json"

# Each task will look like: {"id": 1, "task": "Buy milk", "done": False}
class TaskBody(BaseModel):
    task: str

class TaskResponse(BaseModel):
    id: int
    task: str
    done:bool

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return[]
    with open(TASK_FILE, "r") as file:
        return json.load(file)
    
def save_task(tasks):
    with open (TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

@app.get("/tasks")
async def tasks():
    return load_tasks()


@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def add_task(body: TaskBody):
    tasks = load_tasks()
    if len(tasks)==0:
        new_id =1
    else:
        new_id = max([t["id"] for t in tasks], default=0) +1
    tasks.append({"id": new_id,"task":body.task ,"done":False})
    save_task(tasks)
    return tasks
    #print(f"Task {args.task} added with ID of {new_id} the due date {args.date}")

@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    tasks= load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_task(tasks)
            return task
    raise HTTPException(status_code = 400 , detail= "Task not found")#


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks= load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            del tasks[task]
            save_task(tasks)
            return task
        
@app.get("/tasks/search")
def search_task(keyword: str= Query(..., min_length = 1)):
    tasks= load_tasks()
    for task in tasks:
        if keyword.lower() in task["task"].lower():
            return task
        else:
            raise HTTPException(status_code= 404, detail = "No task found")
        
@app.get("/tasks/stats")
def task_stats():
    tasks = load_tasks()
    total = len(tasks)
    completed = sum(1 for t in tasks if t["done"])
    pending = total - completed
    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }

# @app.get("/")
# async def hello_world():
#     return{"massage": "Hello World", "status": "ok"}



# @app.get("/greet/{name}")
# async def greet(name: str):
#     return {"message": f"Hello, {name}!"}

# @app.get("/items/{item_id}")
# async def get_item(item_id: int):
#     return {"item_id": item_id}

# from pydantic import BaseModel

# class Recipe(BaseModel):
#     recipe: str
#     done: bool = False

#post request
# @app.post("/recipe")
# async def create_recipe(recipe: Recipe):
#     return {"recipe": recipe.recipe, "done": recipe.done}




#Rasing an error
# from fastapi import FastAPI, HTTPException
# ...
# @app.get("/recipes/{recipe_id}")
# async def get_recipe(recipe_id: int):
#     recipes = load_recipes()
#     for recipe in recipes:
#         if recipe["id"] == recipe_id:
#             return recipe
#     raise HTTPException(status_code=404, detail="Recipe not found")