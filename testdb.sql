PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE blogs (
	id INTEGER NOT NULL, 
	title VARCHAR, 
	content VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO blogs VALUES(1,'first blog by shibu','shibu wrote this and tried sqlite');
INSERT INTO blogs VALUES(2,'second blog by shibu','shibu wrote this and tried id number');
CREATE INDEX ix_blogs_id ON blogs (id);
CREATE INDEX ix_blogs_title ON blogs (title);
COMMIT;
