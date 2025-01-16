CREATE SCHEMA IF NOT EXISTS user_service;
SET search_path TO user_service;
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    phone_number VARCHAR(20),
    role VARCHAR(20) DEFAULT 'user' NOT NULL,
    social_links JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE OR REPLACE FUNCTION update_user_timestamp() RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = CURRENT_TIMESTAMP;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER set_users_updated_at BEFORE
UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_user_timestamp();
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username_lower ON users (LOWER(username));
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email_lower ON users (LOWER(email));
GRANT USAGE ON SCHEMA user_service TO userhub_user;
GRANT SELECT,
    INSERT,
    UPDATE,
    DELETE ON ALL TABLES IN SCHEMA user_service TO userhub_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA user_service
GRANT SELECT,
    INSERT,
    UPDATE,
    DELETE ON TABLES TO userhub_user;
DO $$ BEGIN IF NOT EXISTS (
    SELECT 1
    FROM users
    WHERE username = 'admin'
) THEN
INSERT INTO users (
        user_id,
        username,
        password_hash,
        email,
        first_name,
        last_name,
        role,
        created_at,
        updated_at
    )
VALUES (
        gen_random_uuid(),
        'admin',
        '$2b$12$e4y5Q4CRh1R3On7v6jNkMuwCMZVh5.wc3DpE4S5wK89gxVvGGclye',
        'admin@example.com',
        'Default',
        'Admin',
        'admin',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    );
END IF;
END $$;