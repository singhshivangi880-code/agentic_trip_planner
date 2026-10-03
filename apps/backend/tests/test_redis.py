import pytest
from unittest.mock import AsyncMock, patch

# Patch before importing Cache so the global client is mocked
with patch("redis.asyncio.from_url") as mock_from_url:
    mock_redis = AsyncMock()
    mock_from_url.return_value = mock_redis
    from app.core.redis import Cache, redis_client

@pytest.fixture(autouse=True)
def reset_mock():
    mock_redis.reset_mock()
    
@pytest.mark.asyncio
async def test_cache_get_set():
    mock_redis.get.return_value = '{"foo": "bar"}'
    
    val = await Cache.get("test_key")
    assert val == {"foo": "bar"}
    mock_redis.get.assert_called_once_with("test_key")
    
    await Cache.set("test_key", {"foo": "bar"}, ttl=60)
    mock_redis.set.assert_called_once_with("test_key", '{"foo": "bar"}', ex=60)

@pytest.mark.asyncio
async def test_cache_delete():
    await Cache.delete("test_key")
    mock_redis.delete.assert_called_once_with("test_key")

@pytest.mark.asyncio
async def test_workflow_state():
    mock_redis.get.return_value = '{"step": 1}'
    state = await Cache.get_workflow_state("wf1")
    assert state == {"step": 1}
    
    await Cache.set_workflow_state("wf1", {"step": 2})
    mock_redis.set.assert_called_once_with("workflow:wf1", '{"step": 2}', ex=86400)

@pytest.mark.asyncio
async def test_check_idempotency():
    # True means NX worked (new key)
    mock_redis.set.return_value = True
    is_new = await Cache.check_idempotency("req123")
    assert is_new is True
    mock_redis.set.assert_called_once_with("idempotency:req123", "1", nx=True, ex=3600)
    
    # False means NX failed (key exists)
    mock_redis.set.return_value = None
    is_new = await Cache.check_idempotency("req123")
    assert is_new is False
