
CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);

ALTER TABLE public.alembic_version OWNER TO taskmngr;

--
-- TOC entry 217 (class 1259 OID 16409)
-- Name: dialogs; Type: TABLE; Schema: public; Owner: taskmngr
--

CREATE TABLE public.dialogs (
    creator_id uuid NOT NULL,
    interlocutor_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT date_trunc('seconds'::text, (now())::timestamp without time zone) NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL
);


ALTER TABLE public.dialogs OWNER TO taskmngr;

--
-- TOC entry 219 (class 1259 OID 16440)
-- Name: messages; Type: TABLE; Schema: public; Owner: taskmngr
--

CREATE TABLE public.messages (
    dialog_id uuid NOT NULL,
    sender_id uuid NOT NULL,
    content character varying(120),
    send_at timestamp without time zone DEFAULT date_trunc('seconds'::text, (now())::timestamp without time zone) NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL
);


ALTER TABLE public.messages OWNER TO taskmngr;

--
-- TOC entry 220 (class 1259 OID 16457)
-- Name: projects; Type: TABLE; Schema: public; Owner: taskmngr
--

CREATE TABLE public.projects (
    title character varying(128) DEFAULT concat('New project ', "substring"((gen_random_uuid())::text, 1, 5)) NOT NULL,
    description text,
    creator_id uuid NOT NULL,
    team_id uuid,
    created_at timestamp without time zone DEFAULT date_trunc('seconds'::text, (now())::timestamp without time zone) NOT NULL,
    updated_at timestamp without time zone DEFAULT date_trunc('seconds'::text, (now())::timestamp without time zone) NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL
);


ALTER TABLE public.projects OWNER TO taskmngr;

--
-- TOC entry 224 (class 1259 OID 16537)
-- Name: taskcomments; Type: TABLE; Schema: public; Owner: taskmngr
--

CREATE TABLE public.taskcomments (
    content character varying(256) NOT NULL,
    created_at timestamp without time zone DEFAULT date_trunc('seconds'::text, (now())::timestamp without time zone) NOT NULL,
    user_id uuid NOT NULL,
    task_id uuid NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL
);


ALTER TABLE public.taskcomments OWNER TO taskmngr;

--
-- TOC entry 222 (class 1259 OID 16496)
-- Name: tasks; Type: TABLE; Schema: public; Owner: taskmngr
--

CREATE TABLE public.tasks (
    title character varying(128) DEFAULT concat('New task ', substr(md5((random())::text), 1, 5)) NOT NULL,
    description text,
    status character varying(32) DEFAULT 'created'::character varying NOT NULL,
    priority character varying DEFAULT 'low'::character varying NOT NULL,
    due_date timestamp without time zone NOT NULL,
    creator_id uuid NOT NULL,
    project_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT date_trunc('seconds'::text, (now())::timestamp without time zone) NOT NULL,
    updated_at timestamp without time zone DEFAULT date_trunc('seconds'::text, (now())::timestamp without time zone) NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL
);


ALTER TABLE public.tasks OWNER TO taskmngr;

--
-- TOC entry 218 (class 1259 OID 16426)
-- Name: teams; Type: TABLE; Schema: public; Owner: taskmngr
--

CREATE TABLE public.teams (
    title character varying(64) NOT NULL,
    description text,
    creator_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT date_trunc('seconds'::text, (now())::timestamp without time zone) NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL
);


ALTER TABLE public.teams OWNER TO taskmngr;

--
-- TOC entry 216 (class 1259 OID 16396)
-- Name: users; Type: TABLE; Schema: public; Owner: taskmngr
--

CREATE TABLE public.users (
    email character varying(64) NOT NULL,
    username character varying(64) NOT NULL,
    hashed_password character varying(256) NOT NULL,
    first_name character varying(32),
    last_name character varying(32),
    "position" character varying(64),
    avatar_url character varying(256),
    role character varying(32) NOT NULL,
    is_active boolean NOT NULL,
    is_verified boolean NOT NULL,
    created_at timestamp without time zone DEFAULT date_trunc('seconds'::text, (now())::timestamp without time zone) NOT NULL,
    id uuid DEFAULT gen_random_uuid() NOT NULL
);


