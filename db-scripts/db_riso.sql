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
-- Table `RISO`.`tb_conceito`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `RISO`.`tb_conceito` ;

CREATE TABLE IF NOT EXISTS `RISO`.`tb_conceito` (
  `id` INT(11) NOT NULL,
  `termo` VARCHAR(100) NOT NULL,
  `descricao` VARCHAR(100) NULL,
  `contexto` VARCHAR(100) NULL,
  PRIMARY KEY (`id`));

-- -----------------------------------------------------
-- Table `RISO`.`tb_relacao`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `RISO`.`tb_relacao` ;

CREATE TABLE IF NOT EXISTS `RISO`.`tb_relacao` (
  `id_conceito_principal` INT(11) NOT NULL,
  `id_conceito_secundario` INT(11) NOT NULL,
  `relacao` VARCHAR(100) NOT NULL,
  INDEX `fk_tb_conceito_idx` (`id_conceito_principal` ASC),
  FOREIGN KEY (`id_conceito_principal`)
    REFERENCES `RISO`.`tb_conceito` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  FOREIGN KEY (`id_conceito_secundario`)
    REFERENCES `RISO`.`tb_conceito` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Table `RISO`.`tb_documento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `RISO`.`tb_documento` ;

CREATE TABLE IF NOT EXISTS `RISO`.`tb_documento` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(100) NOT NULL,
  `contexto` VARCHAR(100) NULL,
  `arquivo` LONGTEXT NOT NULL,
  PRIMARY KEY (`id`));

-- -----------------------------------------------------
-- Table `RISO`.`tb_conceito_documento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `RISO`.`tb_conceito_documento` ;

CREATE TABLE IF NOT EXISTS `RISO`.`tb_conceito_documento` (
  `id_conceito` INT(11) NOT NULL,
  `id_documento` INT(11) NOT NULL,
  INDEX `fk_tb_documento_idx` (`id_documento` ASC),
  CONSTRAINT `fk_tb_conceito_documento`
    FOREIGN KEY (`id_conceito`)
    REFERENCES `RISO`.`tb_conceito` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_conceito_documento_2`
    FOREIGN KEY (`id_documento`)
    REFERENCES `RISO`.`tb_documento` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
