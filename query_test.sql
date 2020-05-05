
CREATE TABLE dbjudge_database(
    name varchar(20) NOT NULL,
    PRIMARY KEY (name)
);
CREATE TABLE dbjudge_fake_data(
    data text,
    fake_type varchar(20),
    PRIMARY KEY (data)
);
CREATE TABLE dbjudge_question(
    id integer,
    question text,
    sql_query text,
    PRIMARY KEY (id)
);
