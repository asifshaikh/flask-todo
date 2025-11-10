import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/tasks', methods=['GET'])
def get_tasks():
    completed = request.args.get('completed')
    if completed:
        conn = get_db_connection()
        tasks = conn.execute('SELECT * FROM tasks WHERE completed = ?', (completed == '1',)).fetchall()
        conn.close()
        tasks_list = []
        for task in tasks:
            tasks_list.append({
                'id':task['id'],
                'title':task['title'],
                'description':task['description'],
                'completed': bool(task['completed']),
                'created':task['created']
            })
        return jsonify(tasks_list)
    # If no completed query parameter is provided, return all tasks
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            'id':task['id'],
            'title':task['title'],
            'description':task['description'],
            'completed': bool(task['completed']),
            'created':task['created']
        })
    return jsonify(tasks_list)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    task_data = {
        'id':task['id'],
        'title':task['title'],
        'description':task['description'],
        'completed': bool(task['completed']),
        'created':task['created']
    }
    return jsonify(task_data)

@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = request.get_json()
    title = new_task.get('title')
    description = new_task.get('description', '')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, description, completed) VALUES (?,?,0)', (title, description))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': task_id, 'title': title, 'description': description, 'completed': 0}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    updated_task = request.get_json()
    title = updated_task.get('title')
    description = updated_task.get('description')
    completed = updated_task.get('completed')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?',
                   (title, description, int(completed), task_id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'id': task_id, 'title': title, 'description': description, 'completed': completed})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task deleted successfully'})


if __name__ == '__main__':
    app.run(port=5000,host='0.0.0.0',debug=True)