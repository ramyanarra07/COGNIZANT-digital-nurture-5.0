# Digital Nurture 5.0 — Python Backend Frameworks
### Python Backend Frameworks
## NAME : NARRA RAMYA
## REG NO : 212223040128
---

## 📁 Project Structure

```
PythonBackendFrameworks_HandsOn/
├── HANDSON1/      (Web Framework Foundations & Django Setup)
├── HANDSON2/      (Django Models, ORM & Admin)
├── HANDSON3/      (Django REST Views, ViewSets & Routers)
├── HANDSON4/      (Flask App Structure, Routing & Blueprints)
├── HANDSON5/      (Flask + SQLAlchemy ORM Integration)
├── HANDSON6/      (FastAPI Setup, Pydantic & Async Basics)
├── HANDSON7/      (FastAPI Dependency Injection, CRUD & OpenAPI)
├── HANDSON8/      (RESTful API Design Best Practices)
├── HANDSON9/      (JWT Auth, Password Hashing & CORS)
└── HANDSON10/     (Microservices Decomposition & API Gateway)
```

## Tools Used
Django · Django REST Framework · Flask · Flask-SQLAlchemy · FastAPI · Uvicorn · SQLAlchemy
(sync & async) · Pydantic · python-jose · passlib · bcrypt · Postman · Python 3.10+ · VS Code · Git

## Common Scenario: Course Management API

A college digitising its course management process. The API manages **Departments, Courses,
Students, and Enrollments**, exposed through RESTful endpoints consumed by a frontend
application. The same system is built three times — once each in **Django**, **Flask**, and
**FastAPI** — to compare how each framework approaches the same problem.

---

## Hands-On 1 — Web Framework Foundations & Django Project Setup 

**Topics:** Web Framework Concepts · MVC/MVT Pattern · Request-Response Cycle · WSGI vs ASGI ·
Django Project Setup · URL Routing & Middleware

Mapped the journey of a `GET /api/courses/` request through Django (URL router → View → Model →
Response) in code comments, documented where middleware sits in that cycle along with two
built-in middleware classes, and explained WSGI vs ASGI and when Django would switch between
them. Mapped the classic MVC pattern onto Django's MVT convention. Scaffolded the project with
`django-admin startproject coursemanager`, created a `courses` app with `startapp`, registered it
in `INSTALLED_APPS`, wrote a function-based `hello_view` returning a plain `HttpResponse`, and
wired it to `/api/hello/` in `urls.py`.

**Expected Outcome:** Browser shows `Course Management API is running` at `/api/hello/`; the
`courses` app is listed in `INSTALLED_APPS`.

**Output Screenshots:**

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c58be577-5471-494e-94e7-d04f22c36bbd" />


---

## Hands-On 2 — Django Models, ORM & Admin Interface 

**Topics:** Django Models · Field Types & Constraints · Migrations · Django ORM Queries ·
Admin Interface Registration

Defined the `Department`, `Course`, `Student`, and `Enrollment` models with appropriate fields,
`ForeignKey` relations, `__str__` methods, and a `unique_together` constraint on `Enrollment` to
block duplicate enrollments. Ran `makemigrations`/`migrate` and verified the created tables via
`dbshell`. Used the Django shell to create sample departments, courses, and students, then
practiced ORM lookups across relationships (`department__name=...`), `.annotate()` with `Count`,
`select_related` for single-query joins, and a bulk `F()`-expression update on department budgets.
Registered all models in `admin.py` and customised `CourseAdmin` with `list_display`,
`search_fields`, and `list_filter`.

**Expected Outcome:** `showmigrations` shows all migrations applied; ORM queries return the
expected results; the admin interface supports search/filter and rejects duplicate enrollments.

**Output Screenshots:**

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/34b7a1d1-ba19-415d-889c-7955e305413d" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/69227aba-9352-4ff8-9c0f-def42f1a8c61" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/b559c1b6-04f4-4171-90a0-4f7882386cdb" />


---