ALTER TABLE public.users OWNER TO taskmngr;

--
-- TOC entry 223 (class 1259 OID 16519)
-- Name: users_projects; Type: TABLE; Schema: public; Owner: taskmngr
--

CREATE TABLE public.users_projects (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    project_id uuid NOT NULL
);


ALTER TABLE public.users_projects OWNER TO taskmngr;

--
-- TOC entry 225 (class 1259 OID 16554)
-- Name: users_tasks; Type: TABLE; Schema: public; Owner: taskmngr
--

CREATE TABLE public.users_tasks (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    task_id uuid NOT NULL
);


ALTER TABLE public.users_tasks OWNER TO taskmngr;

--
-- TOC entry 221 (class 1259 OID 16478)
-- Name: users_teams; Type: TABLE; Schema: public; Owner: taskmngr
--

CREATE TABLE public.users_teams (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    team_id uuid NOT NULL
);


ALTER TABLE public.users_teams OWNER TO taskmngr;

--
-- TOC entry 3476 (class 0 OID 16391)
-- Dependencies: 215
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: taskmngr
--

COPY public.alembic_version (version_num) FROM stdin;
8b92b33d53bd
\.


--
-- TOC entry 3478 (class 0 OID 16409)
-- Dependencies: 217
-- Data for Name: dialogs; Type: TABLE DATA; Schema: public; Owner: taskmngr
--

COPY public.dialogs (creator_id, interlocutor_id, created_at, id) FROM stdin;
\.


--
-- TOC entry 3480 (class 0 OID 16440)
-- Dependencies: 219
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: taskmngr
--

COPY public.messages (dialog_id, sender_id, content, send_at, id) FROM stdin;
\.


--
-- TOC entry 3481 (class 0 OID 16457)
-- Dependencies: 220
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: taskmngr
--

COPY public.projects (title, description, creator_id, team_id, created_at, updated_at, id) FROM stdin;
\.


--
-- TOC entry 3485 (class 0 OID 16537)
-- Dependencies: 224
-- Data for Name: taskcomments; Type: TABLE DATA; Schema: public; Owner: taskmngr
--

COPY public.taskcomments (content, created_at, user_id, task_id, id) FROM stdin;
\.


--
-- TOC entry 3483 (class 0 OID 16496)
-- Dependencies: 222
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: taskmngr
--

COPY public.tasks (title, description, status, priority, due_date, creator_id, project_id, created_at, updated_at, id) FROM stdin;
\.


--
-- TOC entry 3479 (class 0 OID 16426)
-- Dependencies: 218
-- Data for Name: teams; Type: TABLE DATA; Schema: public; Owner: taskmngr
--

COPY public.teams (title, description, creator_id, created_at, id) FROM stdin;
\.


--
-- TOC entry 3477 (class 0 OID 16396)
-- Dependencies: 216
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: taskmngr
--

COPY public.users (email, username, hashed_password, first_name, last_name, "position", avatar_url, role, is_active, is_verified, created_at, id) FROM stdin;
\.


--
-- TOC entry 3484 (class 0 OID 16519)
-- Dependencies: 223
-- Data for Name: users_projects; Type: TABLE DATA; Schema: public; Owner: taskmngr
--

COPY public.users_projects (id, user_id, project_id) FROM stdin;
\.


--
-- TOC entry 3486 (class 0 OID 16554)
-- Dependencies: 225
-- Data for Name: users_tasks; Type: TABLE DATA; Schema: public; Owner: taskmngr
--

COPY public.users_tasks (id, user_id, task_id) FROM stdin;
\.


--
-- TOC entry 3482 (class 0 OID 16478)
-- Dependencies: 221
-- Data for Name: users_teams; Type: TABLE DATA; Schema: public; Owner: taskmngr
--

COPY public.users_teams (id, user_id, team_id) FROM stdin;
\.


--
-- TOC entry 3285 (class 2606 OID 16395)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 3293 (class 2606 OID 16415)
-- Name: dialogs dialogs_pkey; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.dialogs
    ADD CONSTRAINT dialogs_pkey PRIMARY KEY (id);


