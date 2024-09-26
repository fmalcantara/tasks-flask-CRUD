from flask import Flask, request, jsonify
from models.task import Task
from uuid import uuid4

app = Flask(__name__)

tasks = []


# CRIAR UMA ATIVIDADE
@app.route('/tasks', methods=['POST'])
def create_task():
  data = request.get_json()
  new_task = Task(id = uuid4(), title=data.get('title'), description=data.get('description'))
  tasks.append(new_task)
  print(tasks)
  return jsonify({"message": "Nova Tarefa Criada com sucesso!"})

# LER ATIVIDADES CRIADAS
@app.route('/tasks', methods=['GET'])
def get_tasks():
  task_list = [task.to_dict() for task in tasks]
  
  output = {  
      "tasks": task_list,
      "total_tasks":  len(task_list)
    }
  return jsonify(output)

# LER UMA ATIVIDADE CRIADA EM ESPECÍFICO POR ID
@app.route('/tasks/<uuid:id>', methods=['GET'])
def get_task(id):
  for t in tasks:
    if t.id == id:
      return jsonify(t.to_dict())
  
  return jsonify({"message": "Nao e possivel encontrar a atividade"}), 404 

# EDITAR UMA ATIVIDADE
@app.route('/tasks/<uuid:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
      if t.id == id:
       task = t
       break

    if task == None:
      return jsonify({"message": "Nao foi possivel encontrar sua tarefa"}), 404
    
    data = request.get_json()
    task.title=data['title']
    task.description=data['description']
    task.completed=data['completed']

    return jsonify({"message":"Tarefa atualizada com sucesso"})

#DELETAR UMA ATIVIDADE
@app.route('/tasks/<uuid:id>', methods=['DELETE'])
def delete_task(id):
  task = None
  for t in tasks:
      if t.id == id:
        task = t
        break
      
  if task == None:
    return jsonify({"message":"Não foi possivel encontrar a atividade"})

  tasks.remove(task)
  return jsonify({"message": "Trefa Deletada com sucesso"})

if __name__ == '__main__':
  app.run(debug=True)
  
  