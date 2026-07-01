"""
Task 1: Request-Response Cycle Notes
--------------------------------------

1. Journey of GET /api/courses/ request:
   Browser sends HTTP GET request
   -> Django receives it via WSGI/ASGI server
   -> URL Router (urls.py) matches '/api/courses/' to a View function
   -> View calls the Model to query the database (e.g. Course.objects.all())
   -> Model returns data from DB
   -> View serializes/formats the data
   -> View returns an HttpResponse/JsonResponse
   -> Response travels back through middleware to the browser

2. Middleware sits between the request coming in and the view being called,
   and between the view's response and it going back to the browser.
   Built-in Django middleware examples:
   - SecurityMiddleware: enforces HTTPS, security headers
   - AuthenticationMiddleware: attaches the logged-in user (request.user) to each request

3. WSGI vs ASGI:
   - WSGI (Web Server Gateway Interface): synchronous, handles one request at a time
     per worker. Django's default.
   - ASGI (Asynchronous Server Gateway Interface): supports async views, WebSockets,
     long-lived connections.
   - Django uses WSGI by default (see wsgi.py). Switch to ASGI (asgi.py) when you need
     WebSockets, async views, or real-time features like chat/notifications.

4. MVC vs Django's MVT:
   - MVC: Model (data) -> View (business logic/controller) -> Controller (handles input)
   - Django MVT: Model (data) -> View (business logic, like MVC's Controller) ->
     Template (presentation, like MVC's View)
   - Mapping: Django's "View" = MVC's "Controller". Django's "Template" = MVC's "View".
     Django's "Model" = MVC's "Model" directly.
"""