import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db as _db
from models import Task


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield _db


def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'todo-app'


def test_get_empty_tasks(client):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_task(client):
    task_data = {
        'title': 'Test Task',
        'priority': 'high',
        'description': 'Test description'
    }
    response = client.post('/api/tasks', json=task_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Task'
    assert data['priority'] == 'high'
    assert 'id' in data


def test_create_task_without_title(client):
    response = client.post('/api/tasks', json={'priority': 'high'})
    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_get_task_by_id(client):
    task_data = {'title': 'Task for ID test'}
    create_response = client.post('/api/tasks', json=task_data)
    task_id = create_response.get_json()['id']

    response = client.get(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Task for ID test'


def test_get_nonexistent_task(client):
    response = client.get('/api/tasks/99999')
    assert response.status_code == 404


def test_update_task(client):
    task_data = {'title': 'Before Update'}
    create_response = client.post('/api/tasks', json=task_data)
    task_id = create_response.get_json()['id']

    update_data = {'title': 'After Update', 'status': 'completed'}
    response = client.put(f'/api/tasks/{task_id}', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'After Update'
    assert data['status'] == 'completed'


def test_delete_task(client):
    task_data = {'title': 'Task to Delete'}
    create_response = client.post('/api/tasks', json=task_data)
    task_id = create_response.get_json()['id']

    response = client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Task deleted successfully'

    get_response = client.get(f'/api/tasks/{task_id}')
    assert get_response.status_code == 404


def test_update_task_status(client):
    task_data = {'title': 'Status Test'}
    create_response = client.post('/api/tasks', json=task_data)
    task_id = create_response.get_json()['id']

    update_data = {'status': 'completed'}
    response = client.put(f'/api/tasks/{task_id}', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'completed'


def test_create_task_with_due_date(client):
    task_data = {
        'title': 'Task with due date',
        'due_date': '2026-12-31T23:59:59Z'
    }
    response = client.post('/api/tasks', json=task_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['due_date'] is not None


def test_get_all_tasks_after_create(client):
    client.post('/api/tasks', json={'title': 'Task 1'})
    client.post('/api/tasks', json={'title': 'Task 2'})

    response = client.get('/api/tasks')
    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) >= 2