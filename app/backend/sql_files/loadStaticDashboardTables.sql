INSERT INTO Users (id, name, email, role)
VALUES
    (-1, 'Anonymous/Unknown', '', ''),
    (0, 'Ryan', 'ryano3@umbc.edu', 'developer'),
    (1, 'Ava Johnson', 'avaj@umbc.edu', 'user'),
    (2, 'Marcus Lee', 'mlee2@umbc.edu', 'user'),
    (3, 'Sophia Patel', 'spatel4@umbc.edu', 'user'),
    (4, 'Daniel Kim', 'dkim7@umbc.edu', 'user');

INSERT INTO Departments (name, code, faculty_head, office_location)
VALUES
    ('Computer Science', 'CS', 'Dr. Mohamed Younis', 'ITE 325'),
    ('Chemistry', 'CHEM', 'Dr. Brian Cullum', 'MEYR 243B'),
    ('Physics', 'PHYS', 'Dr. Matthew Pelton', 'Physics 218'),
	('Mathematics & Statistics', 'MATH', 'Dr. Andrei Draganescu', 'MP 406'),
	('Biological Sciences', 'BIOL', 'Dr. Kevin Omland', 'BS 425'),
	('Philosophy', 'PHIL', 'Dr. Jessica Pfeifer', 'PAHB 452'),
	('Mechanical Engineering', 'MECH', 'Dr. Ruey-Hung Chen', 'ENG 210B'),
	('Information Systems', 'IS', 'Dr. Zhiyuan Chen', 'ITE 404G'),
	('Chemical, Biochemical & Environmental Engineering', 'CBEE', 'Dr. Mark R. Marten', 'ENG 314'),
	('History', 'HIST', 'Dr. Amy Froide', 'PAHB 217'),
	('Psychology', 'PSYC', 'Dr. Lira Yoon', 'MP 312'),
	('Sociology, Anthropology, and Public Health', 'SAPH', 'Dr. Andrea Kalfoglou', 'PUP 233');
    
