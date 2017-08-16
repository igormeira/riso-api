SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema RISO
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `RISO` ;

-- -----------------------------------------------------
-- Schema RISO
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `RISO` DEFAULT CHARACTER SET utf8 ;
USE `RISO` ;

-- -----------------------------------------------------
-- Table `RISO`.`tb_termo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `RISO`.`tb_termo` ;

CREATE TABLE IF NOT EXISTS `RISO`.`tb_termo` (
  `id` INT(11) NOT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `descricao` VARCHAR(100) NULL,
  `contexto` VARCHAR(100) NULL,
  PRIMARY KEY (`id`));

-- -----------------------------------------------------
-- Table `RISO`.`tb_conceito`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `RISO`.`tb_conceito` ;

CREATE TABLE IF NOT EXISTS `RISO`.`tb_conceito` (
  `id_termo_principal` INT(11) NOT NULL,
  `id_termo_secundario` INT(11) NOT NULL,
  `relacao` VARCHAR(100) NOT NULL,
  INDEX `fk_tb_termo_idx` (`id_termo_principal` ASC),
  CONSTRAINT `fk_tb_termo_principal`
    FOREIGN KEY (`id_termo_principal`)
    REFERENCES `INSA`.`tb_termo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION),
  CONSTRAINT `fk_tb_termo_secundario`
    FOREIGN KEY (`id_termo_secundario`)
    REFERENCES `INSA`.`tb_termo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Table `RISO`.`tb_documento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `RISO`.`tb_documento` ;

CREATE TABLE IF NOT EXISTS `RISO`.`tb_documento` (
  `id` INT(11) NOT NULL,
  `nome` VARCHAR(100) NOT NULL,
  `contexto` VARCHAR(100) NULL,
  `arquivo` LONGTEXT NOT NULL,
  PRIMARY KEY (`id`));

-- -----------------------------------------------------
-- Table `RISO`.`tb_termo_documento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `RISO`.`tb_termo_documento` ;

CREATE TABLE IF NOT EXISTS `RISO`.`tb_termo_documento` (
  `id_termo` INT(11) NOT NULL,
  `id_documento` INT(11) NOT NULL,
  INDEX `fk_tb_documento_idx` (`id_documento` ASC),
  CONSTRAINT `fk_tb_termo_documento`
    FOREIGN KEY (`id_termo`)
    REFERENCES `INSA`.`tb_termo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_termo_documento_2`
    FOREIGN KEY (`id_documento`)
    REFERENCES `INSA`.`tb_documento` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
