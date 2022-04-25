from app.core.config import settings


def test_read_access(client, basicAuthHash):
    response = client.get("/v1/access/",
                          headers={
                              'Authorization': basicAuthHash,
                              'x-token': settings.API_TOKEN
                          })
    assert response.status_code == 200
    assert not response.json() == {}
