# middleware.py

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Initialize cart in the session if not present
        if 'cart' not in request.session:
            request.session['cart'] = {}

        response = self.get_response(request)
        return response