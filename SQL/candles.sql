--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Debian 17.5-1.pgdg120+1)
-- Dumped by pg_dump version 17.0

-- Started on 2025-08-12 22:03:29 EDT

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
-- TOC entry 217 (class 1259 OID 16460)
-- Name: coinbase_ohlc; Type: TABLE; Schema: public; Owner: developer
--

CREATE TABLE public.coinbase_ohlc (
    symbol text,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume double precision,
    coinname character varying,
    granularity character varying,
    id integer NOT NULL,
    epoctimestamp integer,
    "timestamp" timestamp with time zone
);


ALTER TABLE public.coinbase_ohlc OWNER TO developer;

--
-- TOC entry 218 (class 1259 OID 16467)
-- Name: coinbase_ohlc_id_seq; Type: SEQUENCE; Schema: public; Owner: developer
--

CREATE SEQUENCE public.coinbase_ohlc_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.coinbase_ohlc_id_seq OWNER TO developer;

--
-- TOC entry 3367 (class 0 OID 0)
-- Dependencies: 218
-- Name: coinbase_ohlc_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: developer
--

ALTER SEQUENCE public.coinbase_ohlc_id_seq OWNED BY public.coinbase_ohlc.id;


--
-- TOC entry 3212 (class 2604 OID 16468)
-- Name: coinbase_ohlc id; Type: DEFAULT; Schema: public; Owner: developer
--

ALTER TABLE ONLY public.coinbase_ohlc ALTER COLUMN id SET DEFAULT nextval('public.coinbase_ohlc_id_seq'::regclass);


--
-- TOC entry 3214 (class 2606 OID 16476)
-- Name: coinbase_ohlc coinbase_ohlc_pkey; Type: CONSTRAINT; Schema: public; Owner: developer
--

ALTER TABLE ONLY public.coinbase_ohlc
    ADD CONSTRAINT coinbase_ohlc_pkey PRIMARY KEY (id);


--
-- TOC entry 3216 (class 2606 OID 16490)
-- Name: coinbase_ohlc unique_timestamp_symbol_granularity; Type: CONSTRAINT; Schema: public; Owner: developer
--

ALTER TABLE ONLY public.coinbase_ohlc
    ADD CONSTRAINT unique_timestamp_symbol_granularity UNIQUE (epoctimestamp, symbol, granularity);


-- Completed on 2025-08-12 22:03:30 EDT

--
-- PostgreSQL database dump complete
--

