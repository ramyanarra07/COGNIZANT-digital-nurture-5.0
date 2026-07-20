# HANDS-ON 1: QA Concepts, Functional Testing & Defect Lifecycle

## Task 1: Map Testing Types to a Real System

### 1. Concrete Test Cases per Test Level
*   **Unit Testing:** Validate that the standalone utility function `validateCourseName()` returns `false` if the input string is empty, ensuring boundary checks work in isolation.
*   **Integration Testing:** Verify that calling the `POST /api/courses` endpoint successfully inserts a record into the database and returns a `201 Created` status code, ensuring communication between the API route and the DB layer works smoothly.
*   **System Testing:** Perform an end-to-end test where a new course is created via `POST /api/courses`, retrieved via `GET /api/courses/{id}`, updated via `PUT`, and verified via a final database state check to ensure the entire application workflow functions as intended.
*   **User Acceptance Testing (UAT):** Act as a College Admin to verify that adding a new engineering course successfully appears on the Admin Dashboard and updates the total course catalog count accurately according to business specifications.

### 2. Functional vs. Non-Functional Classification
*   **Classification:** All four test cases detailed above are **Functional Testing** because they validate *what* the system does (features, inputs, and business requirements).
*   **Non-Functional Test Example (Performance):** Measure the API response time under a load of 500 concurrent users to verify that the `GET /api/courses` endpoint responds within less than 2 seconds.

### 3. Black-Box vs. White-Box Testing
*   **Black-Box Testing:** Testing the software application without any knowledge of its internal structure, code architecture, or paths. The tester interacts solely with the user interface or API endpoints based on specifications.
*   **White-Box Testing:** Testing the application with full visibility and access to the internal source code, control flows, data structures, and logic.
*   **Roles:** **QA Testers** typically perform Black-Box (or Gray-Box) testing, while **Developers** primarily perform White-Box testing (such as writing unit tests and performing code coverage analysis).

### 4. Formal Test Cases for POST `/api/courses`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-POST-01** | Verify successful creation of a course with valid payload. | User is authorized to add courses. | 1. Send POST request to `/api/courses` with valid JSON body containing `course_name` and `duration`. | Status code `201 Created`. Response contains a unique course ID and the payload matches database entry. | | |
| **TC-POST-02** | Verify request rejection when mandatory fields are missing. | User is authorized to add courses. | 1. Send POST request to `/api/courses` with an empty JSON object `{}`. | Status code `400 Bad Request`. Error message specifies missing fields. | | |
| **TC-POST-03** | Verify request rejection when duplicate course code is provided. | A course with code 'CS101' already exists. | 1. Send POST request with payload containing duplicate course code 'CS101'. | Status code `409 Conflict` or `400 Bad Request`. System prevents duplicate record creation. | | |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle Description
The defect lifecycle maps the journey of a bug from discovery to resolution:
1.  **New:** The bug is logged by the tester and enters the system.
2.  **Assigned:** The test lead or project manager assigns the bug to a specific developer.
3.  **Open:** The developer begins analyzing and working on a fix for the bug.
4.  **Fixed:** The developer finishes writing the code fix and deploys it to the test environment.
5.  **Retest:** The tester executes the specific test cases again to verify if the fix works.
6.  **Verified:** The tester confirms the bug is resolved in the environment.
7.  **Closed:** The bug is permanently closed and archived after verification.

**Alternative Paths:**
*   **Rejected:** The developer or lead marks it as "Rejected" if it is not an actual bug, works as designed, or cannot be reproduced.
*   **Deferred:** The bug is marked "Deferred" if it is valid but has low priority, meaning it will be fixed in a future release cycle rather than the current sprint.

### 6. Bug Severity and Priority Classification

*   **a) POST `/api/courses` returns 500 Internal Server Error for all requests.**
    *   **Severity:** Critical (Core functionality is completely broken, blocking further testing of course creation).
    *   **Priority:** P1 (Requires immediate fix as it completely halts backend integrations).
*   **b) Course names longer than 150 characters are silently truncated without an error.**
    *   **Severity:** Medium (Data integrity issue, but the system does not crash).
    *   **Priority:** P3 (Should be fixed, but can wait until major blockers are resolved).
*   **c) The `/docs` Swagger page has a typo in the API description.**
    *   **Severity:** Low (Cosmetic defect that does not impact application code functionality).
    *   **Priority:** P4 (Low priority, can be addressed during routine cleanup).
*   **d) Login with correct credentials occasionally returns 401 on the first attempt (intermittent).**
    *   **Severity:** High (Impacts fundamental security/authentication, even if intermittent).
    *   **Priority:** P2 (Needs quick investigation because intermittent auth bugs point to deeper stability issues).

### 7. Complete Defect Report for Bug (a)

*   **Defect ID:** DEF-001
*   **Title:** POST `/api/courses` returns 500 Internal Server Error for all requests
*   **Environment:** QA Environment - Staging v1.2
*   **Build Version:** Build #2026.07.13
*   **Severity:** Critical
*   **Priority:** P1
*   **Steps to Reproduce:**
    1. Navigate to the API client tool (e.g., Postman) or the `/docs` Swagger UI page.
    2. Construct a valid POST request to `/api/courses` with payload: `{"course_name": "QA Basics", "duration": "4 weeks"}`.
    3. Execute the request.
*   **Expected Result:** The endpoint should return a `201 Created` status code and return the created course object.
*   **Actual Result:** The endpoint returns status code `500 Internal Server Error` with a blank response body.
*   **Attachments:** [screenshot of 500 error]

### 8. Severity vs. Priority Explanation
*   **Severity** refers to the technical impact a defect has on the software's functionality or operation (How badly is the system broken?).
*   **Priority** refers to the business urgency dictating how quickly the defect needs to be fixed (How fast do we need to patch this?).

**Real-World Example (High Severity, Low Priority):**
Consider a scenario where the application completely crashes (High Severity) if an admin attempts to generate an "Annual Archive Report for the Year 2015". Because this legacy report is only processed once a year and is rarely touched, the business may classify it as **Low Priority (P4)**, choosing to fix active checkout flow issues first.