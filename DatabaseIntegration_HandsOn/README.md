# Digital Nurture 5.0 — Module 3: Database Integration
### Python Full Stack Engineer- Database Integration

This README documents the completed work for all **7 Hands-On exercises** of Module 3 (Database Integration), covering **MySQL, MongoDB, and Python ORM/Migrations**. It follows the single scenario used throughout the book — a **Student Course Registration System (`college_db`)**.

---

## Project Structure

```
DatabaseIntegration_HandsOn
├── HANDSON1-4/
│   ├── SQL HANDSON 1-4.sql   (Schema Design, DML/Joins, Subqueries/Views/Transactions, Indexes/EXPLAIN/N+1)
│   ├── n_plus_one_demo.py    (N+1 problem simulation & fix)
│   └── Readme.md
├── HANDSON5/                 (MongoDB — mongosh / Compass scripts)
├── HANDSON6/                 (SQLAlchemy ORM — models.py, crud.py)
├── HANDSON7/                 (Alembic migration scripts)
└── Readme.md
```

## Tools Used
MySQL Community Server 8.x (via MySQL Workbench) · MongoDB Community Server + Compass · Python 3.10+ · VS Code · `mysql-connector-python` · `pymongo` · `sqlalchemy` · `flask-sqlalchemy` · Alembic

## 🎓 Common Scenario: Student Course Registration System

A college digitising its Course Registration process. The relational schema (`college_db`) has five tables: **`departments`**, **`students`**, **`courses`**, **`enrollments`**, and **`professors`**, all pre-populated with the sample data provided in the book (4 departments, 8 students, 5 courses, 12 enrollments, 5 professors).

---

## Hands-On 1 — Schema Design & Core SQL: DDL and Normalisation

**Topics:** Database Schema Design · Normalisation (1NF–3NF) · ER Relationships · DDL — `CREATE` / `ALTER` / `DROP` · Referential Integrity

Created the full `college_db` schema from scratch: `CREATE TABLE` statements for all five tables with `NOT NULL`, `UNIQUE`, `PRIMARY KEY`, and `FOREIGN KEY` constraints enforcing referential integrity (students → departments, courses → departments, enrollments → students/courses, professors → departments). Documented 1NF/2NF/3NF compliance in SQL comments, then safely extended the schema with `ALTER TABLE` — adding `phone_number` and `max_seats` columns, a `CHECK` constraint on `grade`, renaming `hod_name` → `head_of_dept`, and rolling back the `phone_number` column.

**Expected Outcome:** All 5 tables created with no errors; `DESCRIBE` confirms columns and constraints; each `ALTER` runs cleanly and the final schema matches the plan.

**Output Screenshots:**

**TASK-1**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/cb360a5d-f8a4-44bf-bae2-ce8ad1318866" />
**TASK-3**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/abb0b1d6-3d69-4c9d-aa94-f1e05a28f5a5" />

---

## Hands-On 2 — Writing SQL Queries: DML, Joins & Aggregations

**Topics:** DML — `INSERT` / `UPDATE` / `DELETE` · `SELECT` with `WHERE` / `ORDER BY` · `INNER JOIN`, `LEFT JOIN`, multi-table joins · Aggregate Functions (`COUNT`, `AVG`, `SUM`, `MAX`) · `GROUP BY` and `HAVING`

Populated `college_db` with the sample data, added two extra students, updated a grade, and deleted un-graded enrollments. Wrote single-table filtering queries (`WHERE`, `ORDER BY`, `LIKE`, `BETWEEN`), multi-table joins spanning 2–4 tables (student-department, enrollment-student-course, students with no enrollments via `LEFT JOIN`, courses with zero enrollments, departments with/without professors), and aggregation reports (enrollments per course, average salary per department, department budgets over ₹600,000, grade distribution for CS101, and `HAVING`-filtered department enrollment counts).

**Expected Outcome:** `students` table has 10 rows; `enrollments` only retains non-NULL grades; join queries correctly surface unmatched rows; aggregate queries return one row per department/course as expected.

