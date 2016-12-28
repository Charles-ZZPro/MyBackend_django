--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE auth_group OWNER TO "littleAdmin";

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: littleAdmin
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_id_seq OWNER TO "littleAdmin";

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: littleAdmin
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_group_permissions OWNER TO "littleAdmin";

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: littleAdmin
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_permissions_id_seq OWNER TO "littleAdmin";

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: littleAdmin
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE auth_permission OWNER TO "littleAdmin";

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: littleAdmin
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_permission_id_seq OWNER TO "littleAdmin";

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: littleAdmin
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE auth_user OWNER TO "littleAdmin";

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE auth_user_groups OWNER TO "littleAdmin";

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: littleAdmin
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_groups_id_seq OWNER TO "littleAdmin";

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: littleAdmin
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: littleAdmin
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_id_seq OWNER TO "littleAdmin";

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: littleAdmin
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_user_user_permissions OWNER TO "littleAdmin";

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: littleAdmin
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_user_permissions_id_seq OWNER TO "littleAdmin";

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: littleAdmin
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE django_admin_log OWNER TO "littleAdmin";

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: littleAdmin
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_admin_log_id_seq OWNER TO "littleAdmin";

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: littleAdmin
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO "littleAdmin";

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: littleAdmin
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_content_type_id_seq OWNER TO "littleAdmin";

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: littleAdmin
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO "littleAdmin";

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: littleAdmin
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO "littleAdmin";

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: littleAdmin
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE django_session OWNER TO "littleAdmin";

--
-- Name: table_activate_num_id_seq; Type: SEQUENCE; Schema: public; Owner: littleAdmin
--

CREATE SEQUENCE table_activate_num_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 99999999
    CACHE 1;


ALTER TABLE table_activate_num_id_seq OWNER TO "littleAdmin";

--
-- Name: table_activate_num; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE table_activate_num (
    id integer DEFAULT nextval('table_activate_num_id_seq'::regclass) NOT NULL,
    proj_name text,
    date_s text,
    act_num integer,
    proj_id integer
);


ALTER TABLE table_activate_num OWNER TO "littleAdmin";

--
-- Name: table_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: littleAdmin
--

CREATE SEQUENCE table_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 99999999
    CACHE 1;


ALTER TABLE table_permission_id_seq OWNER TO "littleAdmin";

--
-- Name: table_permission; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE table_permission (
    id integer DEFAULT nextval('table_permission_id_seq'::regclass) NOT NULL,
    permit_name text
);


ALTER TABLE table_permission OWNER TO "littleAdmin";

--
-- Name: table_role_id_seq; Type: SEQUENCE; Schema: public; Owner: littleAdmin
--

CREATE SEQUENCE table_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 99999999
    CACHE 1;


ALTER TABLE table_role_id_seq OWNER TO "littleAdmin";

--
-- Name: table_role; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE table_role (
    id integer DEFAULT nextval('table_role_id_seq'::regclass) NOT NULL,
    role_name text,
    permission text
);


ALTER TABLE table_role OWNER TO "littleAdmin";

--
-- Name: table_user_id_seq; Type: SEQUENCE; Schema: public; Owner: littleAdmin
--

CREATE SEQUENCE table_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 99999999
    CACHE 1;


ALTER TABLE table_user_id_seq OWNER TO "littleAdmin";

--
-- Name: table_user; Type: TABLE; Schema: public; Owner: littleAdmin
--

CREATE TABLE table_user (
    id integer DEFAULT nextval('table_user_id_seq'::regclass) NOT NULL,
    user_name text,
    user_type text,
    passwd text,
    related_proj_id integer
);


ALTER TABLE table_user OWNER TO "littleAdmin";

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: littleAdmin
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: littleAdmin
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
10	Can add group	4	add_group
11	Can change group	4	change_group
12	Can delete group	4	delete_group
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: littleAdmin
--

SELECT pg_catalog.setval('auth_permission_id_seq', 18, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: littleAdmin
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: littleAdmin
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, false);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: littleAdmin
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: littleAdmin
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, false);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	user
4	auth	group
5	contenttypes	contenttype
6	sessions	session
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: littleAdmin
--

