-- =========================================================
-- MODULE 3: DATABASE INTEGRATION — HANDS-ON 1 to 4 (MySQL)
-- =========================================================

DROP DATABASE IF EXISTS college_db;
CREATE DATABASE college_db;
USE college_db;
SET SQL_SAFE_UPDATES = 0;


-- =========================================================
-- HANDS-ON 1: Schema Design & Core SQL — DDL and Normalisation
-- =========================================================

-- ---------------------------------------------------------
-- TASK 1: Create the Database and Tables
-- ---------------------------------------------------------

CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name     VARCHAR(100) NOT NULL,
    hod_name      VARCHAR(100),
    budget        DECIMAL(12,2)
);

CREATE TABLE students (
    student_id      INT AUTO_INCREMENT PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth   DATE,
    department_id   INT,
    enrollment_year INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE courses (
    course_id     INT AUTO_INCREMENT PRIMARY KEY,
    course_name   VARCHAR(150) NOT NULL,
    course_code   VARCHAR(20) UNIQUE,
    credits       INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE enrollments (
    enrollment_id   INT AUTO_INCREMENT PRIMARY KEY,
    student_id      INT,
    course_id       INT,
    enrollment_date DATE,
    grade           CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE professors (
    professor_id  INT AUTO_INCREMENT PRIMARY KEY,
    prof_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(100) UNIQUE,
    department_id INT,
    salary        DECIMAL(10,2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Verify: 
SHOW TABLES; 
DESCRIBE students;


-- ---------------------------------------------------------
-- TASK 2: Verify Normalisation (1NF, 2NF, 3NF)
-- ---------------------------------------------------------

-- 1NF CHECK:
-- Every column in every table holds a single atomic value (no comma-separated
-- lists, no repeating groups). Hypothetical violation: storing multiple phone
-- numbers like "9876543210,9123456780" in one phone_number field would break
-- 1NF. Our schema avoids this entirely — 1NF is satisfied.

-- 2NF CHECK:
-- enrollments has a surrogate primary key (enrollment_id), with
-- student_id + course_id as a composite candidate key. The non-key columns
-- enrollment_date and grade both depend on the full combination of
-- student_id AND course_id together (a grade only makes sense for a specific
-- student in a specific course), not on either column alone. No partial
-- dependency exists — 2NF is satisfied.

-- 3NF CHECK:
-- No transitive dependencies exist. Test case: if dept_name were stored
-- directly in the students table, it would depend on department_id, which
-- itself depends on student_id (the PK) — making dept_name transitively
-- dependent on the PK, violating 3NF. We avoid this by storing dept_name
-- only in departments and referencing it via the department_id foreign key
-- in students, courses, and professors. 3NF is satisfied.

-- CONCLUSION: college_db satisfies 1NF, 2NF, and 3NF.


-- ---------------------------------------------------------
-- TASK 3: Alter and Extend the Schema
-- ---------------------------------------------------------

ALTER TABLE students ADD COLUMN phone_number VARCHAR(15);
ALTER TABLE courses ADD COLUMN max_seats INT DEFAULT 60;

ALTER TABLE enrollments
ADD CONSTRAINT chk_grade CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL);

ALTER TABLE departments CHANGE hod_name head_of_dept VARCHAR(100);

ALTER TABLE students DROP COLUMN phone_number;

-- Verify:
SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'college_db' AND TABLE_NAME = 'courses';


-- =========================================================
-- HANDS-ON 2: Writing SQL Queries — DML, Joins & Aggregations
-- =========================================================

-- ---------------------------------------------------------
-- TASK 1: Insert, Update and Delete Data
-- ---------------------------------------------------------

INSERT INTO departments (dept_name, head_of_dept, budget) VALUES
 ('Computer Science', 'Dr. Ramesh Kumar', 850000.00),
 ('Electronics', 'Dr. Priya Nair', 620000.00),
 ('Mechanical', 'Dr. Suresh Iyer', 540000.00),
 ('Civil', 'Dr. Ananya Sharma', 430000.00);

INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
 ('Arjun', 'Mehta', 'arjun.mehta@college.edu', '2003-04-12', 1, 2022),
 ('Priya', 'Suresh', 'priya.suresh@college.edu', '2003-07-25', 1, 2022),
 ('Rohan', 'Verma', 'rohan.verma@college.edu', '2002-11-08', 2, 2021),
 ('Sneha', 'Patel', 'sneha.patel@college.edu', '2004-01-30', 3, 2023),
 ('Vikram', 'Das', 'vikram.das@college.edu', '2003-09-14', 1, 2022),
 ('Kavya', 'Menon', 'kavya.menon@college.edu', '2002-05-17', 2, 2021),
 ('Aditya', 'Singh', 'aditya.singh@college.edu', '2004-03-22', 4, 2023),
 ('Deepika','Rao', 'deepika.rao@college.edu', '2003-08-09', 1, 2022);

INSERT INTO courses (course_name, course_code, credits, department_id) VALUES
 ('Data Structures & Algorithms', 'CS101', 4, 1),
 ('Database Management Systems', 'CS102', 3, 1),
 ('Object Oriented Programming', 'CS103', 4, 1),
 ('Circuit Theory', 'EC101', 3, 2),
 ('Thermodynamics', 'ME101', 3, 3);

INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
 (1, 1, '2022-07-01', 'A'), (1, 2, '2022-07-01', 'B'),
 (2, 1, '2022-07-01', 'B'), (2, 3, '2022-07-01', 'A'),
 (3, 4, '2021-07-01', 'A'), (4, 5, '2023-07-01', NULL),
 (5, 1, '2022-07-01', 'C'), (5, 2, '2022-07-01', 'A'),
 (6, 4, '2021-07-01', 'B'), (7, 5, '2023-07-01', NULL),
 (8, 1, '2022-07-01', 'A'), (8, 3, '2022-07-01', 'B');

INSERT INTO professors (prof_name, email, department_id, salary) VALUES
 ('Dr. Anand Krishnan', 'anand.k@college.edu', 1, 95000.00),
 ('Dr. Meena Pillai', 'meena.p@college.edu', 1, 88000.00),
 ('Dr. Sunil Rajan', 'sunil.r@college.edu', 2, 82000.00),
 ('Dr. Latha Gopal', 'latha.g@college.edu', 3, 79000.00),
 ('Dr. Kartik Bose', 'kartik.b@college.edu', 4, 76000.00);

-- Step 16: Insert two additional students
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
 ('Ramya', 'Narra', 'ramya.narra@college.edu', '2003-02-18', 1, 2022),
 ('Karthik', 'Subramaniam', 'karthik.s@college.edu', '2003-06-21', 2, 2022);

-- Step 17: Update grade
UPDATE enrollments
SET grade = 'B'
WHERE student_id = 5 AND course_id = 1;

-- Step 18: Preview, then delete NULL grades
SELECT * FROM enrollments WHERE grade IS NULL;
DELETE FROM enrollments WHERE grade IS NULL;

-- Step 19: Verify row counts
SELECT COUNT(*) FROM students;
SELECT COUNT(*) FROM enrollments;


-- ---------------------------------------------------------
-- TASK 2: Single-Table Queries and Filtering
-- ---------------------------------------------------------

SELECT * FROM students
WHERE enrollment_year = 2022
ORDER BY last_name ASC;

SELECT * FROM courses
WHERE credits > 3
ORDER BY credits DESC;

SELECT * FROM professors
WHERE salary BETWEEN 80000 AND 95000;

SELECT * FROM students
WHERE email LIKE '%@college.edu';

SELECT enrollment_year, COUNT(*) AS student_count
FROM students
GROUP BY enrollment_year;


-- ---------------------------------------------------------
-- TASK 3: Multi-Table Joins
-- ---------------------------------------------------------

SELECT CONCAT(s.first_name, ' ', s.last_name) AS full_name, d.dept_name
FROM students s
JOIN departments d ON s.department_id = d.department_id;

SELECT CONCAT(s.first_name, ' ', s.last_name) AS student_name, c.course_name, e.grade
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id;

SELECT s.student_id, s.first_name, s.last_name
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
WHERE e.enrollment_id IS NULL;

SELECT c.course_name, COUNT(e.enrollment_id) AS enrollment_count
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name;

SELECT d.dept_name, p.prof_name, p.salary
FROM departments d
LEFT JOIN professors p ON d.department_id = p.department_id;


-- ---------------------------------------------------------
-- TASK 4: Aggregations and Grouping
-- ---------------------------------------------------------

SELECT c.course_name, COUNT(e.enrollment_id) AS enrollment_count
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name;

SELECT d.dept_name, ROUND(AVG(p.salary), 2) AS avg_salary
FROM departments d
JOIN professors p ON d.department_id = p.department_id
GROUP BY d.department_id, d.dept_name;

SELECT dept_name, budget
FROM departments
WHERE budget > 600000;

SELECT e.grade, COUNT(*) AS grade_count
FROM enrollments e
JOIN courses c ON e.course_id = c.course_id
WHERE c.course_code = 'CS101'
GROUP BY e.grade;

SELECT d.dept_name, COUNT(DISTINCT e.student_id) AS student_count
FROM departments d
JOIN students s ON d.department_id = s.department_id
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY d.department_id, d.dept_name
HAVING COUNT(DISTINCT e.student_id) > 2;


-- =========================================================
-- HANDS-ON 3: Advanced SQL — Subqueries, Views & Transactions
-- =========================================================

-- ---------------------------------------------------------
-- TASK 1: Subqueries
-- ---------------------------------------------------------

SELECT s.student_id, s.first_name, s.last_name, COUNT(e.enrollment_id) AS total_courses
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.enrollment_id) > (
    SELECT AVG(course_count) FROM (
        SELECT COUNT(*) AS course_count
        FROM enrollments
        GROUP BY student_id
    ) AS sub
);

SELECT c.course_id, c.course_name
FROM courses c
WHERE EXISTS (SELECT 1 FROM enrollments e WHERE e.course_id = c.course_id)
AND NOT EXISTS (
    SELECT 1 FROM enrollments e
    WHERE e.course_id = c.course_id AND (e.grade IS NULL OR e.grade <> 'A')
);

SELECT p.prof_name, p.department_id, p.salary
FROM professors p
WHERE p.salary = (
    SELECT MAX(p2.salary) FROM professors p2
    WHERE p2.department_id = p.department_id
);

SELECT dept_avg.department_id, dept_avg.avg_salary
FROM (
    SELECT department_id, AVG(salary) AS avg_salary
    FROM professors
    GROUP BY department_id
) AS dept_avg
WHERE dept_avg.avg_salary > 85000;


-- ---------------------------------------------------------
-- TASK 2: Creating and Using Views
-- ---------------------------------------------------------

CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    d.dept_name,
    COUNT(e.enrollment_id) AS num_courses,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4 WHEN 'B' THEN 3 WHEN 'C' THEN 2
            WHEN 'D' THEN 1 WHEN 'F' THEN 0 ELSE NULL
        END
    ), 2) AS gpa
FROM students s
JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, full_name, d.dept_name;

CREATE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4 WHEN 'B' THEN 3 WHEN 'C' THEN 2
            WHEN 'D' THEN 1 WHEN 'F' THEN 0 ELSE NULL
        END
    ), 2) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

