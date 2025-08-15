--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Debian 17.5-1.pgdg120+1)
-- Dumped by pg_dump version 17.0

-- Started on 2025-08-14 21:15:27 EDT

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
-- TOC entry 219 (class 1259 OID 24651)
-- Name: coinbase_macd; Type: TABLE; Schema: public; Owner: developer
--

CREATE TABLE public.coinbase_macd (
    epoctimestamp bigint NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    symbol text NOT NULL,
    macd double precision,
    signal double precision,
    histogram double precision,
    coinname text,
    granularity text NOT NULL
);


ALTER TABLE public.coinbase_macd OWNER TO developer;

--
-- TOC entry 3213 (class 2606 OID 24657)
-- Name: coinbase_macd coinbase_macd_pkey; Type: CONSTRAINT; Schema: public; Owner: developer
--

ALTER TABLE ONLY public.coinbase_macd
    ADD CONSTRAINT coinbase_macd_pkey PRIMARY KEY (epoctimestamp, symbol, granularity);


-- Completed on 2025-08-14 21:15:28 EDT

--
-- PostgreSQL database dump complete
--

