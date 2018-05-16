CREATE TABLE project
(
    id   INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE manager (
    id            INTEGER AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    password_hash CHAR(255)    NOT NULL
);

CREATE TABLE managerproject (
    manager_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    PRIMARY KEY (manager_id, project_id)
);

CREATE TABLE employee
(
    id   INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE employeetask
(
    employee_id INTEGER NOT NULL,
    task_id     INTEGER NOT NULL,
    PRIMARY KEY (employee_id, task_id)
);

CREATE TABLE task
(
    id         INTEGER AUTO_INCREMENT PRIMARY KEY,
    project_id INTEGER                            NOT NULL,
    name       VARCHAR(100)                       NOT NULL,
    start_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    end_date   DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);


DROP VIEW projectview;
CREATE VIEW projectview AS
    SELECT
        p.*,
        min(t.start_date) AS start_date,
        max(t.end_date)   AS end_date
    FROM projector.project p
        JOIN projector.task t
    WHERE (t.project_id = p.id)
    GROUP BY p.id;


DROP VIEW busyemployees;
CREATE VIEW busyemployees
    AS
        SELECT
            e.*,
            exists(
                SELECT *
                FROM employeetask et, task t
                WHERE et.employee_id = e.id
                      AND et.task_id = t.id
                      AND t.start_date < now()
                      AND t.end_date > now()
            ) AS busy_today
        FROM employee e;