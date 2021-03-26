from flask import Flask
import sys, re
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'ok', 200 , [("Content-Type", "text/plain"), ("X-Organization", "Nintendo")]



if __name__ == '__main__':
    print('ctest.cdn.nintendo.cn Server')
    argvlen = ( len(sys.argv))
    if argvlen == 1:
        print('Usage: switch_server.exe http://yourserverip:port\nExample: kc_server.exe https://10.10.10.10:8888')
        print('As there is no input, the server will be running on http://192.168.6.2:80')
        url = 'http://192.168.6.2:80'
    else:
        url = sys.argv[1]
    try:
        url_s = re.split('://', url)
        ssl = url_s[0]

        if ':' in url_s[1]:
            ip_port = re.split(':', url_s[1])
            server_ip = ip_port[0]
            port = ip_port[1]
        else:
            server_ip = url_s[1]
            if ssl == 'https':
                port = 443
            else:
                port = 80
    except Exception as e:
        input('Invalid input')
        sys.exit()
    lines = []

    if ssl == 'https':
        app.run(ssl_context='adhoc', port=int(port),host=str(server_ip), debug=True)
    else:
        app.run(host=str(server_ip), port=int(port),  debug=True)




#pyinstaller --onefile -i kc.ico switch_server.py