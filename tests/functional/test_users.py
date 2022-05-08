def test_home_page_post_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test.client.post('/')
    assert response.status_code == 405
    assert b`Flask User Management Example!` not in response.data

def test_home_page_get_with_fixture(test_client):
     """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test.client.get('/')
    #Using `assert`, check the followingh
    #1. 200(OK) status returned
    #2. Expected text is the response
	assert response.status_code == 200
    assert b`Flask User Management Example!` in response.data