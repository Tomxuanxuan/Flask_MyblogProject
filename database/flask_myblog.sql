/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 50724
 Source Host           : localhost:3306
 Source Schema         : flask_myblog

 Target Server Type    : MySQL
 Target Server Version : 50724
 File Encoding         : 65001

 Date: 25/02/2019 09:32:31
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article`  (
  `article_id` int(11) NOT NULL AUTO_INCREMENT,
  `auther` int(11) NULL DEFAULT NULL,
  `title` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `article_img` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `brief` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `publish_time` datetime(0) NULL DEFAULT NULL,
  `label_id` int(11) NULL DEFAULT NULL,
  `read_quantity` int(11) NULL DEFAULT NULL,
  `like_number` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`article_id`) USING BTREE,
  INDEX `auther`(`auther`) USING BTREE,
  INDEX `label_id`(`label_id`) USING BTREE,
  CONSTRAINT `article_ibfk_1` FOREIGN KEY (`auther`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `article_ibfk_2` FOREIGN KEY (`label_id`) REFERENCES `label` (`label_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for atten_user
-- ----------------------------
DROP TABLE IF EXISTS `atten_user`;
CREATE TABLE `atten_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `atten_user_id` int(11) NOT NULL,
  `atten_auther` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `atten_user_id`(`atten_user_id`) USING BTREE,
  INDEX `atten_auther`(`atten_auther`) USING BTREE,
  CONSTRAINT `atten_user_ibfk_1` FOREIGN KEY (`atten_user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `atten_user_ibfk_2` FOREIGN KEY (`atten_auther`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for collect_article
-- ----------------------------
DROP TABLE IF EXISTS `collect_article`;
CREATE TABLE `collect_article`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `collect_article_id` int(11) NULL DEFAULT NULL,
  `collect_user_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `collect_article_id`(`collect_article_id`) USING BTREE,
  INDEX `collect_user_id`(`collect_user_id`) USING BTREE,
  CONSTRAINT `collect_article_ibfk_1` FOREIGN KEY (`collect_article_id`) REFERENCES `article` (`article_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `collect_article_ibfk_2` FOREIGN KEY (`collect_user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment_article_id` int(11) NOT NULL,
  `comment_user_id` int(11) NOT NULL,
  `comment_content` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `comment_time` datetime(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `comment_article_id`(`comment_article_id`) USING BTREE,
  INDEX `comment_user_id`(`comment_user_id`) USING BTREE,
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`comment_article_id`) REFERENCES `article` (`article_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`comment_user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for label
-- ----------------------------
DROP TABLE IF EXISTS `label`;
CREATE TABLE `label`  (
  `label_id` int(11) NOT NULL AUTO_INCREMENT,
  `label_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`label_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `messager` int(11) NOT NULL,
  `messager_other` int(11) NOT NULL,
  `message_time` datetime(0) NOT NULL,
  `message_content` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `messager`(`messager`) USING BTREE,
  INDEX `messager_other`(`messager_other`) USING BTREE,
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`messager`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `message_ibfk_2` FOREIGN KEY (`messager_other`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of message
-- ----------------------------
INSERT INTO `message` VALUES (1, 1, 4, '2019-02-24 16:09:55', '你好zy2，我是zy');
INSERT INTO `message` VALUES (2, 1, 4, '2019-02-24 16:09:55', '你好zy2，我是zy');
INSERT INTO `message` VALUES (3, 1, 4, '2019-02-24 16:09:55', '你好zy2，我是zy');
INSERT INTO `message` VALUES (4, 1, 4, '2019-02-24 16:09:55', '你好zy2，我是zy');

-- ----------------------------
-- Table structure for resource
-- ----------------------------
DROP TABLE IF EXISTS `resource`;
CREATE TABLE `resource`  (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `rname` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `fname` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `rsize` int(11) NULL DEFAULT NULL,
  `up_date` datetime(0) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`rid`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `resource_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of resource
-- ----------------------------
INSERT INTO `resource` VALUES (1, '20190224152059478531.txt', 'python岗位需求.txt', 1, '2019-02-24 15:20:59', 1);
INSERT INTO `resource` VALUES (2, '20190224152108763812.docx', '项目列表v12.docx', 109, '2019-02-24 15:21:08', 1);
INSERT INTO `resource` VALUES (3, '20190224152117466972.docx', '串讲181212.docx', 19, '2019-02-24 15:21:17', 1);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `username` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `photo` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `sex` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `location` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `about_me` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `registration_time` datetime(0) NULL DEFAULT NULL,
  `isAuthen` tinyint(1) NULL DEFAULT NULL,
  `name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, '499730483@qq.com', 'zy', 'pbkdf2:sha256:50000$DYM6t5rO$823e04d037d5fafb4e97cf3b2c4f365073183793397e8a1ecfad927f95215cf4', '20190224161441161463.png', '男', '杭州西湖', '个人简介略个人简介略个人简介略个人简介略个人简介略个人简介略个人简介略个人简介略个人简介略个人简介略个人简介略个人简介略', '2019-02-24 00:00:00', 1, '我的昵称');
INSERT INTO `user` VALUES (4, '2946781996@qq.com', 'zy2', 'pbkdf2:sha256:50000$OgdBdptg$99ba8ead78d3c463af1e7fe03bccea3d318ef91b4b8f82fdccd984ccda08fe4a', '20190224161441161463.png', '男', '温州', '啥也没写', '2019-02-24 00:00:00', 1, 'zzz');

-- ----------------------------
-- Table structure for user_reply
-- ----------------------------
DROP TABLE IF EXISTS `user_reply`;
CREATE TABLE `user_reply`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `replay_kuang` int(11) NOT NULL,
  `replay_user` int(11) NOT NULL,
  `replay_user_self` int(11) NOT NULL,
  `replay_content` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `replay_time` datetime(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `replay_kuang`(`replay_kuang`) USING BTREE,
  INDEX `replay_user`(`replay_user`) USING BTREE,
  INDEX `replay_user_self`(`replay_user_self`) USING BTREE,
  CONSTRAINT `user_reply_ibfk_1` FOREIGN KEY (`replay_kuang`) REFERENCES `comment` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_reply_ibfk_2` FOREIGN KEY (`replay_user`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_reply_ibfk_3` FOREIGN KEY (`replay_user_self`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for video
-- ----------------------------
DROP TABLE IF EXISTS `video`;
CREATE TABLE `video`  (
  `vid` int(11) NOT NULL AUTO_INCREMENT,
  `vtitle` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `savename` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `vcontent` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `up_date` date NULL DEFAULT NULL,
  `hits` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`vid`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `video_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of video
-- ----------------------------
INSERT INTO `video` VALUES (1, '小罐茶', '20190224154452339438.MP4', '中秋到喝小罐茶', '2019-02-24', 0, 1);
INSERT INTO `video` VALUES (2, '小视频2', '20190224155049007245.mp4', '不知道哪里找到的', '2019-02-24', 0, 1);
INSERT INTO `video` VALUES (3, '。。。。', '20190224155552233017.mp4', '额', '2019-02-24', 0, 1);
INSERT INTO `video` VALUES (4, '看看这是啥', '20190224155701538182.mp4', '', '2019-02-24', 0, 1);
INSERT INTO `video` VALUES (5, '...', '20190224214216314285.mp4', '', '2019-02-24', 0, 4);
INSERT INTO `video` VALUES (6, '小罐茶2.0', '20190224214234535837.MP4', '', '2019-02-24', 0, 4);
INSERT INTO `video` VALUES (7, '小罐茶2.03', '20190224214251471143.MP4', '', '2019-02-24', 0, 4);

SET FOREIGN_KEY_CHECKS = 1;
