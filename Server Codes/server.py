import requests
import socket
import json

def main():
    host = '192.168.243.124'
    port = 8121

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    
    print("Server Started")
    
    while True:
        data, addr = s.recvfrom(1024)
        data = json.loads(data)
        print(data)
        try:
            # Sending data to the server [DJANGO local server ]
            # Server should be running in the background
            requests.post('http://127.0.0.1:8000/addData', data)
        except Exception as e:
            pass
    s.close()

if __name__=='__main__':
    main()
