CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    role VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE,
    faculty_head VARCHAR(100),
    office_location VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Room (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(50) NOT NULL,
    number VARCHAR(100),
    capacity INT,
    description VARCHAR(250),
    wd_avblty_start TIME,
    wd_avblty_end TIME,
    sat_avblty_start TIME,
    sat_avblty_end TIME,
    sun_avblty_start TIME,
    sun_avblty_end TIME
);

CREATE TABLE IF NOT EXISTS RoomReservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name VARCHAR(50),
    room_id INT NOT NULL,
    start_dt DATETIME NOT NULL,
    end_dt DATETIME NOT NULL,
    request_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_canceled INT DEFAULT 0,
    UNIQUE(room_id, start_dt),
    FOREIGN KEY (room_id) REFERENCES Room(id)
);

CREATE TABLE IF NOT EXISTS BookLocator (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(100),
    isbn VARCHAR(20) UNIQUE,
    shelf_location VARCHAR(50),
    availability_status VARCHAR(20) DEFAULT 'available'
);

CREATE TABLE IF NOT EXISTS Printer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    location VARCHAR(100),
    model VARCHAR(100),
    curr_status VARCHAR(30) DEFAULT 'available',
    toner_level INT,
    paper_level INT,
    last_maintenance DATE
);

CREATE TABLE IF NOT EXISTS PrinterUsage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pages_printed INT NOT NULL,
    print_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    job_status VARCHAR(30) DEFAULT 'Completed',
    printer_id INT NOT NULL,
    FOREIGN KEY (printer_id) REFERENCES Printer(id)
);

CREATE TABLE IF NOT EXISTS LibraryEntryLog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_time DATETIME NOT NULL,
    entry_count INT NOT NULL
);

CREATE TABLE IF NOT EXISTS FeedbackForms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(30) DEFAULT 'bug report',
    content VARCHAR(1000) NOT NULL,
    submission_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE IF NOT EXISTS TableMetadata (
    table_name PRIMARY KEY,
    last_modified DATETIME
);