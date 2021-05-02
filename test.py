resource=['P', 'O', 'S', 'T', ' ', '/', 'u', 'p', 'l', 'o', 'a', 'd', '?', 'f', 'i', 'l', 'e', '-', 'n', 'a', 'm', 'e', '=', 'g', 'r', 'a', 'p', 'h', '.', 'i', 'c', 'o', ' ', 'H', 'T', 'T', 'P', '/', '1', '.', '1', '\r', '\n', 'H', 'o', 's', 't', ':', ' ', '1', '2', '7']
resource = "".join(resource)
print(resource)
print(resource[resource.find("Content-Length: "):resource.find("\r", resource.find("Content-Length: "))])
contentLength = float(resource[resource.find("Content-Length: "):resource.find("\r", resource.find("Content-Length: "))])
print(contentLength)