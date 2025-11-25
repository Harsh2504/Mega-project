-- Add 2FA columns to users table
-- Run this script to enable 2FA functionality

ALTER TABLE `users` 
ADD COLUMN `totp_secret` VARCHAR(32) NULL DEFAULT NULL COMMENT 'TOTP secret key for 2FA',
ADD COLUMN `totp_enabled` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '2FA enabled flag (0=disabled, 1=enabled)';
