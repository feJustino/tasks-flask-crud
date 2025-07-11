import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"
tasks = []

def test_create_task():
    new_task_data = {
        "title": "nova tarefa",
        "description": "Descrição"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 201
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json

def test_get_tasks():
    new_task_data = {
        "title": "nova tarefa2",
        "description": "Descrição2"
    }
    requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 2

def test_get_task():
    response = requests.get(f"{BASE_URL}/tasks/1")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['title'] == "nova tarefa"

def test_update_task():
    new_task_data = {
        "title": "Nome Alterado",
        "description": "Descrição2"
    }
    put_response = requests.put(f"{BASE_URL}/tasks/1", json=new_task_data)
    assert put_response.status_code == 200
    get_response = requests.get(f"{BASE_URL}/tasks/1")
    response_json = get_response.json()
    assert response_json['title'] == "Nome Alterado"

def test_delete_task():
    delete_response = requests.delete(f"{BASE_URL}/tasks/2")
    assert delete_response.status_code == 200
    get_response = requests.get(f"{BASE_URL}/tasks")
    response_json = get_response.json()
    assert response_json["total_tasks"] == 1