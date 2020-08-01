CREATE TABLE `pos` (
	`idx` INT(10) NOT NULL AUTO_INCREMENT,
	`value` VARCHAR(15) NOT NULL,
	PRIMARY KEY (`idx`)
	);

INSERT INTO `pos` (`value`) VALUES
	('adjective'),
	('adverb'),
	('applicative'),
	('conjunction'),
	('demonstrative'),
	('interjection'),
	('noun'),
	('verb'),
	('pronoun');

CREATE TABLE `sources` (
	`idx` INT(10) NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(50) NOT NULL,
	PRIMARY KEY (`idx`)
	);

CREATE TABLE `lemmata` (
	`idx` INT(15) NOT NULL AUTO_INCREMENT,
	`lemma` VARCHAR(15) NOT NULL,
	`pos` INT(10) NOT NULL,
	`source` INT(10),
	PRIMARY KEY (`idx`),
	FOREIGN KEY (`pos`)
	REFERENCES `pos`(`idx`),
	FOREIGN KEY (`source`)
	REFERENCES `sources`(`idx`)
	);