SELECT * FROM vw_student_enrollment_summary
WHERE gpa > 3.0;

-- Step 42: Attempt to UPDATE through the view (expected to fail)
-- UPDATE vw_student_enrollment_summary SET gpa = 4.0 WHERE student_id = 1;
-- WHY THIS FAILS: This view aggregates multiple tables using JOIN, GROUP BY,
-- COUNT, and AVG. The database cannot map gpa or num_courses back to a single
-- underlying row to update, since these are computed values, not stored
-- columns. A view is only updatable when it maps directly to one table's rows
-- without aggregation, GROUP BY, DISTINCT, or multi-table joins.

CREATE VIEW vw_cs_students AS
SELECT student_id, first_name, last_name, email, department_id
FROM students
WHERE department_id = 1
WITH CHECK OPTION;
-- WITH CHECK OPTION ensures any INSERT/UPDATE through this view that would
-- produce a row with department_id <> 1 is rejected, since such a row
-- would not be visible through the view's own WHERE clause.


-- ---------------------------------------------------------
-- TASK 3: Stored Procedures and Transactions
-- ---------------------------------------------------------

DELIMITER $$

CREATE PROCEDURE sp_enroll_student(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_enrollment_date DATE
)
BEGIN
    DECLARE existing_count INT;

    SELECT COUNT(*) INTO existing_count
    FROM enrollments
    WHERE student_id = p_student_id AND course_id = p_course_id;

    IF existing_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate enrollment: student already enrolled in this course';
    ELSE
        INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
        VALUES (p_student_id, p_course_id, p_enrollment_date, NULL);
    END IF;
