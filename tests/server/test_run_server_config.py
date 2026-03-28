import mcp_server as srv

def test_run_server_uses_mcp_env_streamable_http(monkeypatch):
    called = {}

    def fake_run(**kwargs):
        called.update(kwargs)
    monkeypatch.setattr(srv.mcp, 'run', fake_run)
    monkeypatch.setenv('MCP_TRANSPORT', 'streamable-http')
    monkeypatch.setenv('MCP_HOST', '127.0.0.1')
    monkeypatch.setenv('MCP_PORT', '8081')
    monkeypatch.setenv('MCP_PATH', '/mcp')
    srv.run_server()
    assert called.get('transport') == 'streamable-http'
    assert called.get('host') == '127.0.0.1'
    assert called.get('port') == 8081
    assert called.get('path') == '/mcp'

def test_run_server_uses_mcp_env_sse(monkeypatch):
    called = {}

    def fake_run(**kwargs):
        called.update(kwargs)
    monkeypatch.setattr(srv.mcp, 'run', fake_run)
    monkeypatch.setenv('MCP_TRANSPORT', 'sse')
    monkeypatch.setenv('MCP_HOST', '0.0.0.0')
    monkeypatch.setenv('MCP_PORT', '8082')
    monkeypatch.setenv('MCP_SSE_PATH', '/events')
    srv.run_server()
    assert called.get('transport') == 'sse'
    assert called.get('host') == '0.0.0.0'
    assert called.get('port') == 8082
    assert called.get('path') == '/events'

def test_run_server_applies_license_from_env(monkeypatch):
    called = {'client_id': None, 'client_secret':None}

    def fake_apply_license(client_id, client_secret):
        called['client_id'] = client_id
        called['client_secret'] = client_secret
    def fake_run(**kwargs):
        pass

    monkeypatch.setenv('ASPOSE_CLOUD_CLIENT_ID', 'xxxx-xxxxxxxxxxxxxxxxx-xxxx')
    monkeypatch.setenv('ASPOSE_CLOUD_CLIENT_SECRET','xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    monkeypatch.setattr('core.utils.spreadsheet_util.apply_license', fake_apply_license)
    monkeypatch.setattr(srv.mcp, 'run', fake_run)

    srv.run_server()

    assert called['client_id'] == 'xxxx-xxxxxxxxxxxxxxxxx-xxxx'
    assert called['client_secret'] == 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
def test_run_server_applies_license_from_arg_over_env(monkeypatch):
    called = {'client_id': None, 'client_secret':None}

    def fake_apply_license(client_id, client_secret):
        called['client_id'] = client_id
        called['client_secret'] = client_secret
    def fake_run(**kwargs):
        pass


    monkeypatch.setenv('ASPOSE_CLOUD_CLIENT_ID', 'xxxx-xxxxxxxxxxxxxxxxx-xxxx')
    monkeypatch.setenv('ASPOSE_CLOUD_CLIENT_SECRET','xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    monkeypatch.setattr('core.utils.license.apply_license', fake_apply_license)
    monkeypatch.setattr(srv.mcp, 'run', fake_run)

    srv.run_server(license_path='/tmp/license_arg.lic')

    assert called['lic'] == '/tmp/license_arg.lic'
