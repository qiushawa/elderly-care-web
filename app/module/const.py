class HttpStatus:
    OK = 200
    CREATED = 201
    NOT_FOUND = 404
    BAD_REQUEST = 400

class Docs:    
    def __init__(self, title, description, example_response):
        self.title = title
        self.description = description
        self.example_response = example_response