**Output Screenshots:**
**TASK-1**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/05892cf4-07c5-4309-bdde-0708b79066bc" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d8586f9b-3d2c-4a0d-b6bc-53742d05b012" />
**TASK-2**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/844e1252-75ce-4639-b027-761c69c780b5" />
**TASK-3**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c7255268-b81e-4307-9b87-c5511d1d0683" />
**TASK-4**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0b53c5f7-ce06-453a-8c6d-6f7b86ef9fe1" />

---

## Hands-On 3 — Advanced SQL: Subqueries, Views & Transactions

**Topics:** Subqueries (correlated & non-correlated) · Views — creation, usage, updatable views · Stored Procedures (MySQL) · Transactions — `COMMIT`, `ROLLBACK`, `SAVEPOINT` · Indexes and Query Plans

Used non-correlated subqueries (students enrolled above the average), correlated subqueries/`NOT EXISTS` (courses with all-A grades, top-paid professor per department), and derived-table subqueries (departments with average salary > 85,000). Built `vw_student_enrollment_summary` and `vw_course_stats` views (including a GPA conversion via `CASE`), tested view updatability, and recreated a view `WITH CHECK OPTION`. Wrote `sp_enroll_student` and `sp_transfer_student` stored procedures wrapped in transactions with `ROLLBACK` on failure, plus a `SAVEPOINT` test for partial rollback.

**Expected Outcome:** Subqueries return correct filtered result sets; `vw_course_stats` returns 5 rows (one per course); the transfer procedure rolls back cleanly on error; the `SAVEPOINT` test shows only the pre-savepoint insert surviving.

**Output Screenshots:**

**TASK-1**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/19f97953-e6b3-40fe-a1bc-ba61275432aa" />
**TASK-2**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/76a77fa5-3f3e-4154-af75-cba9c3dc40a4" />

---

## Hands-On 4 — Query Optimisation: Indexes, EXPLAIN & the N+1 Problem

**Topics:** Index Types — B-Tree, Composite, Partial · `EXPLAIN` / `EXPLAIN FORMAT=JSON` · Query Plans — Seq Scan vs Index Scan · N+1 Query Problem · Connection Pooling (concept)

Captured a baseline `EXPLAIN FORMAT=JSON` plan on a 3-table join query and identified a Full Table Scan. Added a B-Tree index on `students.enrollment_year`, a composite `UNIQUE` index on `enrollments(student_id, course_id)`, and an index on `courses.course_code` — then re-ran `EXPLAIN` to confirm the plan shifted from a table scan to an index-backed plan. Simulated the classic **N+1 problem** in Python (`n_plus_one_demo.py`) with 1 query + N per-row lookups, then fixed it with a single `JOIN` query, comparing round-trip counts and timing.

**Expected Outcome:** Post-index `EXPLAIN` shows an index-backed scan; the composite unique index blocks duplicate enrollments; the N+1 script goes from 13 queries down to 1 query with identical results.

**Output Screenshots:**
**TASK-1**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/7f4d1281-3068-4d15-bbef-221b33798429" />
**TASK-2**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1008e7aa-8802-406b-bbb6-a01b82bdfbab" />
**TASK-3**
<img width="858" height="391" alt="image" src="https://github.com/user-attachments/assets/bb345729-6892-49bd-9f8a-cd8136fdb3fc" />

---

## Hands-On 5 — MongoDB: Document Modelling, CRUD & Aggregation

**Topics:** Documents & Collections · BSON Types · CRUD Operations · Aggregation Pipeline · Indexes in MongoDB · Embedding vs Referencing

Modelled a `college_nosql.feedback` collection (course feedback: ratings, comments, tags, attachments) and inserted 10+ documents, including one intentionally missing the `attachments` field to demonstrate MongoDB's schema-less design. Practiced all CRUD operations: filtering by rating, array/tag queries with `$elemMatch`, field projection, `updateMany` with `$set`/`$push`, and conditional deletes. Built a multi-stage **aggregation pipeline** (`$match` → `$group` → `$sort` → `$project` with `$round`) for average rating per course, plus a `$unwind`-based tag-frequency leaderboard, and verified index usage (`IXSCAN` vs `COLLSCAN`) via `.explain('executionStats')`.

