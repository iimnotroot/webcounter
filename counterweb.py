import sys
import http.server
import http.cookies
import socketserver

def validate_args(args: list[str]):
    if len(args) != 2:
        print("usage: counterweb.py <port>")
        exit(1)
    try:
        int(args[1])
    except ValueError:
        print("error: port must be a number")
        exit(1)

class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self) -> None:

        print("Received: GET " + self.path)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")

        cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))
        current_counter: int
        new_counter: int
        if 'counter' in cookies:
            try:
                current_counter = int(cookies['counter'].value)
                if current_counter > 5 or current_counter < 0:
                    raise ValueError("cookie counter is not a valid number")
            except ValueError as e:
                print(f"error: {e}")
                current_counter = 6

            if current_counter == 0:
                new_counter = 5
            else:
                new_counter = current_counter - 1

        else:
            new_counter = 5

        cookie = http.cookies.SimpleCookie()
        cookie['counter'] = str(new_counter)
        self.send_header("Set-Cookie", cookie.output(header='', sep=''))

        self.end_headers()
        self.wfile.write(str(new_counter).encode('utf-8'))




def main() -> None:
    args: list[str] = sys.argv
    validate_args(args)
    port: int = int(args[1])
    with socketserver.TCPServer(("localhost", port), Handler) as MyServer:
        print("serving at port", port)
        MyServer.serve_forever()

if __name__ == "__main__":
    main()
