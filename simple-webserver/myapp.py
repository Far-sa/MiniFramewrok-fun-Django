# from webob import Request, Response
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule


# class API():
#     def __call__(self, environ, start_response):

#         data = b"Hey Puppet!\n"
#         start_response("200,OK", [{
#             "Content-type": "text/plain",
#             "Content-length": str(len(data))
#         }])
#         return iter([data])

class TextResponse(Response):
    pass


class API():
    def __init__(self) -> None:
        self.routes = {}

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def dispatch_request(self, request):
        # response = Response()

        for path, handler in self.routes.items():
            if path == request.path:
                response = handler(request)
                return response
        response = self.error_404(request)
        return response

    def error_404(self, request):
        return TextResponse("Page not found!", status=404)

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper


app = API()


@app.route("/")
def index(req):
    return TextResponse("Index Page")


@app.route("/user/<string:username>")
def user(req, username):
    return TextResponse(f"Hey ,{username}")


@app.route("/dashboard")
def dashboard(req):
    return TextResponse("Dashboard Page")
