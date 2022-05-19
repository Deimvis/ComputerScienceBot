CREATE DATABASE IF NOT EXISTS `{{ DB_NAME }}`;
USE `{{ DB_NAME }}`;
CREATE TABLE IF NOT EXISTS user (
    chat_id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    ts BIGINT
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
CREATE TABLE IF NOT EXISTS course (
    title VARCHAR(128) PRIMARY KEY,
    description VARCHAR(512)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
CREATE TABLE IF NOT EXISTS course_prerequisite (
    title VARCHAR(128),
    prerequisite VARCHAR(128),
    UNIQUE KEY (title, prerequisite),
    FOREIGN KEY (title)
        REFERENCES course (title)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    FOREIGN KEY (prerequisite)
        REFERENCES course (title)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
CREATE TABLE IF NOT EXISTS source (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_title VARCHAR(128) NOT NULL,
    url VARCHAR(4096) NOT NULL,
    title VARCHAR(128) NOT NULL,
    author VARCHAR(128),
    year INT,
    description TEXT,
    `rank` INT DEFAULT 8 NOT NULL,
    language ENUM('RU', 'EN'),
    platform VARCHAR(128),
    FOREIGN KEY (course_title)
        REFERENCES course (title)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
CREATE TABLE IF NOT EXISTS test_unit (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_title VARCHAR(128),
    purpose ENUM('study', 'compete') NOT NULL,
    difficulty VARCHAR(128),
    question TEXT NOT NULL,
    options TEXT NOT NULL COMMENT 'Json list',
    answer_ind INT NOT NULL,
    explanation VARCHAR(128),
    shuffle_options BOOL DEFAULT True NOT NULL,
    has_picture BOOLEAN DEFAULT FALSE NOT NULL,
    picture LONGBLOB,
    FOREIGN KEY (course_title)
        REFERENCES course (title)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
CREATE TABLE IF NOT EXISTS user_completed_test_unit (
    chat_id BIGINT NOT NULL,
    test_unit_id INT,
    course_title VARCHAR(128),
    purpose ENUM('study', 'compete') NOT NULL,
    difficulty VARCHAR(128),
    is_answer_correct BOOLEAN NOT NULL,
    ts BIGINT NOT NULL,
    FOREIGN KEY (test_unit_id)
        REFERENCES test_unit (id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    FOREIGN KEY (course_title)
        REFERENCES course (title)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
CREATE TABLE IF NOT EXISTS user_completed_course (
    chat_id BIGINT NOT NULL,
    course_title VARCHAR(128),
    ts BIGINT NOT NULL,
    FOREIGN KEY (course_title)
        REFERENCES course (title)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
CREATE TABLE IF NOT EXISTS user_action (
    chat_id BIGINT NOT NULL,
    callback_data VARCHAR(512),
    message VARCHAR(512),
    ts BIGINT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
INSERT INTO course (title, description)
VALUES
    ('algorithms', 'Algorithms and data structures'),
    ('algorithms_2', 'Algorithms and data structures - 2'),
    ('calculus', 'Calculus'),
    ('cpp', 'C++'),
    ('discrete_math', 'Discrete mathematics'),
    ('introduction_to_cs', 'Introduction to Computer Science'),
    ('linear_algebra', 'Linear algebra'),
    ('python', 'Python basics')
ON DUPLICATE KEY UPDATE
    description = VALUES(description);
INSERT INTO course_prerequisite (title, prerequisite) VALUES
    ('algorithms', 'python'),
    ('cpp', 'python'),
    ('algorithms_2', 'algorithms'),
    ('algorithms_2', 'discrete_math')
ON DUPLICATE KEY UPDATE
    title=title; # on duplicate key do nothing