--
-- TOC entry 3297 (class 2606 OID 16446)
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- TOC entry 3299 (class 2606 OID 16467)
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- TOC entry 3311 (class 2606 OID 16543)
-- Name: taskcomments taskcomments_pkey; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.taskcomments
    ADD CONSTRAINT taskcomments_pkey PRIMARY KEY (id);


--
-- TOC entry 3305 (class 2606 OID 16508)
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 3295 (class 2606 OID 16434)
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (id);


--
-- TOC entry 3307 (class 2606 OID 16526)
-- Name: users_projects unique_users_projects; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users_projects
    ADD CONSTRAINT unique_users_projects UNIQUE (user_id, project_id);


--
-- TOC entry 3313 (class 2606 OID 16561)
-- Name: users_tasks unique_users_tasks; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users_tasks
    ADD CONSTRAINT unique_users_tasks UNIQUE (user_id, task_id);


--
-- TOC entry 3301 (class 2606 OID 16485)
-- Name: users_teams unique_users_teams; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users_teams
    ADD CONSTRAINT unique_users_teams UNIQUE (user_id, team_id);


--
-- TOC entry 3287 (class 2606 OID 16406)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 3289 (class 2606 OID 16404)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3309 (class 2606 OID 16524)
-- Name: users_projects users_projects_pkey; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users_projects
    ADD CONSTRAINT users_projects_pkey PRIMARY KEY (id);


--
-- TOC entry 3315 (class 2606 OID 16559)
-- Name: users_tasks users_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users_tasks
    ADD CONSTRAINT users_tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 3303 (class 2606 OID 16483)
-- Name: users_teams users_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users_teams
    ADD CONSTRAINT users_teams_pkey PRIMARY KEY (id);


--
-- TOC entry 3291 (class 2606 OID 16408)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 3316 (class 2606 OID 16416)
-- Name: dialogs dialogs_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.dialogs
    ADD CONSTRAINT dialogs_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 3317 (class 2606 OID 16421)
-- Name: dialogs dialogs_interlocutor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.dialogs
    ADD CONSTRAINT dialogs_interlocutor_id_fkey FOREIGN KEY (interlocutor_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 3319 (class 2606 OID 16447)
-- Name: messages messages_dialog_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_dialog_id_fkey FOREIGN KEY (dialog_id) REFERENCES public.dialogs(id);


--
-- TOC entry 3320 (class 2606 OID 16452)
-- Name: messages messages_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 3321 (class 2606 OID 16468)
-- Name: projects projects_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(id);


--
-- TOC entry 3322 (class 2606 OID 16473)
-- Name: projects projects_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.teams(id);


--
-- TOC entry 3329 (class 2606 OID 16544)
-- Name: taskcomments taskcomments_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.taskcomments
    ADD CONSTRAINT taskcomments_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3330 (class 2606 OID 16549)
-- Name: taskcomments taskcomments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.taskcomments
    ADD CONSTRAINT taskcomments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3325 (class 2606 OID 16509)
-- Name: tasks tasks_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(id);


--
-- TOC entry 3326 (class 2606 OID 16514)
-- Name: tasks tasks_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- TOC entry 3318 (class 2606 OID 16435)
-- Name: teams teams_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3327 (class 2606 OID 16527)
-- Name: users_projects users_projects_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users_projects
    ADD CONSTRAINT users_projects_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3328 (class 2606 OID 16532)
-- Name: users_projects users_projects_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users_projects
    ADD CONSTRAINT users_projects_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3331 (class 2606 OID 16562)
-- Name: users_tasks users_tasks_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users_tasks
    ADD CONSTRAINT users_tasks_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3332 (class 2606 OID 16567)
-- Name: users_tasks users_tasks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users_tasks
    ADD CONSTRAINT users_tasks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3323 (class 2606 OID 16486)
-- Name: users_teams users_teams_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users_teams
    ADD CONSTRAINT users_teams_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.teams(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3324 (class 2606 OID 16491)
-- Name: users_teams users_teams_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: taskmngr
--

ALTER TABLE ONLY public.users_teams
    ADD CONSTRAINT users_teams_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2023-12-15 20:06:31 MSK

--
-- PostgreSQL database dump complete
--