END$$

DELIMITER ;

-- Test:
CALL sp_enroll_student(1, 4, '2026-06-30');   -- succeeds
CALL sp_enroll_student(1, 1, '2026-06-30');   -- fails (duplicate)

CREATE TABLE department_transfer_log (
    log_id        INT AUTO_INCREMENT PRIMARY KEY,
    student_id    INT,
    old_dept_id   INT,
    new_dept_id   INT,
    transfer_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (new_dept_id) REFERENCES departments(department_id)
);

DELIMITER $$

CREATE PROCEDURE sp_transfer_student(
    IN p_student_id INT,
    IN p_new_dept_id INT
)
BEGIN
    DECLARE old_dept INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT department_id INTO old_dept FROM students WHERE student_id = p_student_id;

    UPDATE students SET department_id = p_new_dept_id WHERE student_id = p_student_id;

    INSERT INTO department_transfer_log (student_id, old_dept_id, new_dept_id)
    VALUES (p_student_id, old_dept, p_new_dept_id);

    COMMIT;
END$$

DELIMITER ;

-- Test:
-- CALL sp_transfer_student(2, 3);
-- SELECT * FROM department_transfer_log;

-- Step 46: Force rollback with invalid department_id (FK violation)
-- CALL sp_transfer_student(2, 999);
-- SELECT * FROM students WHERE student_id = 2;

