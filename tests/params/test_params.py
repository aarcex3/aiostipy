import pytest


@pytest.mark.asyncio
async def test_body_param(client):
    resp = await client.get("/body", json={"Test": "Test"})
    assert resp.status == 200
    json_response = await resp.json()
    assert json_response == {"Test": "Test"}
