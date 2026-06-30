"""
HANDS-ON 4, Task 3: N+1 Query Problem demonstration.
"""

import time
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="009700",
    database="college_db"
)

def n_plus_one_version():
    cursor = conn.cursor()
    query_count = 0

    cursor.execute("SELECT enrollment_id, student_id, course_id FROM enrollments")
    query_count += 1
    enrollments = cursor.fetchall()

    results = []
    for enr in enrollments:
        student_id = enr[1]
        cursor.execute(
            "SELECT first_name, last_name FROM students WHERE student_id = %s",
            (student_id,)
        )
        query_count += 1
        student = cursor.fetchone()
        results.append((enr, student))

    cursor.close()
    print(f"N+1 version: {query_count} queries executed")
    return results, query_count


def joined_version():
    cursor = conn.cursor()
    query_count = 0

    cursor.execute("""
        SELECT e.enrollment_id, e.student_id, e.course_id,
               s.first_name, s.last_name
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
    """)
    query_count += 1
    results = cursor.fetchall()

    cursor.close()
    print(f"JOIN version: {query_count} query executed")
    return results, query_count


if __name__ == "__main__":
    start1 = time.time()
    results1, count1 = n_plus_one_version()
    time1 = time.time() - start1

    start2 = time.time()
    results2, count2 = joined_version()
    time2 = time.time() - start2

    print(f"\nN+1 version: {count1} queries, {time1:.4f}s")
    print(f"JOIN version: {count2} queries, {time2:.4f}s")
    print(f"Query reduction: {count1 - count2} fewer queries with JOIN")

conn.close()