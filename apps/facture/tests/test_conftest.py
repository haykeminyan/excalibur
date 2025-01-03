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



def test_superuser_creation(superuser):
    assert superuser.is_superuser, "Superuser flag should be True"
    assert superuser.is_staff, "Staff flag should be True for superuser"
    assert superuser.username == 'superuser', "Username should match the created username"
    assert superuser.check_password('password'), "Password should be correctly set and verified"
