--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5
-- Dumped by pg_dump version 11.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: album; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.album (
    title character varying NOT NULL,
    uri character varying NOT NULL,
    artisturi character varying,
    id character varying NOT NULL
);


--
-- Name: artist; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.artist (
    name character varying NOT NULL,
    uri character varying NOT NULL,
    id character varying NOT NULL
);


--
-- Name: context; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.context (
    uri character varying NOT NULL,
    type character varying NOT NULL
);


--
-- Name: cursors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cursors (
    after character varying NOT NULL,
    before character varying
);


--
-- Name: played; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.played (
    trackuri character varying NOT NULL,
    artisturi character varying,
    contexturi character varying,
    "time" timestamp without time zone NOT NULL
);


--
-- Name: track; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.track (
    title character varying NOT NULL,
    uri character varying NOT NULL,
    artisturi character varying,
    albumuri character varying,
    id character varying NOT NULL,
    duration integer,
    explicit boolean,
    popularity smallint,
    tracknumber smallint
);


--
-- Name: album album_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.album
    ADD CONSTRAINT album_pkey PRIMARY KEY (id);


--
-- Name: album album_uri_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.album
    ADD CONSTRAINT album_uri_key UNIQUE (uri);


--
-- Name: artist artist_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.artist
    ADD CONSTRAINT artist_pkey PRIMARY KEY (id);


--
-- Name: artist artist_uri_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.artist
    ADD CONSTRAINT artist_uri_key UNIQUE (uri);


--
-- Name: context context_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.context
    ADD CONSTRAINT context_pkey PRIMARY KEY (uri);


--
-- Name: cursors cursors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cursors
    ADD CONSTRAINT cursors_pkey PRIMARY KEY (after);


--
-- Name: played played_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.played
    ADD CONSTRAINT played_pkey PRIMARY KEY ("time");


--
-- Name: track track_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.track
    ADD CONSTRAINT track_pkey PRIMARY KEY (id);


--
-- Name: track track_uri_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.track
    ADD CONSTRAINT track_uri_key UNIQUE (uri);


--
-- PostgreSQL database dump complete
--

