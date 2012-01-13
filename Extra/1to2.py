BEGIN;

CREATE TABLE `server_course_manager` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `course_id` integer NOT NULL,
    `user_id` integer NOT NULL,
    UNIQUE (`course_id`, `user_id`)
)
;
ALTER TABLE `server_course_manager` ADD CONSTRAINT `user_id_refs_id_416f8a7e` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `server_course` ADD(
   
    `course_category` integer NOT NULL,
)
;
ALTER TABLE `server_course_manager` ADD CONSTRAINT `course_id_refs_id_30241921` FOREIGN KEY (`course_id`) REFERENCES `server_course` (`id`);
CREATE TABLE `Server_profile_teach_courses` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `profile_id` integer NOT NULL,
    `course_id` integer NOT NULL,
    UNIQUE (`profile_id`, `course_id`)
)
;
ALTER TABLE `Server_profile_teach_courses` ADD CONSTRAINT `course_id_refs_id_a5bb99c3` FOREIGN KEY (`course_id`) REFERENCES `server_course` (`id`);
ALTER TABLE `Server_profile` ADD(
    `user_type` integer NOT NULL,
)
;
ALTER TABLE `Server_profile_teach_courses` ADD CONSTRAINT `profile_id_refs_id_699bbbb6` FOREIGN KEY (`profile_id`) REFERENCES `Server_profile` (`id`);
CREATE TABLE `Server_assignment` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `content` varchar(755) NOT NULL,
    `deadline` datetime,
    `tocourse_id` integer NOT NULL
)
;
ALTER TABLE `Server_assignment` ADD CONSTRAINT `tocourse_id_refs_id_6baef9b1` FOREIGN KEY (`tocourse_id`) REFERENCES `server_course` (`id`);
CREATE TABLE `Server_comment` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `timestamp` datetime NOT NULL,
    `content` longtext NOT NULL,
    `course_id` integer,
    `place_id` varchar(20),
    `user_id` integer,
    `sendername` varchar(255) NOT NULL
)
;
ALTER TABLE `Server_comment` ADD CONSTRAINT `course_id_refs_id_20c4f548` FOREIGN KEY (`course_id`) REFERENCES `server_course` (`id`);
ALTER TABLE `Server_comment` ADD CONSTRAINT `user_id_refs_id_fa74e119` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `Server_comment` ADD CONSTRAINT `place_id_refs_keyid_eb825b8f` FOREIGN KEY (`place_id`) REFERENCES `Server_place` (`keyid`);
CREATE TABLE `Server_sms_touser` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `sms_id` integer NOT NULL,
    `user_id` integer NOT NULL,
    UNIQUE (`sms_id`, `user_id`)
)
;
ALTER TABLE `Server_sms_touser` ADD CONSTRAINT `user_id_refs_id_dae5ee39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `Server_sms` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `title` varchar(255),
    `content` longtext NOT NULL,
    `sendfrom_id` integer NOT NULL,
    `sendername` varchar(255) NOT NULL,
    `timestamp` datetime NOT NULL,
    `state` bool NOT NULL
)
;
ALTER TABLE `Server_sms` ADD CONSTRAINT `sendfrom_id_refs_id_c9dcd843` FOREIGN KEY (`sendfrom_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `Server_sms_touser` ADD CONSTRAINT `sms_id_refs_id_ae89cb77` FOREIGN KEY (`sms_id`) REFERENCES `Server_sms` (`id`);
CREATE TABLE `Server_sys_notice` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `title` varchar(255),
    `content` longtext NOT NULL,
    `sendername` varchar(255) NOT NULL,
    `timestamp` datetime NOT NULL
)
;
CREATE TABLE `Server_reply` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `tocomment_id` integer NOT NULL,
    `toreply` longtext,
    `touser_id` integer NOT NULL,
    `sendfrom_id` integer NOT NULL,
    `sendername` varchar(255) NOT NULL,
    `content` longtext NOT NULL,
    `timestamp` datetime NOT NULL
)
;
ALTER TABLE `Server_reply` ADD CONSTRAINT `tocomment_id_refs_id_13d678b0` FOREIGN KEY (`tocomment_id`) REFERENCES `Server_comment` (`id`);
ALTER TABLE `Server_reply` ADD CONSTRAINT `touser_id_refs_id_5168e13c` FOREIGN KEY (`touser_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `Server_reply` ADD CONSTRAINT `sendfrom_id_refs_id_5168e13c` FOREIGN KEY (`sendfrom_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `Server_notice` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `touser_id` integer NOT NULL,
    `obj_id` integer NOT NULL,
    `state` bool NOT NULL,
    `sendername` varchar(255) NOT NULL,
    `ntype` integer NOT NULL
)
;
COMMIT;