-- Step 47: SAVEPOINT test
START TRANSACTION;

INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
VALUES (3, 2, '2026-06-30', NULL);

SAVEPOINT after_first_insert;

-- Deliberately fail: course_id 999 does not exist (FK violation)
-- INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
-- VALUES (3, 999, '2026-06-30', NULL);

ROLLBACK TO SAVEPOINT after_first_insert;
COMMIT;

-- Verify only the first insert persisted:
SELECT * FROM enrollments WHERE student_id = 3 AND course_id = 2;


-- =========================================================
-- HANDS-ON 4: Query Optimisation — Indexes, EXPLAIN & N+1
-- =========================================================

-- ---------------------------------------------------------
-- TASK 1: Baseline Performance — No Indexes
-- ---------------------------------------------------------

EXPLAIN FORMAT=JSON
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- BASELINE RESULT: query plan shows a full table scan on "students" because
-- enrollment_year has no index — MySQL must check every row's value.
-- Rows examined on students: equal to total row count in the table.
-- This will scale poorly as the students table grows.


-- ---------------------------------------------------------
-- TASK 2: Add Indexes and Compare Plans
-- ---------------------------------------------------------

CREATE INDEX idx_enrollment_year ON students(enrollment_year);
CREATE UNIQUE INDEX idx_unique_enrollment ON enrollments(student_id, course_id);
CREATE INDEX idx_course_code ON courses(course_code);

EXPLAIN FORMAT=JSON
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- AFTER INDEX RESULT: the plan now shows an Index Scan / ref access type on
-- students.enrollment_year instead of a full table scan, since MySQL can
-- jump directly to matching rows using idx_enrollment_year rather than
-- checking every row. Rows examined drops significantly.

-- Step 55: MySQL has no true partial indexes (that's PostgreSQL-only via
-- WHERE clause on CREATE INDEX). MySQL workaround: a regular composite index
-- still helps the optimizer when filtering with IS NULL.
CREATE INDEX idx_enrollment_grade_null ON enrollments(student_id, grade);


-- ---------------------------------------------------------
-- TASK 3: N+1 Problem — documented here, implemented separately
-- ---------------------------------------------------------
-- Steps 56-59 require Python (mysql-connector-python), not pure SQL.
-- See n_plus_one_demo.py in the same GitHub folder for that part.
-- Summary: fetching enrollments then querying each student individually in
-- a loop = N+1 queries; rewriting as a single JOIN = 1 query regardless of
-- row count. At 10,000 enrollments, the N+1 version would issue 10,001
-- queries vs. 1 for the JOIN version.