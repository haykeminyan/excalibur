def test_factory_creates_request(factory):
    # Create a GET request
    request = factory.get('/test-url/')
    assert request.method == 'GET'
    assert request.path == '/test-url/'

    # Create a POST request
    data = {'key': 'value'}
    request = factory.post('/test-url/', data)
    assert request.method == 'POST'
    assert request.path == '/test-url/'
    assert request.POST['key'] == 'value'
