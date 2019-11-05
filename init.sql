use attendance_system;

create table if not exists student(
    roll_no INT AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    age INT NOT NULL,
    PRIMARY KEY (roll_no)
);

create table if not exists faculty(
    id INT AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL,
    age INT NOT NULL,
    PRIMARY KEY (id)
);

create table if not exists class(
    id INT references faculty(id),
    roll_no INT references student(roll_no),
    subject VARCHAR(20) NOT NULL
);


INSERT INTO student
(name    , age)
VALUES
('Rahul' , 15),
('Ram'   , 16),
('Shayam', 15),
('Jose'  , 17);

--select * from student;


INSERT INTO faculty
(name     , age)
VALUES
('Andrew' , 35),
('Mickale', 27),
('Kim'    , 32);

--select * from faculty;

INSERT INTO class
(id,roll_no,subject)
VALUES
(1 ,1, 'Machine Learning'),
(1, 2, 'Machine Learning'),
(1, 3, 'Machine Learning'),
(1, 4, 'Deep Learning'),
(3, 1, 'Python'),
(3, 4, 'Python'),
(2, 2, 'C++'),
(2, 3, 'OS'),
(2, 2, 'OS');

--select * from class;