# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import logging
import math

# TO DO: set constants
IP = "127.0.0.1"
PORT = 80
SOCKET_TIMEOUT = 300
SOURCE_FOLDER = "webroot"
client_socket = socket.socket()
DEFAULT_URL = f"{SOURCE_FOLDER}/index.html"
FILES_SOURCE_FOLDER = r"webroot\uploads\files uploaded"


def get_file_data(filename):
    """ Get data from file """
    with open(filename, 'rb') as f:
        return f.read()


def send404(message="NOT_FOUND"):
    logging.warning(f"ERROR 404: {message}")
    client_socket.send(f"HTTP/1.1 404 {message} \r\n".encode())


def send403(message="FORBIDDEN"):
    logging.warning(f"ERROR 403: {message}")
    client_socket.send(f"HTTP/1.1 403 {message} \r\n".encode())


def send500(message="INTERNAL_SERVER_ERROR"):
    logging.error(f"ERROR 500: {message}")
    client_socket.send(f"HTTP/1.1 500 {message}  \r\n".encode())


def get_next_number(number: str):
    return str(int(number) + 1)


def get_parameters(url: str):
    url = url[url.find("?") + 1: url.find(" HTTP/1.1")]
    url = url.split("&")
    parameters = {}
    for i in url:
        parameters[i[0:i.find("=")]] = i[i.find("=") + 1::]
    return parameters if parameters != {} else None


def get_area(parameters):
    width = float(parameters["width"])
    height = float(parameters["height"])
    return str(width * height / 2)


def handle_client_get_request(resource):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    if resource == ' ':
        url = DEFAULT_URL
    else:
        url = resource

    # TO DO: check if URL had been redirected, not available or other error code. For example:
    if url in {}:
        pass
    else:
        pass
    if url != DEFAULT_URL:
        filename = f"{SOURCE_FOLDER}" + url
    else:
        filename = url
    if url[url.find("/") + 1:url.find("?")] == "calculate-next":
        try:
            data = get_next_number(get_parameters(url)["num"])
            http_header = "HTTP/1.1 200 OK \r\n" + f"Content-Length: {len(data)}\r\n" + "Content-Type: text/plain\r\n\r\n"
            client_socket.send(http_header.encode() + data.encode())
        except ValueError:
            send404("the input can only be numbers")
    elif url[url.find("/") + 1:url.find("?")] == "calculate-area":
        try:
            parameters = get_parameters(url)
            data = get_area(parameters)
            http_header = "HTTP/1.1 200 OK \r\n" + f"Content-Length: {len(data)}\r\n" + "Content-Type: text/plain\r\n\r\n"
            client_socket.send(http_header.encode() + data.encode())
        except ValueError:
            send404("the input can only be numbers")
        except KeyError:
            send404("not enough parameter")
    elif url[url.find("/") + 1:url.find("?")] == "image":
        filename = get_parameters(url)["image-name"] + ".jpg"
        data = get_file_data(fr"{FILES_SOURCE_FOLDER}\{filename}")
        http_header = "HTTP/1.1 200 OK\r\n" + f"Content-Length: {len(data)}\r\n" + "Content-Type: image/jpeg\r\n\r\n"
        client_socket.send(http_header.encode() + data)

    else:
        data = get_file_data(filename)
        # TO DO: send 302 redirection response
        file_type = url[url.find(".")::]
        http_header = ""
        if file_type.lower() == 'html':
            http_header = "HTTP/1.1 200 OK \r\n" + f"Content-Length: {len(data)}\r\n" + "Content-Type: text/html\r\n\r\n"
        elif file_type.lower() == 'jpg':
            http_header = "HTTP/1.1 200 OK \r\n" + f"Content-Length: {len(data)}\r\n" + "Content-Type: image/jpeg\r\n\r\n"
        elif file_type.lower() == "js":
            http_header = "HTTP/1.1 200 OK \r\n" + f"Content-Length: {len(data)}\r\n" + "Content-Type: text/javascript; charset=UTF-8\r\n\r\n"
        elif file_type.lower() == "css":
            http_header = "HTTP/1.1 200 OK \r\n" + f"Content-Length: {len(data)}\r\n" + "Content-Type: text/css\r\n\r\n"
        elif file_type.lower() == "ico":
            http_header = "HTTP/1.1 200 OK \r\n" + f"Content-Length: {len(data)}\r\n" + "Content-Type: image/ico\r\n\r\n"
        elif file_type.lower() == "gif":
            http_header = "HTTP/1.1 200 OK \r\n" + f"Content-Length: {len(data)}\r\n" + "Content-Type: image/gif\r\n\r\n"
        client_socket.send(http_header.encode() + data)


def handle_client_post_request(resource):
    filename = get_parameters(resource)["file-name"]
    contentLength = float(resource[resource.find("Content-Length: ") + len("Content-Length: "):resource.find("\r",
                                                                                                             resource.find(
                                                                                                                 "Content-Length: "))])
    data = "".encode()
    for i in range(math.ceil(contentLength / 1024)):
        data += client_socket.recv(1024)
    with open(f"{FILES_SOURCE_FOLDER}\{filename}", 'wb') as f:
        f.write(data)
    client_socket.send("HTTP/1.1 200 OK".encode())


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    request = request.decode()
    if request[0:3] == "GET":
        if request[0:14] == "GET / HTTP/1.1":
            return "GET", True, " "
        else:
            return "GET", True, request[4:request.find("HTTP/1.1")]
    if request[0:4] == "POST":
        if request[0:14] == "POST / HTTP/1.1":
            return "POST", True, " "
        else:
            return "POST", True, request
    else:
        return None, False, ""


def handle_client():
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        # TO DO: insert code that receives client request
        try:
            client_request = client_socket.recv(1024)
            print(client_request.decode())
            kind, valid_http, resource = validate_http_request(client_request)
            if valid_http:
                print('Got a valid HTTP request')
                if kind == "GET":
                    handle_client_get_request(resource)
                else:
                    handle_client_post_request(resource)
                break
            else:
                print('Error: Not a valid HTTP request')
                send404()
                break
        except Exception as e:
            send500(str(e))
            break
    print('Closing connection...')
    print('Server Still Up And Running')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    global client_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client()


if __name__ == "__main__":
    # Call the main handler function
    main()
