DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS manager;
DROP TABLE IF EXISTS managerproject;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS employeetask;
DROP TABLE IF EXISTS task;

CREATE TABLE project
(
    id   INTEGER AUTO_INCREMENT PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL
);

CREATE TABLE manager (
    id            INTEGER AUTO_INCREMENT PRIMARY KEY,
    NAME          VARCHAR(100) NOT NULL,
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
    NAME VARCHAR(100) NOT NULL
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
    NAME       VARCHAR(100)                       NOT NULL,
    start_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    end_date   DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);


DROP VIEW IF EXISTS projectview;
CREATE VIEW projectview AS
    SELECT
        p.*,
        min(t.start_date) AS start_date,
        max(t.end_date)   AS end_date
    FROM project p
        LEFT JOIN task t ON p.id = t.project_id
    GROUP BY p.id;


DROP VIEW IF EXISTS busyemployees;
CREATE VIEW busyemployees
    AS
        SELECT
            e.*,
            EXISTS(
                SELECT *
                FROM employeetask et, task t
                WHERE et.employee_id = e.id
                      AND et.task_id = t.id
                      AND t.start_date < now()
                      AND t.end_date > now()
            ) AS busy_today
        FROM employee e;


DROP VIEW IF EXISTS ManagerView;
CREATE VIEW ManagerView AS
    SELECT
        m.*,
        COUNT(mp.project_id) AS assigned_projects
    FROM manager m
        LEFT JOIN managerproject mp ON mp.manager_id = m.id
    GROUP BY m.id;

DROP TRIGGER IF EXISTS assign_new_project_to_free_manager;
CREATE TRIGGER assign_new_project_to_free_manager
    AFTER INSERT
    ON project
    FOR EACH ROW
    BEGIN
        INSERT INTO managerproject (manager_id, project_id)
            SELECT
                mv.id,
                new.ID
            FROM ManagerView mv
            ORDER BY assigned_projects ASC
            LIMIT 1;
    END;

DROP TRIGGER IF EXISTS delete_task_assignments_on_employee_delete;
CREATE TRIGGER delete_task_assignments_on_employee_delete
    AFTER DELETE
    ON employee
    FOR EACH ROW
    BEGIN
        DELETE FROM employeetask
        WHERE employee_id = OLD.id;
    END;

DROP TRIGGER IF EXISTS delete_employee_assignments_on_task_delete;
CREATE TRIGGER delete_employee_assignments_on_task_delete
    AFTER DELETE
    ON task
    FOR EACH ROW
    BEGIN
        DELETE FROM employeetask
        WHERE task_id = OLD.id;
    END;


DROP TRIGGER IF EXISTS delete_project_assignments_on_manager_delete;
CREATE TRIGGER delete_project_assignments_on_manager_delete
    AFTER DELETE
    ON manager
    FOR EACH ROW
    BEGIN
        DELETE FROM managerproject
        WHERE manager_id = OLD.id;
    END;


DROP TRIGGER IF EXISTS delete_manager_assignments_on_project_delete;
CREATE TRIGGER delete_manager_assignments_on_project_delete
    AFTER DELETE
    ON project
    FOR EACH ROW
    BEGIN
        DELETE FROM managerproject
        WHERE project_id = OLD.id;
    END;


DROP PROCEDURE IF EXISTS completed_projects;
CREATE PROCEDURE completed_projects(manager_id VARCHAR(10))
    BEGIN
        IF manager_id = 'ALL'
        THEN
            SELECT *
            FROM projectview
            WHERE end_date < now();
        ELSE
            SELECT *
            FROM managerproject mp
                LEFT JOIN projectview pv ON mp.project_id = pv.id
            WHERE pv.end_date < now()
                  AND mp.manager_id = manager_id;
        END IF;
    END;

DROP PROCEDURE IF EXISTS incomplete_projects;
CREATE PROCEDURE incomplete_projects(manager_id VARCHAR(10))
    BEGIN
        IF manager_id = 'ALL'
        THEN
            SELECT *
            FROM projectview
            WHERE end_date > now() OR end_date IS NULL;
        ELSE
            SELECT *
            FROM managerproject mp
                LEFT JOIN projectview pv ON mp.project_id = pv.id
            WHERE (pv.end_date > now() OR pv.end_date IS NULL)
                  AND mp.manager_id = manager_id;
        END IF;
    END;