from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="API de tareas")

class Tarea(BaseModel):
    titulo: str
    hecha: bool = False

tareas = {}
siguiente_id = 1

@app.get("/tareas")
def listar():
    return tareas

@app.get("/tareas/{id}")
def obtener(id: int):
    if id not in tareas:
        raise HTTPException(status_code=404, detail="No existe")
    return tareas[id]

@app.post("/tareas")
def crear(tarea: Tarea):
    global siguiente_id
    tareas[siguiente_id] = tarea
    siguiente_id += 1
    return {"id": siguiente_id - 1, "tarea": tarea}

@app.delete("/tareas/{id}")
def borrar(id: int):
    if id not in tareas:
        raise HTTPException(status_code=404, detail="No existe")
    del tareas[id]
    return {"borrada": id}

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def web():
    return open("index.html", encoding="utf-8").read()