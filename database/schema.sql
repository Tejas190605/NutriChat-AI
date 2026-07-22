-- PostgreSQL DDL Schema for NutriChat AI (schema.sql)

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table 1: Dashboard Admin Users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: WhatsApp Chat Users (Nutrition Clients)
CREATE TABLE IF NOT EXISTS whatsapp_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    wa_id VARCHAR(50) UNIQUE NOT NULL, -- Phone number identifier
    name VARCHAR(255) NOT NULL,
    height DECIMAL(5,2),
    weight DECIMAL(5,2),
    goal VARCHAR(50),
    activity_level VARCHAR(50),
    target_calories INTEGER,
    target_protein DECIMAL(5,2),
    target_carbs DECIMAL(5,2),
    target_fat DECIMAL(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table 3: Meal Logs
CREATE TABLE IF NOT EXISTS meals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    whatsapp_user_id UUID NOT NULL REFERENCES whatsapp_users(id) ON DELETE CASCADE,
    meal_name VARCHAR(255) NOT NULL,
    calories INTEGER NOT NULL,
    protein DECIMAL(5,2) NOT NULL,
    carbs DECIMAL(5,2) NOT NULL,
    fat DECIMAL(5,2) NOT NULL,
    quantity VARCHAR(100), -- e.g. "2 slices", "1 bowl"
    image_url VARCHAR(512), -- Cloudinary storage URL
    time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table 4: Conversational Chat History
CREATE TABLE IF NOT EXISTS chat_histories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    whatsapp_user_id UUID NOT NULL REFERENCES whatsapp_users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- "user" or "assistant"
    message_body TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table 5: Automated Reminder Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    whatsapp_user_id UUID NOT NULL REFERENCES whatsapp_users(id) ON DELETE CASCADE,
    reminder_message VARCHAR(512) NOT NULL,
    schedule_cron VARCHAR(50) NOT NULL, -- Cron syntax e.g. "0 9 * * *"
    active BOOLEAN DEFAULT TRUE,
    last_sent TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table 6: Food Nutrition Queries Cache
CREATE TABLE IF NOT EXISTS food_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    food_query VARCHAR(255) UNIQUE NOT NULL,
    calories INTEGER NOT NULL,
    protein DECIMAL(5,2) NOT NULL,
    carbs DECIMAL(5,2) NOT NULL,
    fat DECIMAL(5,2) NOT NULL,
    raw_response JSONB,
    cached_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table 7: User Exercise & Activity History
CREATE TABLE IF NOT EXISTS user_activities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    whatsapp_user_id UUID NOT NULL REFERENCES whatsapp_users(id) ON DELETE CASCADE,
    activity_name VARCHAR(255) NOT NULL, -- e.g., "running", "walking"
    duration_minutes DECIMAL(6,2) NOT NULL,
    MET_value DECIMAL(4,2) NOT NULL,
    calories_burned INTEGER NOT NULL,
    time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_meals_user_time ON meals(whatsapp_user_id, time DESC);
CREATE INDEX IF NOT EXISTS idx_chat_user_timestamp ON chat_histories(whatsapp_user_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_notifications_active ON notifications(active) WHERE active IS TRUE;
CREATE INDEX IF NOT EXISTS idx_food_cache_query ON food_cache(food_query);
CREATE INDEX IF NOT EXISTS idx_activities_user_time ON user_activities(whatsapp_user_id, time DESC);
