/*
 Navicat Premium Data Transfer

 Source Server         : MyConnection
 Source Server Type    : MySQL
 Source Server Version : 100422
 Source Host           : localhost:3306
 Source Schema         : db_praktikum

 Target Server Type    : MySQL
 Target Server Version : 100422
 File Encoding         : 65001

 Date: 03/05/2022 11:25:24
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for mahasiswa
-- ----------------------------
DROP TABLE IF EXISTS `mahasiswa`;
CREATE TABLE `mahasiswa`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `nim` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `nama` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `jenis_kel` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `jurusan` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `hobi` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mahasiswa
-- ----------------------------
INSERT INTO `mahasiswa` VALUES (21, '1111', 'AAA', 'Laki-Laki', 'Filsafat Meme', 'Main Game, Bulu Tangkis');
INSERT INTO `mahasiswa` VALUES (22, '2222', 'BBB', 'Laki-Laki', 'Sastra Mesin', 'Main Game, Sepak Bola');

SET FOREIGN_KEY_CHECKS = 1;
