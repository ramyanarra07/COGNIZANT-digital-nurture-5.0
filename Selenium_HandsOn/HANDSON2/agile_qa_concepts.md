# HANDS-ON 2: SDLC vs TDLC — V-Model & Agile QA Integration

---

## Task 1: V-Model Mapping

### 9. V-Model Diagram (ASCII Art Mapping)

```text
  SDLC Phases (Development)                         TDLC Phases (Testing)
  =========================                         =====================
  
  [Requirements Phase]  ------------------------->  [Acceptance Testing]
           \                                                 ^
            v                                                |
     [System Design]  ----------------------------->  [System Testing]
              \                                              ^
               v                                             |
        [Architecture Design]  -------------------->  [Integration Testing]
                 \                                           ^
                  v                                          |
           [Module Design]  ----------------------->  [Unit Testing]
                    \                                        ^
                     v                                       |
                     =======> [ Coding Phase ] =======>======
                              (Bottom Vertex)
```

### 10. SDLC <=> TDLC Phase Pairings & Test Artifacts
*   **Requirements Phase <=> Acceptance Testing:** The *Acceptance Test Plan* and *Acceptance Test Cases* are prepared during this phase based on customer/business requirements.
*   **System Design Phase <=> System Testing:** The *System Test Plan* and end-to-end user workflow test cases are produced here to validate overall system specifications.
*   **Architecture Design Phase <=> Integration Testing:** The *Integration Test Suite* and interface/API contract validation test scenarios are designed here to evaluate subsystem communications.
*   **Module Design Phase <=> Unit Testing:** Developers author low-level *Unit Test Scripts* alongside the detailed logic component specifications for individual modules or functions.

### 11. Entry and Exit Criteria for Testing Levels

| Testing Level | Entry Criteria (What must be true to start) | Exit Criteria (What must be true to finish) |
| :--- | :--- | :--- |
| **Unit Testing** | • Module code complete and compiles without syntax errors.<br>• Low-level code design documents are available. | • 100% of planned unit tests executed successfully.<br>• Code coverage goals (e.g., 80%+) are met. |
| **Integration Testing** | • All required modules pass Unit Testing.<br>• API structural contracts or interfaces are exposed. | • Integration/API connection suites run cleanly.<br>• Zero critical or high architectural defects remain open. |
| **System Testing** | • Integrated application build is deployed to the QA environment.<br>• Complete system test cases are approved. | • All planned end-to-end tests are executed.<br>• Total defect count drops below the defined quality threshold. |
| **Acceptance Testing**| • System testing is fully signed off with no critical bugs.<br>• UAT environment is prepared with near-real production data. | • Business scenarios fulfill all defined acceptance criteria.<br>• Formal stakeholder/admin sign-off is achieved. |

### 12. Two Early QA Engagement Points in the Course Management API Project
*   **Requirements Review (Left Side - Top):** Engaging QA during the analysis of the Course Management requirements catches ambiguities—such as undefined string boundaries or missing edge cases for unique course codes—long before any code is typed.
*   **Architecture Design / Contract Definition (Left Side - Middle):** Participating while the API contracts (e.g., Swagger/OpenAPI schemas) are drafted allows QA to define mock test templates early, preventing interface mismatches between front-end and back-end modules before coding.

---

## Task 2: Agile QA and Shift-Left Testing

### 13. Three Problems of Waterfall Testing for the Course Management API Project
*   **Late Defect Discovery:** If bugs in the core course-creation endpoints or database schemas are discovered only at the end of the lifecycle, fixing them requires rewriting large parts of the completed codebase, causing costly delays.
*   **High Risk of Scope Creep/Misalignment:** Because the API is built completely before testing begins, any misinterpretation of the initial business requirements (e.g., how course codes map to enrollment rules) isn't caught until it is too late.
*   **Testing Bottlenecks:** QA is squeezed into a tiny window at the very end of the schedule. If development runs late, testing time is cut short, forcing the API to release with hidden bugs or unverified endpoints.

### 14. QA Engineer Roles in Agile Ceremonies
*   **Sprint Planning:** Collaborates with Product Owners and developers to analyze user stories, identify ambiguities, and define clear, measurable **Acceptance Criteria** before a single line of code is written.
*   **Daily Standup:** Shares daily testing progress, reports on blockers/impediments (e.g., test environment downtime or dependency delays), and aligns with developers on which bug fixes are ready for verification.
*   **Sprint Review:** Demos completed features to stakeholders from a quality perspective, confirming that the new API features meet the agreed-upon standards.
*   **Retrospective:** Contributes to continuous process improvement by discussing what went well, what testing bottlenecks occurred, and how the team can collaborate better to prevent defects in the next sprint.

### 15. Four Shift-Left Practices Applied to the Course Management API
*   **(a) Reviewing Requirements for Testability:** The QA team audits the user stories early to ensure requirements like *"should handle course codes"* explicitly state the length, character constraints, and validation rules before development kicks off.
*   **(b) Writing Test Cases Before Code (TDD/BDD):** QA defines the concrete Gherkin scenarios and test cases upfront. This gives developers a crystal-clear checklist of what behaviors their code must satisfy to pass testing.
*   **(c) Static Code Analysis:** Integrating automated linter and static code checking tools into the local development workflow or CI/CD pipeline to catch syntax issues, code smells, and basic logic flaws before the code is compiled.
*   **(d) API Contract Testing Before Integration:** Using tools to validate that the API request/response structures perfectly match the predefined OpenAPI/Swagger specifications, allowing front-end and back-end teams to test against the contract long before full integration happens.

### 16. Acceptance Criteria in Given-When-Then (Gherkin) Format

**User Story:** 
*As a college admin, I want to create a new course, so that students can enroll in it.*

#### Scenario 1: Successful Course Creation (Happy Path)
```gherkin
Given the college admin is authenticated and authorized to manage courses
When the admin sends a POST request to "/api/courses" with a unique course code "CS-101" and a valid course name "Introduction to Computer Science"
Then the system should return a status code of 201 Created
And the new course should be saved in the database and visible in the course catalog
```

#### Scenario 2: Error Handling for Duplicate Course Code
```gherkin
Given the college admin is authenticated and a course with code "CS-101" already exists in the system
When the admin attempts to create a new course using the duplicate course code "CS-101"
Then the system should reject the request with a status code of 400 Bad Request or 409 Conflict
And the response body should contain an error message stating "Course code already exists"
```

#### Scenario 3: Error Handling for Missing Required Fields
```gherkin
Given the college admin is authenticated and looking at the course creation endpoint
When the admin sends a request to create a course but leaves the mandatory "course_name" field empty
Then the system should reject the request with a status code of 400 Bad Request
And the response body should display a validation error message stating "Course name is a required field"
```