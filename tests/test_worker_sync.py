import pdb
from gunicorn.config import Config
from gunicorn.workers.sync import SyncWorker
from gunicorn.six import BytesIO
from unittest import mock
from t import FakeSocket

def simple_wsgi_app(environ, start_response):
  status = '200 OK'
  output = b'Hello World!\n'
  response_headers = [('Content-type', 'text/plain'),
                      ('Access-Control-Allow-Origin', '*'),
                      ('Content-Length', str(len(output)))]
  #try:
  #    length= int(environ.get('CONTENT_LENGTH', '0'))
  #except ValueError:
  #    length= 0
  #if length > 0:
  #  body= environ['wsgi.input'].read(length)
  start_response(status, response_headers)
  return [output]

#@mock.patch('gunicorn.http.unreader.SocketUnreader')
def test_worker_sync():
  post_data = 'Hello'
  post_request = '\r\n'.join([
    'POST / HTTP/1.1',
    'Content-Length: %d' % len(post_data),
    '',
    post_data,
  ])
  stream = BytesIO(post_request.encode())
  fake_sock = FakeSocket(stream)
  mock_logger = mock.Mock()
  worker = SyncWorker('age',
                      'ppid',
                      'sockets',
                      'app',
                      'timeout',
                      Config(),
                      mock_logger)
  worker.wsgi = simple_wsgi_app
  mock_listener = mock.Mock()
  mock_listener.getsockname.return_value = ('192.168.1.1', '80')
  pdb.set_trace()
  worker.handle(mock_listener, fake_sock, 'addr')
  assert True