## Hands-On 3 — Django REST Views, URL Routing & Forms *(Beginner)*

**Topics:** Function-Based Views (FBV) · Class-Based Views (CBV) · URL Routing with `include()` ·
Django REST Framework (DRF) Basics · Serializers · Request & Response Objects

Installed DRF and created `ModelSerializer`s for all four models. Built `CourseListView`
(GET/POST) and `CourseDetailView` (GET/PUT/DELETE) using DRF's `APIView`, wired them into
`courses/urls.py`, and tested every operation in Postman/the browsable API. Refactored both views
into a single `CourseViewSet` extending `viewsets.ModelViewSet`, registered it with a
`DefaultRouter` alongside `StudentViewSet` and `EnrollmentViewSet`, and added a custom `@action`
endpoint `/api/courses/{id}/students/` returning only the students enrolled in that course.

**Expected Outcome:** All 5 HTTP methods return correct status codes (200/201/204/400/404); the
custom `/students/` action returns the correctly filtered list of enrolled students.

**Output Screenshots:**

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/da9270e2-1329-473b-a8f2-07b925a98b59" />


<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8306c740-d14d-4389-964d-32d3fa7d0f58" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/39faeb07-a160-474a-b850-d0966b74640d" />




---

## Hands-On 4 — Flask: App Structure, Routing, Jinja2 & Blueprints *(Intermediate)*

**Topics:** Flask App Structure · Routing & URL Rules · Jinja2 Templates · Request & Response
Objects · Blueprints for Modular Design · Flask Configuration

Structured the Flask project around the **application factory pattern** (`create_app()`), with a
`Config` class supplying `SQLALCHEMY_DATABASE_URI`, `SECRET_KEY`, and `DEBUG`. Built a
`courses_bp` Blueprint with `url_prefix='/api/courses'` and registered it in the factory. Parsed
incoming JSON with `request.get_json()`, validated required fields (`name`, `code`, `credits`),
added full CRUD routes (GET/POST/PUT/DELETE), a consistent JSON response envelope
(`{'status': 'success', 'data': ...}`), and JSON-based error handlers for 404/500 so the API never
falls back to Flask's default HTML error pages.

**Expected Outcome:** All endpoints return JSON; missing required fields return 400 with a
descriptive message; unknown course IDs return 404.

**Output Screenshots:**
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/accdb187-d77c-4afe-81a9-87c547462ab1" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/5f5aa7c2-2c80-4beb-9335-c984bb5ebc5d" />


---

## Hands-On 5 — Flask with SQLAlchemy ORM & Database Integration *(Intermediate)*

**Topics:** Flask-SQLAlchemy Setup · Model Definition · Migrations with Flask-Migrate · ORM CRUD
Operations · Relationship Queries · Connection Pooling

Initialised `db = SQLAlchemy()` / `db.init_app(app)` and defined `Department`, `Course`,
`Student`, and `Enrollment` as `db.Model` subclasses with `db.relationship()` links mirroring the
Django schema. Set up Flask-Migrate (`flask db init/migrate/upgrade`) and inserted sample data via
the Flask shell. Replaced the in-memory route data from Hands-On 4 with real queries
(`Course.query.all()`, `Course.query.get_or_404(id)`), added a `to_dict()` serialization helper on
each model, and wired a JOIN-based `/api/courses/<id>/students/` route.

**Expected Outcome:** `flask db upgrade` creates all tables; CRUD endpoints read from and write to
the database; the `/students/` route returns the correct enrolled students via a JOIN.

**Output Screenshots:**
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/29c72b90-7796-470c-ad36-bda923a708c3" />

<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/75305997-b71b-485b-8317-afbdc1639812" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/3a7cbfcf-de74-414a-a5c8-2a0319196bb0" />

---

## Hands-On 6 — FastAPI: Path Parameters, Pydantic & Async Endpoints *(Intermediate)*

