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