INSERT INTO Room (type, number, capacity, description, wd_avblty_start, wd_avblty_end, sat_avblty_start, sat_avblty_end, sun_avblty_start, sun_avblty_end)
VALUES
    ('Group', '368', 4,
        'This room is available to UMBC students, faculty, and staff. It contains a small conference table and a smart TV with Chromecast, which allows a laptop, tablet or smartphone to stream content to the screen.',
        '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '257', 8,
        "This room has been set up for students to practice giving presentations, speeches, etc. Bring your flash drive to plug into our one-button recording system - when you're finished, you'll have a recording of your presentation to critique.",
        '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '258', 30,
        'Our Screening Room is designed for groups to view films. It is located on the 2nd floor of the library and fits up to 30 people.',
        '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', 'RLC Seminar Room', 6,
        'Contains a small conference table, large-screen monitor, and a projector with cables to connect to your laptop.',
        '00:00:00', '24:00:00', '00:00:00', '24:00:00', '00:00:00', '24:00:00'),
    ('Group', '210', 2, 'Small group study room with chalkboard.', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '211', 2, 'Small group study room with a whiteboard and a chalkboard.', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '212', 2, 'A small group study room.', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '213', 2, 'Small group study room with a chalkboard.', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '369', 2, 'Small group study room.', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '370', 2, 'Small group study room.', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '371', 2, 'Small group study room.', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '372', 2, 'Small group study room.', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '373', 2, 'Small group study room', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '374', 2, 'Small group study room with chalkboard.', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '453', 4, 'Small group study room with a whiteboard.', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '454', 4, 'Small group study room with computer.', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '456', 4, 'Small group study room with a computer', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Group', '457', 4, 'Small group study room with a computer', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Individual', '204', 1, '', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Individual', '205', 1, '', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Individual', '206', 1, 'Study room with seating for one', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Individual', '207', 1, 'Study room with seating for one', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Individual', '208', 1, 'Study room with seating for one', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Individual', '209', 1, 'Study room with seating for one', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Individual', '231', 1, 'Study room with seating for one', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00'),
    ('Individual', '232', 1, 'Study room with seating for one', '08:00:00', '22:00:00', '10:00:00', '17:00:00', '12:00:00', '22:00:00');

INSERT INTO BookLocator (title, author, isbn, shelf_location, availability_status)
VALUES
	('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 'FIC-FITZ-001', 'Available'),
	('A Brief History of Time', 'Stephen Hawking', '9780553380163', 'SCI-HAWK-502', 'Checked Out'),
	('Thinking, Fast and Slow', 'Daniel Kahneman', '9780374275631', 'PSY-KAHN-212', 'Available'),
	('The Immortal Life of Henrietta Lacks', 'Rebecca Skloot', '9781400052189', 'BIO-SKLO-109', 'Available'),
	('The 7 Habits of Highly Effective People', 'Stephen R. Covey', '9781982137274', 'SELF-COVE-881', 'Available'),
	('Educated', 'Tara Westover', '9780399590504', 'MEM-WEST-304', 'Checked Out'),
	('The Silent Patient', 'Alex Michaelides', '9781250301697', 'MYS-MICH-442', 'Available'),
	('Atomic Habits', 'James Clear', '9780735211292', 'SELF-CLEA-773', 'Available'),
	('The Overstory', 'Richard Powers', '9780393356687', 'FIC-POWE-115', 'Available'),
	('Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', '9780062316097', 'HIST-HARA-601', 'Checked Out'),
	('Project Hail Mary', 'Andy Weir', '9780593135204', 'SCI-WEIR-902', 'Available'),
	('Killers of the Flower Moon', 'David Grann', '9780385534246', 'NF-GRAN-127', 'Available'),
	('The Body Keeps the Score', 'Bessel van der Kolk', '9780143127741', 'MED-KOLK-554', 'Available'),
	('Circe', 'Madeline Miller', '9780316556347', 'MYTH-MILL-219', 'Checked Out'),
	('Quiet: The Power of Introverts', 'Susan Cain', '9780307352156', 'PSY-CAIN-332', 'Available');

INSERT INTO Printer (name, location, model, curr_status, toner_level, paper_level, last_maintenance)
VALUES
    ('Printer A', 'First Floor - Lobby', 'HP LaserJet Pro 4001', 'Available', 82, 76, '2026-03-15'),
    ('Printer B', 'First Floor - Study Area', 'Canon imageCLASS MF455dw', 'Busy', 64, 52, '2026-03-10'),
    ('Printer C', 'Second Floor - Computer Lab', 'Brother HL-L6415DW', 'Available', 91, 88, '2026-03-20'),
    ('Printer D', 'Second Floor - Quiet Zone', 'Xerox B315', 'Maintenance', 20, 34, '2026-03-28'),
    ('Printer E', 'Third Floor - Admin Office', 'Lexmark MS431dn', 'Offline', 48, 15, '2026-03-05');

INSERT INTO PrinterUsage (pages_printed, print_time, job_status, printer_id)
VALUES
    (3,  '2026-03-30 09:15:00', 'Completed', 1),
    (12, '2026-03-30 10:05:00', 'Completed', 2),
    (7,  '2026-03-30 11:20:00', 'Completed', 3),
    (20, '2026-03-30 13:45:00', 'Completed', 1),
    (5,  '2026-03-30 15:10:00', 'Completed', 2),
    (18, '2026-03-31 08:30:00', 'Completed', 3),
    (9,  '2026-03-31 09:40:00', 'Completed', 1),
    (15, '2026-03-31 11:00:00', 'Completed', 2),
    (4,  '2026-03-31 12:25:00', 'Completed', 3),
    (11, '2026-03-31 14:50:00', 'Queued', 4),
    (6,  '2026-03-31 16:05:00', 'Failed', 5),
    (14, '2026-03-31 17:40:00', 'Completed', 1);


INSERT INTO LibraryEntryLog (entry_time, entry_count)
VALUES
    
    ('2026-04-07 08:00:00', 34),
    ('2026-04-07 09:00:00', 52),
    ('2026-04-07 10:00:00', 46),
    ('2026-04-07 11:00:00', 38),
    ('2026-04-07 12:00:00', 27),
    ('2026-04-07 13:00:00', 24),
    ('2026-04-07 14:00:00', 26),
    ('2026-04-07 15:00:00', 31),
    ('2026-04-07 16:00:00', 39),
    ('2026-04-07 17:00:00', 42),
    ('2026-04-07 18:00:00', 33),
    ('2026-04-07 19:00:00', 24),

  
    ('2026-04-08 08:00:00', 16),
    ('2026-04-08 09:00:00', 24),
    ('2026-04-08 10:00:00', 33),
    ('2026-04-08 11:00:00', 41),
    ('2026-04-08 12:00:00', 47),
    ('2026-04-08 13:00:00', 49),
    ('2026-04-08 14:00:00', 46),
    ('2026-04-08 15:00:00', 42),
    ('2026-04-08 16:00:00', 36),
    ('2026-04-08 17:00:00', 31),
    ('2026-04-08 18:00:00', 24),
    ('2026-04-08 19:00:00', 18),

 
    ('2026-04-09 08:00:00', 18),
    ('2026-04-09 09:00:00', 29),
    ('2026-04-09 10:00:00', 44),
    ('2026-04-09 11:00:00', 61),
    ('2026-04-09 12:00:00', 58),
    ('2026-04-09 13:00:00', 47),
    ('2026-04-09 14:00:00', 39),
    ('2026-04-09 15:00:00', 32),
    ('2026-04-09 16:00:00', 27),
    ('2026-04-09 17:00:00', 24),
    ('2026-04-09 18:00:00', 22),
    ('2026-04-09 19:00:00', 19),

 
    ('2026-04-10 08:00:00', 24),
    ('2026-04-10 09:00:00', 31),
    ('2026-04-10 10:00:00', 35),
    ('2026-04-10 11:00:00', 37),
    ('2026-04-10 12:00:00', 39),
    ('2026-04-10 13:00:00', 38),
    ('2026-04-10 14:00:00', 36),
    ('2026-04-10 15:00:00', 35),
    ('2026-04-10 16:00:00', 34),
    ('2026-04-10 17:00:00', 32),
    ('2026-04-10 18:00:00', 28),
    ('2026-04-10 19:00:00', 23),

   
    ('2026-04-11 08:00:00', 32),
    ('2026-04-11 09:00:00', 46),
    ('2026-04-11 10:00:00', 43),
    ('2026-04-11 11:00:00', 37),
    ('2026-04-11 12:00:00', 34),
    ('2026-04-11 13:00:00', 29),
    ('2026-04-11 14:00:00', 24),
    ('2026-04-11 15:00:00', 19),
    ('2026-04-11 16:00:00', 16),
    ('2026-04-11 17:00:00', 14),
    ('2026-04-11 18:00:00', 11),
    ('2026-04-11 19:00:00', 8),

    
    ('2026-04-12 08:00:00', 6),
    ('2026-04-12 09:00:00', 10),
    ('2026-04-12 10:00:00', 18),
    ('2026-04-12 11:00:00', 27),
    ('2026-04-12 12:00:00', 36),
    ('2026-04-12 13:00:00', 44),
    ('2026-04-12 14:00:00', 47),
    ('2026-04-12 15:00:00', 41),
    ('2026-04-12 16:00:00', 32),
    ('2026-04-12 17:00:00', 24),
    ('2026-04-12 18:00:00', 18),
    ('2026-04-12 19:00:00', 12),

 
    ('2026-04-13 08:00:00', 5),
    ('2026-04-13 09:00:00', 8),
    ('2026-04-13 10:00:00', 14),
    ('2026-04-13 11:00:00', 22),
    ('2026-04-13 12:00:00', 29),
    ('2026-04-13 13:00:00', 34),
    ('2026-04-13 14:00:00', 37),
    ('2026-04-13 15:00:00', 39),
    ('2026-04-13 16:00:00', 38),
    ('2026-04-13 17:00:00', 35),
    ('2026-04-13 18:00:00', 29),
    ('2026-04-13 19:00:00', 21);