**Expected Outcome:** `db.feedback.countDocuments()` ≥ 10; tag/array queries return only matching CS101 feedback; the aggregation pipeline returns one document per course with `average_rating` rounded to 1 decimal; the tag leaderboard surfaces `'challenging'` near the top.

**Output Screenshots:**

**TASK-1**
<img width="606" height="436" alt="image" src="https://github.com/user-attachments/assets/da592520-8a36-4cc2-bd38-5b6439603516" />

**TASK-2**
<img width="636" height="515" alt="image" src="https://github.com/user-attachments/assets/91320f5e-f4cf-4c29-977f-e1b6c16c6595" />

**TASK-3**

---

## Hands-On 6 — ORM Integration: SQLAlchemy

**Topics:** SQLAlchemy Core & ORM · Defining Models and Relationships · CRUD via ORM · Sessions and Connection Pooling · Avoiding N+1 with `joinedload`

Defined `Department`, `Student`, `Course`, `Enrollment`, and `Professor` ORM model classes in `models.py` mirroring the SQL schema, with `relationship()` mappings (many-to-one Student→Department, Enrollment→Student/Course), and auto-created tables in `college_db_orm` via `Base.metadata.create_all(engine)`. Performed full CRUD through a SQLAlchemy `Session` (`crud.py`) — inserts, filtered reads via `.join()`, updates, and deletes — enabling `echo=True` to reveal an N+1 query pattern on the enrollment/student/course read. Fixed it using `joinedload()` (dropping query count from 13 to 1).

**Expected Outcome:** `python models.py` creates all 5 tables in `college_db_orm`; CRUD operations commit/query correctly; `echo=True` logs confirm the N+1 pattern is eliminated after adding `joinedload`.

**Output Screenshots:**

**TASK-1**
<img width="820" height="630" alt="image" src="https://github.com/user-attachments/assets/b795eeb6-cb90-4982-a07a-9cb6f46ee167" />
<img width="811" height="265" alt="image" src="https://github.com/user-attachments/assets/ed03305b-c4b2-43b8-8d47-c00268ddee8d" />

**TASK-2**
<img width="698" height="521" alt="image" src="https://github.com/user-attachments/assets/b08e8dd3-81fe-4672-8c45-7535389b149e" />

**TASK-3**



---

## Hands-On 7 — Migrations & Versioning: Alembic

**Topics:** Migration Concepts · Alembic for SQLAlchemy · Migration History and Version Control · Rollback Strategies

Initialised Alembic (`alembic init migrations`), pointed it at `college_db_orm`, and generated a baseline migration via `--autogenerate`, applying it with `alembic upgrade head` and confirming the `alembic_version` table. Added incremental schema changes — an `is_active` column on `Student` and a new `CourseSchedule` table — each as its own autogenerated, inspected, and applied migration, then reviewed the full chain with `alembic history --verbose`. Practiced safe rollback: `alembic downgrade -1` (removes `is_active`), `alembic downgrade base` (removes all migrations), and re-applying with `alembic upgrade head` to confirm full recovery.

**Expected Outcome:** `alembic history` shows 3 revisions; `is_active` and `course_schedules` exist after upgrades; `downgrade -1` removes `is_active` and `upgrade head` restores it, matching the expected head hash.

**Output Screenshots:**

**TASK-1**
<img width="777" height="593" alt="image" src="https://github.com/user-attachments/assets/6bdd96fc-12c3-4cb6-9d6f-466c236425d9" />

**TASK-3**
<img width="916" height="642" alt="image" src="https://github.com/user-attachments/assets/ef83a1c6-fbe0-4b42-a672-069afbf2e184" />

---

## Summary

| Hands-On | Topic | Technology |
|---|---|---|
| 1 | Schema Design & Core SQL (DDL, Normalisation) | MySQL |
| 2 | DML, Joins & Aggregations | MySQL |
| 3 | Subqueries, Views & Transactions | MySQL |
| 4 | Query Optimisation — Indexes, EXPLAIN, N+1 | MySQL + Python |
| 5 | Document Modelling, CRUD & Aggregation | MongoDB |
| 6 | ORM Integration | SQLAlchemy (Python) |
| 7 | Migrations & Versioning | Alembic |

## Submitted By: NARRA RAMYA(212223040128)
