import server as srv

def main():
    server = srv.Server('0.0.0.0', 3000)
    server.start_server() 

if __name__ == '__main__':
    main()