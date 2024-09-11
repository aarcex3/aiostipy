import pytest


@pytest.mark.asyncio
async def test_app_info(client):
    resp = await client.get("/app_info")
    assert resp.status == 200
    json_response = await resp.json()
    assert json_response == {"version": "1.0.0", "name": "Testapp"}


@pytest.mark.asyncio
async def test_request_info(client):
    resp = await client.post("/request_info")
    assert resp.status == 200
    json_response = await resp.json()
    assert json_response == {"scheme": "http"}
