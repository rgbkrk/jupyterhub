"""Tests for the ORM bits"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from .. import orm

try:
    unicode
except NameError:
    # py3
    unicode = str


def test_server(db):
    server = orm.Server()
    db.add(server)
    db.commit()
    assert server.ip == u'localhost'
    assert server.base_url == '/'
    assert server.proto == 'http'
    assert isinstance(server.port, int)
    assert isinstance(server.cookie_name, unicode)
    assert isinstance(server.cookie_secret, bytes)
    assert server.url == 'http://localhost:%i/' % server.port


def test_proxy(db):
    proxy = orm.Proxy(
        auth_token=u'abc-123',
        public_server=orm.Server(
            ip=u'192.168.1.1',
            port=8000,
        ),
        api_server=orm.Server(
            ip=u'127.0.0.1',
            port=8001,
        ),
    )
    db.add(proxy)
    db.commit()
    assert proxy.public_server.ip == u'192.168.1.1'
    assert proxy.api_server.ip == u'127.0.0.1'
    assert proxy.auth_token == u'abc-123'


def test_hub(db):
    hub = orm.Hub(
        server=orm.Server(
            ip = u'1.2.3.4',
            port = 1234,
            base_url='/hubtest/',
        ),
        
    )
    db.add(hub)
    db.commit()
    assert hub.server.ip == u'1.2.3.4'
    hub.server.port == 1234
    assert hub.api_url == u'http://1.2.3.4:1234/hubtest/api'


def test_user(db):
    user = orm.User(name=u'kaylee',
        server=orm.Server(),
        state={'pid': 4234},
    )
    db.add(user)
    db.commit()
    assert user.name == u'kaylee'
    assert user.server.ip == u'localhost'
    assert user.state == {'pid': 4234}


def test_tokens(db):
    user = orm.User(name=u'inara')
    db.add(user)
    db.commit()
    token = user.new_cookie_token()
    db.add(token)
    db.commit()
    assert token in user.cookie_tokens
    db.add(user.new_cookie_token())
    db.add(user.new_cookie_token())
    db.add(user.new_api_token())
    db.commit()
    assert len(user.api_tokens) == 1
    assert len(user.cookie_tokens) == 3
    
