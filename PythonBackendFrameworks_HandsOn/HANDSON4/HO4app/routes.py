from flask import Blueprint, jsonify, request

# 39. Define the Blueprint with the required URL prefix
courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

# In-memory database simulator for tracking data during testing
# Format: { course_id (int): { "name": str, "code": str, "credits": int } }
courses_db = {}
id_counter = 1

# 44. Helper function to return a consistent JSON envelope
def make_response_json(data, status_code):
    envelope = {
        'status': 'success' if status_code < 400 else 'error',
        'data': data
    }
    return jsonify(envelope), status_code

# 39 & 41. GET all courses & POST a new course
@courses_bp.route('/', methods=['GET'])
def get_courses():
    # Returns a list of all course dictionaries
    all_courses = list(courses_db.values())
    return jsonify(all_courses)

@courses_bp.route('/', methods=['POST'])
def create_course():
    global id_counter
    
    # 42. Check if Content-Type is application/json
    req_data = request.get_json()
    if req_data is None:
        return make_response_json({'message': 'Invalid JSON or missing Content-Type header.'}, 400)
    
    # 42. Validate that required fields are present
    required_fields = ['name', 'code', 'credits']
    missing_fields = [field for field in required_fields if field not in req_data]
    
    if missing_fields:
        return make_response_json(
            {'message': f'Missing required fields: {", ".join(missing_fields)}'}, 
            400
        )
    
    # Extract values and assign a unique ID
    new_course = {
        'id': id_counter,
        'name': req_data['name'],
        'code': req_data['code'],
        'credits': req_data['credits']
    }
    
    courses_db[id_counter] = new_course
    id_counter += 1
    
    return make_response_json(new_course, 201)

# 43. GET, PUT, and DELETE by course_id
@courses_bp.route('/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    if course_id not in courses_db:
        return make_response_json({'message': f'Course with ID {course_id} not found.'}, 404)
    return make_response_json(courses_db[course_id], 200)

@courses_bp.route('/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    if course_id not in courses_db:
        return make_response_json({'message': f'Course with ID {course_id} not found.'}, 404)
        
    req_data = request.get_json()
    if req_data is None:
        return make_response_json({'message': 'Invalid JSON data provided.'}, 400)
        
    # Update fields if provided in request body
    course = courses_db[course_id]
    course['name'] = req_data.get('name', course['name'])
    course['code'] = req_data.get('code', course['code'])
    course['credits'] = req_data.get('credits', course['credits'])
    
    return make_response_json(course, 200)

@courses_bp.route('/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    if course_id not in courses_db:
        return make_response_json({'message': f'Course with ID {course_id} not found.'}, 404)
        
    deleted_course = courses_db.pop(course_id)
    return make_response_json({'message': f'Course {deleted_course["code"]} successfully deleted.'}, 200)