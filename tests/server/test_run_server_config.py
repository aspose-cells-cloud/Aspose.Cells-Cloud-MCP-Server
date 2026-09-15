"""Hermetic tests for mcp_server.run_server transport/credential wiring.

The real MCP server process is never started; ``mcp.run`` is monkeypatched so we
can assert the exact arguments run_server derives from environment variables and
function arguments. ``register_tools`` is also stubbed to keep the tests fast.
"""

import os

import pytest

pytest.importorskip('fastmcp')

import mcp_server as srv


@pytest.fixture
def patch_run(monkeypatch):
    monkeypatch.setattr(srv, 'register_tools', lambda: None)
    called = {}

    def fake_run(**kwargs):
        called.update(kwargs)

    monkeypatch.setattr(srv.mcp, 'run', fake_run)
    return called


@pytest.fixture
def clean_transport_env(monkeypatch):
    """Isolate a test from ambient transport env vars."""
    monkeypatch.delenv('MCP_TRANSPORT', raising=False)
    monkeypatch.delenv('TRANSPORT', raising=False)


def _http(called):
    """The transport/host/port/path run_server derived for an HTTP transport."""
    return {k: called[k] for k in ('transport', 'host', 'port', 'path')}


def test_streamable_http_from_env(monkeypatch, patch_run, clean_transport_env):
    monkeypatch.setenv('MCP_TRANSPORT', 'streamable-http')
    monkeypatch.setenv('MCP_HOST', '127.0.0.1')
    monkeypatch.setenv('MCP_PORT', '8081')
    monkeypatch.setenv('MCP_PATH', '/mcp')
    srv.run_server()
    assert _http(patch_run) == {'transport': 'streamable-http', 'host': '127.0.0.1', 'port': 8081, 'path': '/mcp'}
    # no middleware is ever attached now (bearer auth was removed -> anonymous)
    assert 'middleware' not in patch_run


def test_sse_from_env(monkeypatch, patch_run, clean_transport_env):
    monkeypatch.setenv('MCP_TRANSPORT', 'sse')
    monkeypatch.setenv('MCP_HOST', '0.0.0.0')
    monkeypatch.setenv('MCP_PORT', '8082')
    monkeypatch.setenv('MCP_SSE_PATH', '/events')
    srv.run_server()
    assert _http(patch_run) == {'transport': 'sse', 'host': '0.0.0.0', 'port': 8082, 'path': '/events'}


def test_function_arg_precedence_over_env(monkeypatch, patch_run, clean_transport_env):
    monkeypatch.setenv('MCP_TRANSPORT', 'sse')
    srv.run_server(transport='streamable-http')
    assert patch_run['transport'] == 'streamable-http'


def test_http_uses_default_path_when_env_unset(monkeypatch, patch_run, clean_transport_env):
    monkeypatch.setenv('MCP_TRANSPORT', 'streamable-http')
    srv.run_server()
    assert patch_run['path'] == '/mcp'


def test_stdin_default_transport(monkeypatch, patch_run, clean_transport_env):
    srv.run_server()
    assert patch_run == {'transport': 'stdio'}
    assert 'middleware' not in patch_run


def test_credentials_from_args_set_env(monkeypatch, patch_run, clean_transport_env):
    # run_server writes into the real process env by design; snapshot and restore
    # so the ambient (or absent) credentials are left untouched for other tests.
    old_id = os.environ.get('ASPOSE_CLOUD_CLIENT_ID')
    old_secret = os.environ.get('ASPOSE_CLOUD_CLIENT_SECRET')
    try:
        srv.run_server(client_id='id-from-arg', client_secret='secret-from-arg')
        assert os.environ['ASPOSE_CLOUD_CLIENT_ID'] == 'id-from-arg'
        assert os.environ['ASPOSE_CLOUD_CLIENT_SECRET'] == 'secret-from-arg'
    finally:
        if old_id is None:
            os.environ.pop('ASPOSE_CLOUD_CLIENT_ID', None)
        else:
            os.environ['ASPOSE_CLOUD_CLIENT_ID'] = old_id
        if old_secret is None:
            os.environ.pop('ASPOSE_CLOUD_CLIENT_SECRET', None)
        else:
            os.environ['ASPOSE_CLOUD_CLIENT_SECRET'] = old_secret


def test_env_credentials_are_preserved_without_args(monkeypatch, patch_run, clean_transport_env):
    monkeypatch.setenv('ASPOSE_CLOUD_CLIENT_ID', 'id-from-env')
    monkeypatch.setenv('ASPOSE_CLOUD_CLIENT_SECRET', 'secret-from-env')
    srv.run_server()
    assert os.environ['ASPOSE_CLOUD_CLIENT_ID'] == 'id-from-env'
    assert os.environ['ASPOSE_CLOUD_CLIENT_SECRET'] == 'secret-from-env'
