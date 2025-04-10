--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: appointments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.appointments (
    id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    email character varying(100),
    phone character varying(20),
    appointment_time timestamp without time zone NOT NULL,
    event_type character varying(50),
    gender_identity character varying(50),
    notes text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.appointments OWNER TO postgres;

--
-- Name: appointments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.appointments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.appointments_id_seq OWNER TO postgres;

--
-- Name: appointments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.appointments_id_seq OWNED BY public.appointments.id;


--
-- Name: appointments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointments ALTER COLUMN id SET DEFAULT nextval('public.appointments_id_seq'::regclass);


--
-- Data for Name: appointments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.appointments (id, full_name, email, phone, appointment_time, event_type, gender_identity, notes, created_at) FROM stdin;
1	Jasmine Rivera	jasmine.r@example.com	317-555-1234	2025-04-10 14:00:00	Prom	Female	Wants something in navy or black.	2025-04-07 14:32:51.852921
2	Marcus Lee	marcus.l@example.com	317-555-2345	2025-04-11 10:30:00	Interview	Male	Needs something conservative for an office setting.	2025-04-07 14:32:51.852921
3	Taylor Nguyen	\N	317-555-3456	2025-04-12 13:00:00	Graduation	Non-binary	Prefers neutral tones.	2025-04-07 14:32:51.852921
4	Samantha Green	sam.green@example.com	\N	2025-04-13 15:00:00	Wedding	Female	Attending as a guest.	2025-04-07 14:32:51.852921
5	Devon Brooks	devon.b@example.com	317-555-4567	2025-04-14 11:00:00	Interview	Male	Looking for dress shoes as well.	2025-04-07 14:32:51.852921
\.


--
-- Name: appointments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.appointments_id_seq', 5, true);


--
-- Name: appointments appointments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

