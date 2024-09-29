import pytest 
import requests

#CRUD
BASE_URL = 'http://127.0.0.1:5000'
tasks = []

#TESTE DE POST
def test_create_task():
    new_task_data = {
      "title": "Nova Tarefa",
      "description": "Nova Tarefa Criada com sucesso!"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json  # Corrigido o nível de indentação
    tasks.append(response_json['id'])
  
 #TESTE DE GET GERAL 
def test_get_testes():
    response = requests.get(f"{BASE_URL}/tasks")
    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json
    
 #TESTE DE GET ESPECIFICO    
def test_get_task():
  if tasks:
    task_id = tasks[0]
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert task_id == response_json['id']
  
# TESTE DE UPDATE ESPECIFICO
def test_update_task():
  
  assert tasks, "A lista de tarefas está vazia, o teste não pode continuar."
  
  if tasks:
    task_id = tasks[0]
    payload = {
      "completed": True,
      "description": "nova descricao",
      "title": "Titulo atualizado"
    }
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    assert response.status_code == 200,  f"Falha ao atualizar a tarefa {task_id}. Status code: {response.status_code}"
    response_json = response.json()
    assert "message" in response_json, "Campo 'message' ausente na resposta."
  
    # Nova requisição a tarefa especifica
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200, f"Falha ao buscar a tarefa {task_id}. Status code: {response.status_code}"
    response_json = response.json()
    assert response_json["title"] == payload["title"], "O título não foi atualizado corretamente."
    assert response_json["description"] == payload["description"], "A descrição não foi atualizada corretamente."
    assert response_json["completed"] == payload["completed"], "O status 'completed' não foi atualizado corretamente."
    
    
def test_delete_task():
  
  assert tasks, "A lista de tarefas está vazia, o teste não pode continuar."
  
  if tasks: 
     task_id = tasks[0]  
     response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
     assert response.status_code == 200, f"Falha ao deletar a tarefa {task_id}. Status code: {response.status_code}"
     
     response = requests.get(f"{BASE_URL}/tasks/{tasks}")
     assert response.status_code == 404, f"Tarefa {task_id} ainda existe após deletar. Status code: {response.status_code}"
     
     tasks.remove(task_id)