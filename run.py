import socket

urls = {
    '/': 'hello index',
    '/blog': 'hello blog'
}

def parse_request(request):
    split_obj = request.split(' ')
    return (split_obj[0], split_obj[1])

def generate_headers(method, url):
    if method != 'GET':
        return ('HTTP/1.1 405 method not allowed\n\n', 405)
    if not url in urls:
        return ('HTTP/1.1 404 not found\n\n', 404)
    return ('HTTP/1.1 200 it is ok\n\n', 200)

def generate_content(code, url):
    if code == 405:
        return '<h1>405<h1/><p>Method not Allowed<p/>'
    if code == 404:
        return '<h1>404<h1/><p>Not Found<p/>'
    return '<h1>200 -- {}<h1/><p>It is OK!<p/>'.format(urls[url])


def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    content = generate_content(code, url)
    return (headers + content).encode()

def run():
    server_socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket_obj.bind(('localhost', 5000))
    server_socket_obj.listen()

    while True:
        client_socket, addr = server_socket_obj.accept()
        request = client_socket.recv(1024)

        response = generate_response(request.decode('utf-8'))

        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    run()