**Topics:** FastAPI Project Setup · Path & Query Parameters · Pydantic Models for Validation ·
Async/Await in FastAPI · Automatic OpenAPI/Swagger Docs · Response Models

Scaffolded `main.py` with `FastAPI(title='Course Management API', version='1.0')` and a root `/`
route. Defined Pydantic schemas — `CourseCreate`, `CourseUpdate` (optional fields), and
`CourseResponse` — plus a nested `DepartmentResponse` to demonstrate nested models. Built
`POST /api/courses/` with automatic request validation (422 on bad input) and explored the
auto-generated Swagger UI at `/docs`. Added a typed path parameter on
`GET /api/courses/{course_id}` and pagination/filter query parameters (`skip`, `limit`,
`department_id`) on the list endpoint, backed by an async SQLAlchemy engine and a `get_db()`
dependency.

**Expected Outcome:** `/docs` shows the `CourseCreate` schema; invalid payloads return 422 with
field-level errors; `GET /api/courses/?skip=&limit=` returns the correctly paginated subset.

**Output Screenshots:**

<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/4412d1d1-5537-4241-992f-f22db2faafd8" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/3c7007d5-d8a5-46a8-8cce-26f28fad5c3d" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/3db11613-aae2-49b7-8fd6-c87a4fd2675f" />




---

## Hands-On 7 — FastAPI: Dependency Injection, CRUD & OpenAPI Documentation *(Intermediate)*

**Topics:** FastAPI Dependency Injection · CRUD Operations · Response Models & Status Codes ·
Background Tasks · OpenAPI Customisation · Error Handling with `HTTPException`

Completed `PUT`/`DELETE` on courses using `response_model=CourseResponse`,
`status_code=201` on create, and `status_code=204` (no body) on delete, raising
`HTTPException(status_code=404, ...)` for missing resources. Added a JOIN-based
`/api/courses/{id}/students/` endpoint and full CRUD for Students and Enrollments. Attached a
`BackgroundTasks` parameter to `POST /api/enrollments/` to simulate an async confirmation email
without blocking the response, then customised the OpenAPI metadata (title, description, version,
contact) and grouped endpoints with `tags` for a cleaner `/docs` page.

**Expected Outcome:** POST returns 201 immediately while the background task logs afterward in the
console; `/docs` shows grouped, well-documented endpoints.

**Output Screenshots:**

<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/961f7b72-c4d8-47ca-b78f-2a194c53c08d" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/ec758dd8-f890-4513-8e76-5e19de3013dd" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/972d8213-5caf-429f-9b5e-ab97f1630742" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/bb201d08-5507-4626-b7d5-fefdc2ae81da" />


---

## Hands-On 8 — RESTful API Design Best Practices *(Advanced)*

**Topics:** REST Principles · HTTP Methods & Status Codes · Resource Naming Conventions · API
Versioning · Pagination & Filtering · Error Response Standards

Audited existing endpoints for REST naming violations (plural nouns, no verbs, hyphens instead of
underscores) and added a `PATCH /api/courses/{id}/` endpoint alongside the existing `PUT`. Verified
status codes across the board (200/201/204/400/401/404/422) and added a `Location` header to POST
responses. Introduced URL-based versioning (`/api/v1/...`), implemented offset pagination
(`page`, `page_size`) with a DRF-style envelope (`count`/`next`/`previous`/`results`), added a
case-insensitive `search=` filter on course name/code, and standardised all error responses to a
single `{'error': {'code', 'message', 'field'}}` shape.

**Expected Outcome:** `GET /api/v1/courses/?page=1&page_size=2` returns the correct paginated
envelope; all error responses follow the standardised format.

**Output Screenshots:**
<img width="1118" height="632" alt="image" src="https://github.com/user-attachments/assets/dfc20045-8054-44ec-b5cf-f002320a3a6f" />

<img width="1126" height="642" alt="image" src="https://github.com/user-attachments/assets/b69c54cf-989c-4700-93e8-7a12750f1605" />

