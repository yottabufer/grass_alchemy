import pytest
from httpx import AsyncClient

data_for_test = {
    'id': int,
    'title': 'test title',
    'completed': bool,
    'created_at': str,
    'updated_at': str
}

available_body = {
    'title': 'test title',
    'completed': False,
}


@pytest.mark.anyio
async def test_create(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/tasks/create", json=available_body)
    body = response.json()
    assert response.status_code == 201
    data_for_test['id'] = body.get('id')
    data_for_test['title'] = body.get('title')
    data_for_test['completed'] = body.get('completed')
    data_for_test['created_at'] = body.get('created_at')
    data_for_test['updated_at'] = body.get('updated_at')
    assert body.get('title') == data_for_test['title']


@pytest.mark.anyio
async def test_get_all_tasks(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/tasks/get")
    body = response.json()
    assert response.status_code == 200
    assert isinstance(body[0].get('title'), str) is True
    assert body[0].get('title') == data_for_test['title']


@pytest.mark.anyio
async def test_get_one_task(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/tasks/get/1")
    body = response.json()
    assert response.status_code == 200
    assert isinstance(body.get('title'), str) is True
    assert body.get('title') == data_for_test['title']
    assert body.get('completed') is False


body_non_title = {
    'title': None,
    'completed': False,
}


@pytest.mark.anyio
async def test_create_non_title_task(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/tasks/create", json=body_non_title)
    assert response.status_code == 400
    assert response.json()['detail'] == 'The title cannot be empty'


body_string_completed_type = {
    'title': 'String type',
    'completed': 'true',
}


@pytest.mark.anyio
async def test_create_string_completed_type(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/tasks/create", json=body_string_completed_type)
    assert response.status_code == 400
    assert response.json()['detail'] == 'Completed must be a boolean'
