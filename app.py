from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route("/")
def home():
    return "<h1>Bem-vindo ao Gerenciador de Tarefas</h1>"

@app.route("/about")
def about():
    return "<h3>Esta é a página sobre.</h3>"

@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control,title=data.get("title"), description=data.get("description", ""))
    task_id_control += 1
    tasks.append(new_task)
    return jsonify({"message": "Nova tarefa criada com sucesso!", "id": new_task.id}), 201

@app.route("/tasks", methods=["GET"])
def get_tasks():
    task_list = [task.to_dict() for task in tasks ]
    output = {
        "tasks": task_list,
        "total_tasks": len(tasks),
    }
    return jsonify(output)

@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
        
    return jsonify({"message": "Tarefa não encontrada"}), 404

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if task == None:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    task.title = data['title']
    task.description = data['description']
    task.completed = data.get('completed', task.completed)


    return jsonify({"message": "Tarefa atualizada com sucesso!"})

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    global tasks
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404
    
    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso!"})


if __name__ == "__main__":
    app.run(debug=True)