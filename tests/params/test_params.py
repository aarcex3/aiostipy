import io

import pytest
from aiohttp import web


@pytest.mark.asyncio
async def test_body_param(client):
    resp = await client.get("/body", json={"Test": "Test"})
    assert resp.status == 200
    json_response = await resp.json()
    assert json_response == {"Test": "Test"}


@pytest.mark.asyncio
async def test_no_body_param(client):
    resp = await client.get("/body")
    assert resp.status == 400


@pytest.mark.asyncio
async def test_query_param(client):
    resp = await client.get("/get_query", params={"a": 3, "b": 3})
    assert resp.status == 200
    json_response = await resp.json()
    assert json_response["result"] == 6


@pytest.mark.asyncio
async def test_query_param_wrong_type(client):
    resp = await client.get("/get_query", params={"a": "'3'", "b": 3})
    assert resp.status == 400


@pytest.mark.asyncio
async def test_header(client):
    response = await client.get("/get_header", headers={"X-Custom": "test-value"})

    assert response.status == 200

    json_data = await response.json()
    assert json_data["x_custom"] == "test-value"


@pytest.mark.asyncio
async def test_header_missing(client):
    response = await client.get("/get_header")

    assert response.status == 400
    assert "Missing header 'X-Custom'" in await response.text()


@pytest.mark.asyncio
async def test_get_cookie(client):
    response = await client.get("/get_cookie", cookies={"my_cookie": "test-value"})
    assert response.status == 200

    json_data = await response.json()
    assert json_data["cookie"] == "test-value"


@pytest.mark.asyncio
async def test_get_cookie_missing(client):
    response = await client.get("/get_cookie", cookies={})
    assert response.status == 400


@pytest.mark.asyncio
async def test_request(client):
    response = await client.get("/request", json={"test": "test"})
    assert response.status == 200
    data = await response.json()
    assert data["test"] == "test"


@pytest.mark.asyncio
async def test_path(client):
    response = await client.get(f"/get_path/{4}/{10}")
    assert response.status == 200

    json_data = await response.json()
    assert json_data["result"] == 14


@pytest.mark.asyncio
async def test_path_invalid_type(client):
    response = await client.get(f"/get_path/{4}/g")
    assert response.status == 400
    assert "Invalid type for path parameter 'b'. Expected int." in await response.text()


@pytest.mark.asyncio
async def test_path_missing_param(client):
    response = await client.get(f"/get_path/{4}")
    assert response.status == 404


@pytest.mark.asyncio
async def test_file(client):

    fake_file = io.BytesIO(b"This is a test file.")
    fake_file.name = "test.txt"

    data = {"file": fake_file}
    response = await client.post("/post_file", data=data)
    assert response.status == 200

    json_data = await response.json()
    assert json_data["filename"] == "test.txt"
    assert json_data["content"] == "This is a test file."


@pytest.mark.asyncio
async def test_file_exception(client):
    response = await client.post("/post_file")
    assert response.status == 400
