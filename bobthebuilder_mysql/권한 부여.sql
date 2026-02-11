drop user bob@localhost;
create user "bob"@"localhost"IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON bob.* TO 'bob'@'localhost';
flush privileges