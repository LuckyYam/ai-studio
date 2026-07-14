CREATE DATABASE IF NOT EXISTS ai_studio_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE ai_studio_db;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
CREATE TABLE IF NOT EXISTS users (
    id                          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    full_name                   VARCHAR(255)     NOT NULL,
    email                       VARCHAR(255)     NOT NULL,
    password_hash               VARCHAR(255)     NOT NULL,
    model                       VARCHAR(100)     NOT NULL DEFAULT 'gemini-3.1-flash-lite',
    temperature                 FLOAT            NOT NULL DEFAULT 0.1,
    max_output_tokens           INT UNSIGNED     NOT NULL DEFAULT 2048,
    top_p                       FLOAT            NOT NULL DEFAULT 0.95,
    top_k                       INT UNSIGNED     NOT NULL DEFAULT 64,
    web_search                  BOOLEAN          NOT NULL DEFAULT FALSE,
    is_active                   BOOLEAN          NOT NULL DEFAULT TRUE,
    email_verified_at           DATETIME         NULL,
    last_login_at               DATETIME         NULL,
    created_at                  DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                  DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP
                                                  ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS conversations (
    id                VARCHAR(100)    PRIMARY KEY,
    user_id           BIGINT UNSIGNED NOT NULL,
    title             VARCHAR(500)    NOT NULL DEFAULT 'New chat',
    model             VARCHAR(100)    NULL,
    is_pinned         BOOLEAN         NOT NULL DEFAULT FALSE,
    message_count     INT UNSIGNED    NOT NULL DEFAULT 0,
    word_count        INT UNSIGNED    NOT NULL DEFAULT 0,
    created_at        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                                       ON UPDATE CURRENT_TIMESTAMP,
    pinned_at         DATETIME        NULL,
    CONSTRAINT fk_conversations_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,
    INDEX idx_conversations_user_id      (user_id),
    INDEX idx_conversations_user_pinned  (user_id, is_pinned),
    INDEX idx_conversations_user_updated (user_id, updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS messages (
    id                 BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    conversation_id    VARCHAR(100)    NOT NULL,
    role               ENUM('user', 'assistant') NOT NULL,
    message            MEDIUMTEXT      NOT NULL,
    raw_parts          JSON            NULL,
    created_at         DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_messages_conversation
        FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        ON DELETE CASCADE,
    INDEX idx_messages_conversation_id      (conversation_id),
    INDEX idx_messages_conversation_created (conversation_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS message_attachments (
    id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    message_id    BIGINT UNSIGNED NOT NULL,
    name          VARCHAR(255)    NOT NULL,
    mime_type     VARCHAR(127)    NOT NULL,
    size          INT UNSIGNED    NOT NULL,
    available     BOOLEAN         NOT NULL DEFAULT TRUE,
    data          LONGBLOB        NULL,
    created_at    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_attachments_message
        FOREIGN KEY (message_id) REFERENCES messages(id)
        ON DELETE CASCADE,
    INDEX idx_attachments_message_id (message_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS message_sources (
    id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    message_id    BIGINT UNSIGNED NOT NULL,
    uri           VARCHAR(2048)   NOT NULL,
    title         VARCHAR(500)    NOT NULL,
    CONSTRAINT fk_sources_message
        FOREIGN KEY (message_id) REFERENCES messages(id)
        ON DELETE CASCADE,
    INDEX idx_sources_message_id (message_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
SET FOREIGN_KEY_CHECKS = 1;