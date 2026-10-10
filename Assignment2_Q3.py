import csv
import mysql.connector

def run_analytics(db_config, student_csv, reg_csv, course_id, spi_threshold):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Create Tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student (
            student_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100),
            spi FLOAT
        );
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS CourseRegistration (
            reg_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id VARCHAR(50),
            course_id VARCHAR(50),
            FOREIGN KEY (student_id) REFERENCES Student(student_id)
        );
        """)

        # Insert Students
        with open(student_csv, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)
            student_data = [(row[0], row[1], float(row[2])) for row in reader if row]
            cursor.executemany("INSERT IGNORE INTO Student VALUES (%s, %s, %s)", student_data)

        # Insert Registrations
        with open(reg_csv, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)
            reg_data = [(row[0], row[1]) for row in reader if row]
            cursor.executemany("INSERT INTO CourseRegistration (student_id, course_id) VALUES (%s, %s)", reg_data)

        conn.commit()

        # Parameterized Analytics Query
        query = """
        SELECT s.student_id, s.name, s.spi, r.course_id
        FROM Student s
        JOIN CourseRegistration r ON s.student_id = r.student_id
        WHERE r.course_id = %s AND s.spi > %s
        ORDER BY s.spi DESC, s.student_id ASC;
        """
        cursor.execute(query, (course_id, spi_threshold))

        for sid, name, spi, cid in cursor.fetchall():
            print(f"{sid} {name} {spi} {cid}")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    # Config template
    db_config = {'host': 'localhost', 'user': 'root', 'password': 'password', 'database': 'university'}
    # Example execution call:
    # run_analytics(db_config, 'student.csv', 'registration.csv', 'PY101', 8.0)
