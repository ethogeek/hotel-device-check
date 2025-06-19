-- Device Lifecycle API: SQLite schema

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT,
    role TEXT NOT NULL DEFAULT 'viewer',
    score INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1
);

CREATE TABLE devices (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    manufacturer TEXT NOT NULL,
    model TEXT NOT NULL,
    eos_date DATE,
    eol_date DATE,
    life_status TEXT,
    notes TEXT,
    photo TEXT,
    approval_state TEXT CHECK (approval_state IN ('pending', 'published')) NOT NULL DEFAULT 'pending',
    created_by TEXT,
    FOREIGN KEY (created_by) REFERENCES users(username)
);

CREATE INDEX idx_devices_name_model ON devices(name, model);
