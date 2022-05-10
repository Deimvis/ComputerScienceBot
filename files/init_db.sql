CREATE DATABASE IF NOT EXISTS `computer_science_bot`;
USE `computer_science_bot`;
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
CREATE TABLE IF NOT EXISTS source (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_title VARCHAR(128) NOT NULL,
    url VARCHAR(4096) NOT NULL,
    title VARCHAR(128),
    description TEXT,
    `rank` INT,
    language VARCHAR(32),
    FOREIGN KEY (course_title)
        REFERENCES course (title)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
CREATE TABLE IF NOT EXISTS test_unit (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_title VARCHAR(128),
    purpose VARCHAR(512) NOT NULL,
    difficulty VARCHAR(512),
    question TEXT NOT NULL,
    options TEXT NOT NULL COMMENT 'Json list',
    answer_ind INT NOT NULL,
    explanation VARCHAR(512),
    FOREIGN KEY (course_title)
        REFERENCES course (title)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
CREATE TABLE IF NOT EXISTS user_completed_test_unit (
    chat_id BIGINT,
    test_unit_id INT,
    course_title VARCHAR(128),
    purpose VARCHAR(512) NOT NULL,
    difficulty VARCHAR(512),
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
    chat_id BIGINT,
    course_title VARCHAR(128),
    ts BIGINT NOT NULL,
    FOREIGN KEY (course_title)
        REFERENCES course (title)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
CREATE TABLE IF NOT EXISTS user_action (
    chat_id BIGINT,
    callback_data VARCHAR(512),
    message VARCHAR(512),
    ts BIGINT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
INSERT INTO course (title, description)
VALUES
    ('algorithms', 'Algorithms and data structures'),
    ('python', 'Python basics')
ON DUPLICATE KEY UPDATE
    description = VALUES(description);
