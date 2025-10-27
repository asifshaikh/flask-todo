import click
import requests

BASE_URL = "http://127.0.0.1:5000"


@click.group()
def cli():
    """TaskFlow CLI - Manage tasks via API."""
    pass


@cli.command(name="get_tasks")
@click.option('--completed', type=str, default=None, help='Filter tasks by completion status')
def get_tasks(completed):
    """Fetch all tasks (optionally filter by completion status)."""
    url = f"{BASE_URL}/tasks"
    if completed:
        url += f"?completed={completed}"
    response = requests.get(url)
    if response.status_code == 200:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.text}")


@cli.command(name="create_task")
@click.option('--title', type=str, required=True, help='Task title')
@click.option('--description', type=str, required=True, help='Task description')
def create_task(title, description):
    """Create a new task."""
    url = f"{BASE_URL}/tasks"
    data = {'title': title, 'description': description}
    response = requests.post(url, json=data)
    if response.status_code == 201:
        click.echo('✅ Task created successfully!')
    else:
        click.echo(f"Error: {response.text}")


@cli.command(name="delete_task")
@click.option('--task_id', type=int, required=True, help='Task ID to delete')
def delete_task(task_id):
    """Delete a task by ID."""
    url = f"{BASE_URL}/tasks/{task_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        click.echo('🗑️ Task deleted successfully!')
    else:
        click.echo(f"Error: {response.text}")


@cli.command(name="update_task")
@click.option('--task_id', type=int, required=True, help='Task ID to update')
@click.option('--title', type=str, required=False, help='New task title')
@click.option('--description', type=str, required=False, help='New task description')
@click.option('--completed', type=bool, required=False, help='Task completion status')
def update_task(task_id, title, description, completed):
    """Update a task by ID."""
    url = f"{BASE_URL}/tasks/{task_id}"
    data = {k: v for k, v in {
        'title': title,
        'description': description,
        'completed': completed
    }.items() if v is not None}
    response = requests.put(url, json=data)
    if response.status_code == 200:
        click.echo('✏️ Task updated successfully!')
    else:
        click.echo(f"Error: {response.text}")


if __name__ == '__main__':
    cli()
