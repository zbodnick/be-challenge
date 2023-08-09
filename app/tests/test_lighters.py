import pytest
from flask import Flask
from app import create_app, db
from app.models import Lighter
from app.lighters import bp
    
def test_get_all_lighters(client):
    response = client.get('/lighters/')
    data = response.get_json()
    assert response.status_code == 200
    assert isinstance(data, list)

def test_create_lighter_valid(client):
    payload = {'name': 'New Lighter', 'value': 15.0, 'description': 'New Description', 'image_uri': 'https://www.image.com/img.png', 'manufacturer_id': 1}
    response = client.post('/lighters/', json=payload)
    data = response.get_json()

    assert response.status_code == 201
    assert data['name'] == 'New Lighter'
    assert data['value'] == 15.0
    assert data['description'] == 'New Description'
    assert data['image_uri'] == 'https://www.image.com/img.png'
    assert isinstance(data, dict)

def test_create_lighter_invalid_no_name(client): # Missing name param
    payload = {'value': 15.0, 'description': 'New Description', 'image_uri': 'https://www.image.com/img.png', 'manufacturer_id': 1}
    response = client.post('/lighters/', json=payload)

    assert response.status_code == 400

def test_get_lighter_by_id_valid(client):
    test_lighter = Lighter(name='Test Lighter', value=10.0, description='Test Description', image_uri='https://www.image.com/img.png', manufacturer_id=1)
    db.session.add(test_lighter)
    db.session.commit()

    response = client.get('/lighters/1')
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, dict)

def test_get_lighter_by_id_invalid(client):
    response = client.get('/lighters/999')
    assert response.status_code == 404

def test_update_lighter_valid(client):
    test_lighter = Lighter(name='Test Lighter', value=10.0, description='Test Description', image_uri='https://www.image.com/img.png', manufacturer_id=1)
    db.session.add(test_lighter)
    db.session.commit()

    payload = {'name': 'Updated Lighter', 'value': 20.0, 'description': 'Updated Description', 'image_uri': 'https://www.image.com/img2.png'}
    response = client.patch(f'/lighters/{test_lighter.id}', json=payload)
    data = response.get_json()

    assert response.status_code == 201
    assert data['name'] == 'Updated Lighter'
    assert data['value'] == 20.0
    assert data['description'] == 'Updated Description'
    assert data['image_uri']== 'https://www.image.com/img2.png'
    assert isinstance(data, dict)

def test_update_lighter_invalid_id(client):
    payload = {'name': 'Updated Lighter', 'value': 25.0}
    response = client.patch('/lighters/999', json=payload)

    assert response.status_code == 404

def test_update_lighter_invalid_value(client):
    test_lighter = Lighter(name='Test Lighter', value=10.0, description='Test Description', image_uri='https://www.image.com/img.png', manufacturer_id=1)
    db.session.add(test_lighter)
    db.session.commit()

    payload = {'value': 'NOT A FLOAT'}
    response = client.patch(f'/lighters/{test_lighter.id}', json=payload)

    assert response.status_code == 400

def test_delete_lighter_valid_id(client):
    test_lighter = Lighter(name='Test Lighter', value=10.0, description='Test Description', image_uri='https://www.image.com/img.png', manufacturer_id=1)
    db.session.add(test_lighter)
    db.session.commit()

    response = client.delete(f'/lighters/{test_lighter.id}')
    assert response.status_code == 200

def test_delete_lighter_invalid_id(client):
    response = client.delete(f'/lighters/999')
    assert response.status_code == 404