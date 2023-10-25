CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID DEFAULT uuid_generate_v4(),
    username VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT date_trunc('seconds', now()::timestamp),
    CONSTRAINT pk_users PRIMARY KEY (id)
);

CREATE TABLE projects (
    id UUID DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    user_id UUID,
    created_at TIMESTAMP DEFAULT date_trunc('seconds', now()::timestamp),
    updated_at TIMESTAMP DEFAULT date_trunc('seconds', now()::timestamp),
    CONSTRAINT pk_projects PRIMARY KEY (id),
    CONSTRAINT fk_users FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE tasks (
    id UUID DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    due_date DATE,
    user_id UUID,
    project_id UUID,
    created_at TIMESTAMP DEFAULT date_trunc('seconds', now()::timestamp),
    updated_at TIMESTAMP DEFAULT date_trunc('seconds', now()::timestamp),
    CONSTRAINT pk_tasks PRIMARY KEY (id),
    CONSTRAINT fk_users FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_projects FOREIGN KEY (project_id) REFERENCES projects(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE comments (
    id UUID DEFAULT uuid_generate_v4(),
    content TEXT NOT NULL,
    user_id UUID,
    task_id UUID,
    created_at TIMESTAMP DEFAULT date_trunc('seconds', now()::timestamp),
    CONSTRAINT pk_comments PRIMARY KEY (id),
    CONSTRAINT fk_users FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_tasks FOREIGN KEY (task_id) REFERENCES tasks(id) ON UPDATE CASCADE ON DELETE CASCADE
);
