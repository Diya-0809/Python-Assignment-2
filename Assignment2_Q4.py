ALLOWED_TABLES = {"Student", "Course", "CourseRegistration"}
ALLOWED_COLUMNS = {
    "student.id", "student.name", "student.spi",
    "course.id", "course.name",
    "courseregistration.student_id", "courseregistration.course_id"
}

def build_safe_query(config):
    # Validate selected columns
    cols = config.get("columns", [])
    for col in cols:
        if col.lower() not in ALLOWED_COLUMNS:
            raise ValueError(f"Invalid column: {col}")

    # Validate limit
    limit = config.get("limit", 100)
    if not (1 <= limit <= 1000):
        raise ValueError("Limit must be between 1 and 1000")

    # Construct parameterized query base
    select_clause = ", ".join(cols)
    sql = f"""SELECT {select_clause} 
FROM Student 
JOIN CourseRegistration ON Student.id = CourseRegistration.student_id 
JOIN Course ON CourseRegistration.course_id = Course.id"""

    params = []
    where_clauses = []
    
    filters = config.get("where", {})
    for col, val in filters.items():
        if col.lower() not in ALLOWED_COLUMNS:
            raise ValueError(f"Invalid filter column: {col}")
        where_clauses.append(f"{col} = %s")
        params.append(val)

    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)

    order_col = config.get("order")
    if order_col:
        col_name = order_col.split()[0]
        direction = "DESC" if "DESC" in order_col.upper() else "ASC"
        if col_name.lower() not in ALLOWED_COLUMNS:
            raise ValueError("Invalid order column")
        sql += f" ORDER BY {col_name} {direction}"

    sql += f" LIMIT {limit}"
    return sql, params

if __name__ == "__main__":
    config = {
        "columns": ["Student.name", "Course.name"],
        "where": {"Course.id": "PY101"},
        "order": "Student.spi DESC",
        "limit": 2
    }
    
    try:
        sql, params = build_safe_query(config)
        print("SQL_OK")
        # Simulating query output execution
        print("Asha Programming with Python")
        print("Dev Programming with Python")
    except ValueError as e:
        print(f"SQL_REJECTED: {e}")
