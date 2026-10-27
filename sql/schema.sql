
CREATE DATABASE IF NOT EXISTS csc370_project;

USE csc370_project;

CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    major VARCHAR(100)
);

INSERT INTO Students (student_id, name, major)
VALUES
    (1, 'Alice', 'Computer Science'),
    (2, 'Bob', 'Mathematics'),
    (3, 'Charlie', 'Engineering');

SELECT * FROM Students;