<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/48b5ae68-fcb9-4fcf-b401-b1af8f7deb4e" />
<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/b668090c-af07-4d81-9d79-a84756a1d1cd" />





---

## Hands-On 9 — Authentication & Security: JWT, OAuth2 & OWASP *(Advanced)*

**Topics:** JWT Token Structure · Token-Based Auth vs Session-Based Auth · Password Hashing with
bcrypt · OAuth2 Flow (concept) · CORS Configuration · OWASP Top 10 Awareness

Created a `User` model and `security.py` helpers (`get_password_hash`, `verify_password`) using
passlib's `CryptContext` with the bcrypt scheme. Built `POST /api/v1/auth/register/` — validating
email format, checking for duplicates (409 Conflict), hashing the password, and never storing or
logging plain text. Built `POST /api/v1/auth/login/` to verify credentials and issue a 30-minute
JWT via `python-jose`, plus a `get_current_user()` dependency that decodes/validates the token
(401 on invalid/expired) and protects the course-mutation endpoints. Configured CORS for
`http://localhost:3000` and documented the OAuth2 Authorization Code flow against the simpler JWT
login implemented here.

**Expected Outcome:** Login returns a valid JWT; unauthenticated POST/DELETE requests on
`/api/v1/courses/` return 401; CORS allows the `localhost:3000` frontend origin.

**Output Screenshots:**

<img width="602" height="338" alt="image" src="https://github.com/user-attachments/assets/f0e28572-19be-4556-991c-08d59091ad71" />

<img width="602" height="338" alt="image" src="https://github.com/user-attachments/assets/b6918490-d9fa-4435-ae05-b07f3be8e974" />

<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/ff536d62-3a37-49a4-a20c-b76a2610f604" />

---

## Hands-On 10 — Microservices Architecture: Concepts & Decomposition *(Advanced)*

**Topics:** Monolith vs Microservices · Service Decomposition · Inter-Service Communication · API
Gateway Pattern · Service Discovery (concept)

Identified 3–4 bounded contexts in the existing API — Student Service, Course Service, Auth
Service, Notification Service — and documented each as `Service Name | Responsibility | Endpoints
it owns | Database it owns` in a `README.md`. Built two minimal, independently-running Flask apps:
`course_service/` (port 5001) and `student_service/` (port 5002), each with its own SQLite
database. Added `POST /api/students/{id}/enroll` on Student Service, which calls Course Service's
`GET /api/courses/{id}/` via `requests` to confirm the course exists, catching `ConnectionError`
and returning 503 if Course Service is unreachable. Built a minimal API Gateway (`gateway/`, port
5000) proxying `/api/courses/*` and `/api/students/*` to the correct backend service, and
documented the trade-offs of synchronous (HTTP) vs asynchronous (message queue) inter-service
communication.

**Expected Outcome:** A request through the gateway successfully routes Student Service → Course
Service; stopping Course Service causes the enrollment endpoint to return 503.

**Output Screenshots:**

<img width="940" height="529" alt="image" src="https://github.com/user-attachments/assets/016749e2-6634-43f7-a7c0-7aff6ae789ec" />



---

## Summary

| Hands-On | Topic | Technology |
|---|---|---|
| 1 | Web Framework Foundations & Django Project Setup | Django |
| 2 | Django Models, ORM & Admin Interface | Django |
| 3 | Django REST Views, URL Routing & ViewSets | Django + DRF |
| 4 | Flask App Structure, Routing & Blueprints | Flask |
| 5 | Flask + SQLAlchemy ORM Integration | Flask |
| 6 | FastAPI Setup, Pydantic & Async Basics | FastAPI |
| 7 | FastAPI Dependency Injection, CRUD & OpenAPI Docs | FastAPI |
| 8 | RESTful API Design Best Practices | Django / Flask / FastAPI |
| 9 | JWT Auth, Password Hashing & CORS | Django / Flask / FastAPI |
| 10 | Microservices Decomposition & API Gateway | Flask |

## Submitted By: NARRA RAMYA (212223240128)
