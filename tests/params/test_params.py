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
