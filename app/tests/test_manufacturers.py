import pytest
from flask import Flask
from app import create_app, db
from app.models import Manufacturer
from app.manufacturers import bp
    
def test_get_all_manufacturers(client):
    response = client.get('/manufacturers/')
    data = response.get_json()
    assert response.status_code == 200
    assert isinstance(data, list)

def test_create_manufacturer_valid(client):
    payload = {'name': 'New manufacturer', 'description': 'New Description', 'image_uri': 'https://www.image.com/img.png', 'manufacturer_id': 1}
    response = client.post('/manufacturers/', json=payload)
    data = response.get_json()

    assert response.status_code == 201
    assert data['name'] == 'New manufacturer'
    assert data['description'] == 'New Description'
    assert data['image_uri'] == 'https://www.image.com/img.png'
    assert isinstance(data, dict)

def test_create_manufacturer_invalid_no_name(client): # Missing name param
    payload = {'description': 'New Description', 'image_uri': 'https://www.image.com/img.png'}
    response = client.post('/manufacturers/', json=payload)

    assert response.status_code == 400

def test_get_manufacturer_by_id_valid(client):
    test_manufacturer = Manufacturer(name='Test manufacturer', description='Test Description', image_uri='https://www.image.com/img.png')
    db.session.add(test_manufacturer)
    db.session.commit()

    response = client.get('/manufacturers/1')
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, dict)

def test_get_manufacturer_by_id_invalid(client):
    response = client.get('/manufacturers/999')
    assert response.status_code == 404

def test_update_manufacturer_valid(client):
    test_manufacturer = Manufacturer(name='Test manufacturer', description='Test Description', image_uri='https://www.image.com/img.png')
    db.session.add(test_manufacturer)
    db.session.commit()

    payload = {'name': 'Updated manufacturer', 'description': 'Updated Description', 'image_uri': 'https://www.image.com/img2.png'}
    response = client.patch(f'/manufacturers/{test_manufacturer.id}', json=payload)
    data = response.get_json()

    assert response.status_code == 201
    assert data['name'] == 'Updated manufacturer'
    assert data['description'] == 'Updated Description'
    assert data['image_uri']== 'https://www.image.com/img2.png'
    assert isinstance(data, dict)

def test_update_manufacturer_invalid_id(client):
    payload = {'name': 'Updated manufacturer'}
    response = client.patch('/manufacturers/999', json=payload)

    assert response.status_code == 404

def test_delete_manufacturer_valid_id(client):
    test_manufacturer = Manufacturer(name='Test manufacturer', description='Test Description', image_uri='https://www.image.com/img.png')
    db.session.add(test_manufacturer)
    db.session.commit()

    response = client.delete(f'/manufacturers/{test_manufacturer.id}')
    assert response.status_code == 200

def test_delete_manufacturer_invalid_id(client):
    response = client.delete(f'/manufacturers/999')
    assert response.status_code == 404