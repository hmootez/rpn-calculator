headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
}


def test_swagger_page(client):
    """
    test swagger ui page
    """
    response = client.get('/apidocs/')
    assert response.status_code == 200


def test_push_element(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/rpn/stack/push/ (Post) then check the response
    """
    response = client.post('/rpn/stack/push', headers=headers, json={
        "value": "10",
    })
    print(response)
    assert response.status_code == 200
    assert b"10 pushed" in response.data


def test_peek_element(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    client.post('/rpn/stack/push', headers=headers, json={
        "value": "10",
    })
    response = client.get('/rpn/stack/peek')
    print(response.data)
    assert response.status_code == 200
    assert b"Top: 10" in response.data


def test_clear_stack(client):
    """
    test clearing the stack
    """
    response = client.delete('/rpn/stack')
    print(response)
    assert response.status_code == 200
    assert b"all elements are deleted" in response.data


def test_pop_empty_stack(client):
    """
    test pop the stack when the stack is empty
    """
    client.delete('/rpn/stack')
    response = client.get('/rpn/stack/pop')
    print(response)
    assert response.status_code == 400
    assert b"the stack is empty" in response.data


def test_pop_stack(client):
    """
    test pop the stack when the stack is empty
    """
    client.post('/rpn/stack/push', headers=headers, json={
        "value": "10",
    })
    response = client.get('/rpn/stack/pop')
    print(response)
    assert response.status_code == 200
    assert b"10 popped" in response.data


def test_operation_plus(client):
    client.post('/rpn/stack/push', headers=headers, json={
        "value": "10",
    })
    client.post('/rpn/stack/push', headers=headers, json={
        "value": "15",
    })
    client.post('/rpn/apply', headers=headers, json={
        "operator": "+",
    })
    response = client.get('/rpn/stack/peek')
    assert response.status_code == 200
    assert b"Top: 25" in response.data


def test_operation_minus(client):
    client.post('/rpn/stack/push', headers=headers, json={
        "value": "10",
    })
    client.post('/rpn/stack/push', headers=headers, json={
        "value": "15",
    })
    client.post('/rpn/apply', headers=headers, json={
        "operator": "-",
    })
    response = client.get('/rpn/stack/peek')
    assert response.status_code == 200
    assert b"Top: 5" in response.data


def test_operation_multiply(client):
    client.post('/rpn/stack/push', headers=headers, json={
        "value": "10",
    })
    client.post('/rpn/stack/push', headers=headers, json={
        "value": "15",
    })
    client.post('/rpn/apply', headers=headers, json={
        "operator": "*",
    })
    response = client.get('/rpn/stack/peek')
    assert response.status_code == 200
    assert b"Top: 150" in response.data


def test_operation_divide(client):
    client.post('/rpn/stack/push', headers=headers, json={
        "value": "10",
    })
    client.post('/rpn/stack/push', headers=headers, json={
        "value": "15",
    })
    client.post('/rpn/apply', headers=headers, json={
        "operator": "/",
    })
    response = client.get('/rpn/stack/peek')
    assert response.status_code == 200
    assert b"Top: 1.5" in response.data