SELECT pg_catalog.setval('django_content_type_id_seq', 6, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2016-12-16 12:45:15.237252+08
2	auth	0001_initial	2016-12-16 12:45:15.358416+08
3	admin	0001_initial	2016-12-16 12:45:15.420513+08
4	admin	0002_logentry_remove_auto_add	2016-12-16 12:45:15.454968+08
5	contenttypes	0002_remove_content_type_name	2016-12-16 12:45:15.492262+08
6	auth	0002_alter_permission_name_max_length	2016-12-16 12:45:15.507655+08
7	auth	0003_alter_user_email_max_length	2016-12-16 12:45:15.525154+08
8	auth	0004_alter_user_username_opts	2016-12-16 12:45:15.536698+08
9	auth	0005_alter_user_last_login_null	2016-12-16 12:45:15.556561+08
10	auth	0006_require_contenttypes_0002	2016-12-16 12:45:15.55996+08
11	auth	0007_alter_validators_add_error_messages	2016-12-16 12:45:15.574862+08
12	auth	0008_alter_user_username_max_length	2016-12-16 12:45:15.595707+08
13	sessions	0001_initial	2016-12-16 12:45:15.613018+08
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: littleAdmin
--

SELECT pg_catalog.setval('django_migrations_id_seq', 13, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: table_activate_num; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY table_activate_num (id, proj_name, date_s, act_num, proj_id) FROM stdin;
1	第一个项目	2016-12-12	150	1
2	第二个项目	2016-12-12	110	2
3	第三个项目	2016-12-12	180	3
4	第一个项目	2016-12-13	390	1
5	第二个项目	2016-12-13	240	2
6	第三个项目	2016-12-13	250	3
7	第一个项目	2016-12-14	585	1
8	第二个项目	2016-12-14	996	2
9	第三个项目	2016-12-14	1457	3
10	第一个项目	2016-12-15	1874	1
11	第二个项目	2016-12-15	2150	2
12	第三个项目	2016-12-15	3658	3
13	第一个项目	2016-12-16	7864	1
14	第二个项目	2016-12-16	9337	2
15	第三个项目	2016-12-16	1285	3
16	第一个项目	2016-12-17	4881	1
17	第二个项目	2016-12-17	87974	2
18	第三个项目	2016-12-17	41687	3
19	第一个项目	2016-12-18	79465	1
20	第二个项目	2016-12-18	7963	2
21	第三个项目	2016-12-18	1357	3
22	第四个test项目	2016-12-18	97418	4
23	第一个项目	2016-12-19	887654131	1
24	第二个项目	2016-12-19	7821212	2
25	第三个项目	2016-12-19	966131	3
26	第四个test项目	2016-12-19	32137674	4
143	第一个项目	2016-12-23	695557	1
144	第二个项目	2016-12-23	975538	2
145	第三个项目	2016-12-23	57519	3
146	第四个test项目	2016-12-23	579315	4
147	第一个项目	2016-12-24	847738	1
148	第二个项目	2016-12-24	50819	2
149	第三个项目	2016-12-24	629050	3
150	第四个test项目	2016-12-24	146085	4
151	第一个项目	2016-12-25	212687	1
152	第二个项目	2016-12-25	518896	2
153	第三个项目	2016-12-25	419645	3
154	第四个test项目	2016-12-25	306680	4
155	第一个项目	2016-12-26	818846	1
156	第二个项目	2016-12-26	413198	2
157	第三个项目	2016-12-26	135482	3
158	第四个test项目	2016-12-26	240028	4
159	第一个项目	2016-12-26	61844	1
160	第二个项目	2016-12-26	520363	2
161	第三个项目	2016-12-26	643315	3
162	第四个test项目	2016-12-26	924368	4
163	第一个项目	2016-12-26	120773	1
164	第二个项目	2016-12-26	940209	2
165	第三个项目	2016-12-26	540822	3
166	第四个test项目	2016-12-26	399856	4
167	第一个项目	2016-12-26	75314	1
168	第二个项目	2016-12-26	174783	2
169	第三个项目	2016-12-26	557688	3
170	第四个test项目	2016-12-26	443692	4
99	第一个项目	2016-12-20	721943	1
100	第二个项目	2016-12-20	493214	2
101	第三个项目	2016-12-20	200903	3
102	第四个test项目	2016-12-20	359310	4
171	第一个项目	2016-12-26	176762	1
172	第二个项目	2016-12-26	856463	2
173	第三个项目	2016-12-26	139394	3
174	第四个test项目	2016-12-26	729665	4
175	第一个项目	2016-12-27	387155	1
176	第二个项目	2016-12-27	697773	2
177	第三个项目	2016-12-27	852120	3
178	第四个test项目	2016-12-27	865569	4
111	第一个项目	2016-12-21	255665	1
112	第二个项目	2016-12-21	210871	2
113	第三个项目	2016-12-21	201770	3
114	第四个test项目	2016-12-21	209003	4
131	第一个项目	2016-12-22	771526	1
132	第二个项目	2016-12-22	971704	2
133	第三个项目	2016-12-22	975063	3
134	第四个test项目	2016-12-22	374234	4
\.


--
-- Name: table_activate_num_id_seq; Type: SEQUENCE SET; Schema: public; Owner: littleAdmin
--

SELECT pg_catalog.setval('table_activate_num_id_seq', 178, true);


--
-- Data for Name: table_permission; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY table_permission (id, permit_name) FROM stdin;
1	view_act_num
\.


--
-- Name: table_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: littleAdmin
--

SELECT pg_catalog.setval('table_permission_id_seq', 1, true);


--
-- Data for Name: table_role; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY table_role (id, role_name, permission) FROM stdin;
1	super_admin	\N
2	admin	\N
3	user	\N
\.


--
-- Name: table_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: littleAdmin
--

SELECT pg_catalog.setval('table_role_id_seq', 3, true);


--
-- Data for Name: table_user; Type: TABLE DATA; Schema: public; Owner: littleAdmin
--

COPY table_user (id, user_name, user_type, passwd, related_proj_id) FROM stdin;
1	slient	admin	a123456	\N
2	charles	admin	a654321	\N
3	j	user	a	2
\.


--
-- Name: table_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: littleAdmin
--

SELECT pg_catalog.setval('table_user_id_seq', 3, true);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: table_activate_num_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY table_activate_num
    ADD CONSTRAINT table_activate_num_pkey PRIMARY KEY (id);


--
-- Name: table_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY table_permission
    ADD CONSTRAINT table_permission_pkey PRIMARY KEY (id);


--
-- Name: table_role_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY table_role
    ADD CONSTRAINT table_role_pkey PRIMARY KEY (id);


--
-- Name: table_user_pkey; Type: CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY table_user
    ADD CONSTRAINT table_user_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: littleAdmin
--

CREATE INDEX auth_group_name_a6ea08ec_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: littleAdmin
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: littleAdmin
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: littleAdmin
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: littleAdmin
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: littleAdmin
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: littleAdmin
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: littleAdmin
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: littleAdmin
--

CREATE INDEX auth_user_username_6821ab7c_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: littleAdmin
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: littleAdmin
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: littleAdmin
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: littleAdmin
--

CREATE INDEX django_session_session_key_c0390e0f_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: littleAdmin
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

