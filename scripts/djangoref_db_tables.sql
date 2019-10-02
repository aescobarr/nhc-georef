--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

-- Started on 2019-10-01 16:37:24 CEST

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
-- TOC entry 232 (class 1259 OID 406643)
-- Name: authority; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.authority (
    id character varying(100) NOT NULL,
    authority character varying(100)
);


--
-- TOC entry 233 (class 1259 OID 406646)
-- Name: autorrecursgeoref; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.autorrecursgeoref (
    id character varying(100) NOT NULL,
    idrecursgeoref character varying(100) NOT NULL,
    idpersona character varying(100) NOT NULL
);


--
-- TOC entry 234 (class 1259 OID 406658)
-- Name: capawms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.capawms (
    id character varying(200) NOT NULL,
    baseurlservidor character varying(400) NOT NULL,
    name character varying(400) NOT NULL,
    label character varying(400),
    minx double precision,
    maxx double precision,
    miny double precision,
    maxy double precision,
    boundary public.geometry(Polygon,4326)
);


--
-- TOC entry 235 (class 1259 OID 406664)
-- Name: capesrecurs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.capesrecurs (
    idcapa character varying(200),
    idrecurs character varying(200),
    id character varying(200) NOT NULL
);


--
-- TOC entry 236 (class 1259 OID 406685)
-- Name: comments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.comments (
    id integer NOT NULL,
    comment text,
    data date,
    attachment character varying(500),
    nom_original character varying(500),
    author character varying(500),
    idversio character varying(200)
);


--
-- TOC entry 237 (class 1259 OID 406691)
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4872 (class 0 OID 0)
-- Dependencies: 237
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;


--
-- TOC entry 238 (class 1259 OID 406717)
-- Name: datum; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.datum (
    id character varying(100) NOT NULL,
    nom character varying(100) NOT NULL,
    codi character varying(100) NOT NULL,
    idmarcreferencia character varying(100)
);


--
-- TOC entry 246 (class 1259 OID 406766)
-- Name: epsg_area; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.epsg_area (
    area_code integer NOT NULL,
    area_name character varying(80) NOT NULL,
    area_of_use text NOT NULL,
    area_south_bound_lat double precision,
    area_north_bound_lat double precision,
    area_west_bound_lon double precision,
    area_east_bound_lon double precision,
    area_polygon_file_ref character varying(254),
    iso_a2_code character varying(2),
    iso_a3_code character varying(3),
    iso_n_code integer,
    remarks character varying(254),
    information_source character varying(254),
    data_source character varying(40) NOT NULL,
    revision_date date NOT NULL,
    change_id character varying(255),
    deprecated smallint NOT NULL
);


--
-- TOC entry 247 (class 1259 OID 406787)
-- Name: epsg_coordinatereferencesystem; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.epsg_coordinatereferencesystem (
    coord_ref_sys_code integer NOT NULL,
    coord_ref_sys_name character varying(80) NOT NULL,
    area_of_use_code integer NOT NULL,
    coord_ref_sys_kind character varying(24) NOT NULL,
    coord_sys_code integer,
    datum_code integer,
    source_geogcrs_code integer,
    projection_conv_code integer,
    cmpd_horizcrs_code integer,
    cmpd_vertcrs_code integer,
    crs_scope character varying(254) NOT NULL,
    remarks character varying(254),
    information_source character varying(254),
    data_source character varying(40) NOT NULL,
    revision_date date NOT NULL,
    change_id character varying(255),
    show_crs smallint NOT NULL,
    deprecated smallint NOT NULL
);


--
-- TOC entry 248 (class 1259 OID 406793)
-- Name: epsg_coordinatesystem; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.epsg_coordinatesystem (
    coord_sys_code integer NOT NULL,
    coord_sys_name character varying(254) NOT NULL,
    coord_sys_type character varying(24) NOT NULL,
    dimension smallint NOT NULL,
    remarks character varying(254),
    information_source character varying(254),
    data_source character varying(50) NOT NULL,
    revision_date date NOT NULL,
    change_id character varying(255),
    deprecated smallint NOT NULL
);


--
-- TOC entry 249 (class 1259 OID 406826)
-- Name: epsg_datum; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.epsg_datum (
    datum_code integer NOT NULL,
    datum_name character varying(80) NOT NULL,
    datum_type character varying(24) NOT NULL,
    origin_description character varying(254),
    realization_epoch character varying(4),
    ellipsoid_code integer,
    prime_meridian_code integer,
    area_of_use_code integer NOT NULL,
    datum_scope character varying(254) NOT NULL,
    remarks character varying(254),
    information_source character varying(254),
    data_source character varying(40) NOT NULL,
    revision_date date NOT NULL,
    change_id character varying(255),
    deprecated smallint NOT NULL
);


--
-- TOC entry 250 (class 1259 OID 406836)
-- Name: epsg_ellipsoid; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.epsg_ellipsoid (
    ellipsoid_code integer NOT NULL,
    ellipsoid_name character varying(80) NOT NULL,
    semi_major_axis double precision NOT NULL,
    uom_code integer NOT NULL,
    inv_flattening double precision,
    semi_minor_axis double precision,
    ellipsoid_shape smallint NOT NULL,
    remarks character varying(254),
    information_source character varying(254),
    data_source character varying(40) NOT NULL,
    revision_date date NOT NULL,
    change_id character varying(255),
    deprecated smallint NOT NULL
);


--
-- TOC entry 251 (class 1259 OID 406848)
-- Name: epsg_primemeridian; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.epsg_primemeridian (
    prime_meridian_code integer NOT NULL,
    prime_meridian_name character varying(80) NOT NULL,
    greenwich_longitude double precision NOT NULL,
    uom_code integer NOT NULL,
    remarks character varying(254),
    information_source character varying(254),
    data_source character varying(40) NOT NULL,
    revision_date date NOT NULL,
    change_id character varying(255),
    deprecated smallint NOT NULL
);


--
-- TOC entry 252 (class 1259 OID 406858)
-- Name: epsg_unitofmeasure; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.epsg_unitofmeasure (
    uom_code integer NOT NULL,
    unit_of_meas_name character varying(80) NOT NULL,
    unit_of_meas_type character varying(50),
    target_uom_code integer NOT NULL,
    factor_b double precision,
    factor_c double precision,
    remarks character varying(254),
    information_source character varying(254),
    data_source character varying(40) NOT NULL,
    revision_date date NOT NULL,
    change_id character varying(255),
    deprecated smallint NOT NULL
);


--
-- TOC entry 253 (class 1259 OID 406867)
-- Name: filtrejson; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.filtrejson (
    idfiltre character varying(100) NOT NULL,
    json text,
    modul character varying(100),
    nomfiltre character varying(200)
);


--
-- TOC entry 254 (class 1259 OID 406888)
-- Name: geometries_api; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.geometries_api (
    id character varying(200) NOT NULL,
    geometria public.geometry(Geometry,4326) NOT NULL
);


--
-- TOC entry 264 (class 1259 OID 406959)
-- Name: pais; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pais (
    id character varying(100) NOT NULL,
    nom character varying(200) NOT NULL
);


--
-- TOC entry 265 (class 1259 OID 406962)
-- Name: paraulaclau; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.paraulaclau (
    id character varying(100) NOT NULL,
    paraula character varying(500) NOT NULL
);


--
-- TOC entry 266 (class 1259 OID 406968)
-- Name: paraulaclaurecursgeoref; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.paraulaclaurecursgeoref (
    id character varying(100) NOT NULL,
    idrecursgeoref character varying(100) NOT NULL,
    idparaula character varying(100) NOT NULL
);


--
-- TOC entry 267 (class 1259 OID 406995)
-- Name: prefs_visibilitat_capes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prefs_visibilitat_capes (
    id character varying(100) NOT NULL,
    prefscapesjson text,
    iduser integer
);


--
-- TOC entry 268 (class 1259 OID 407025)
-- Name: qualificadorversio; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.qualificadorversio (
    id character varying(100) NOT NULL,
    qualificador character varying(500) NOT NULL
);


--
-- TOC entry 269 (class 1259 OID 407031)
-- Name: recursgeoref; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recursgeoref (
    id character varying(100) NOT NULL,
    nom character varying(500) NOT NULL,
    idtipusrecursgeoref character varying(100),
    comentarisnoambit character varying(500),
    campidtoponim character varying(500),
    idsistemareferenciaepsg character varying(100),
    versio character varying(100),
    fitxergraficbase character varying(100),
    idsuport character varying(100),
    urlsuport character varying(250),
    ubicaciorecurs character varying(200),
    actualitzaciosuport character varying(250),
    mapa character varying(100),
    comentariinfo text,
    comentariconsulta text,
    comentariqualitat text,
    classificacio character varying(300),
    divisiopoliticoadministrativa character varying(300),
    idambit character varying(100),
    acronim character varying(100),
    idsistemareferenciamm character varying(100),
    idtipusunitatscarto character varying(100),
    base_url_wms character varying(255),
    capes_wms_json text,
    iduser integer
);


--
-- TOC entry 270 (class 1259 OID 407037)
-- Name: recursgeoreftoponim; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.recursgeoreftoponim (
    id character varying(100) NOT NULL,
    idrecursgeoref character varying(100) NOT NULL,
    idtoponim character varying(200)
);


--
-- TOC entry 273 (class 1259 OID 407080)
-- Name: sistemareferencia; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sistemareferencia (
    id character varying(100) NOT NULL,
    idepsg integer NOT NULL
);


--
-- TOC entry 274 (class 1259 OID 407083)
-- Name: sistemareferenciamm; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sistemareferenciamm (
    id character varying(100) NOT NULL,
    nom character varying(500) NOT NULL
);


--
-- TOC entry 275 (class 1259 OID 407089)
-- Name: sistemareferenciarecurs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sistemareferenciarecurs (
    id character varying(100) NOT NULL,
    idrecursgeoref character varying(100) NOT NULL,
    idsistemareferenciamm character varying(100),
    sistemareferencia character varying(1000),
    conversio character varying(250)
);


--
-- TOC entry 276 (class 1259 OID 407098)
-- Name: suport; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.suport (
    id character varying(100) NOT NULL,
    nom character varying(100) NOT NULL
);


--
-- TOC entry 277 (class 1259 OID 407107)
-- Name: tipusrecursgeoref; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipusrecursgeoref (
    id character varying(100) NOT NULL,
    nom character varying(100) NOT NULL
);


--
-- TOC entry 278 (class 1259 OID 407110)
-- Name: tipustoponim; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipustoponim (
    id character varying(100) NOT NULL,
    nom character varying(100) NOT NULL
);


--
-- TOC entry 279 (class 1259 OID 407113)
-- Name: tipusunitats; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipusunitats (
    id character varying(100) NOT NULL,
    tipusunitat character varying(500) NOT NULL
);


--
-- TOC entry 280 (class 1259 OID 407119)
-- Name: toponim; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.toponim (
    id character varying(200) NOT NULL,
    codi character varying(50),
    nom character varying(250) NOT NULL,
    aquatic character(1),
    idtipustoponim character varying(100) NOT NULL,
    idpais character varying(100),
    idpare character varying(200),
    nom_fitxer_importacio character varying(255),
    linia_fitxer_importacio text,
    denormalized_toponimtree text
);


--
-- TOC entry 281 (class 1259 OID 407125)
-- Name: toponims_api; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.toponims_api (
    id character varying(200) NOT NULL,
    nomtoponim character varying(255),
    nom character varying(500),
    aquatic boolean,
    tipus character varying(255),
    idtipus character varying(255),
    datacaptura date,
    coordenadaxcentroide double precision,
    coordenadaycentroide double precision,
    incertesa double precision
);


--
-- TOC entry 282 (class 1259 OID 407131)
-- Name: toponimversio; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.toponimversio (
    id character varying(200) NOT NULL,
    codi character varying(50),
    nom character varying(250) NOT NULL,
    datacaptura date,
    coordenada_x double precision,
    coordenada_y double precision,
    coordenada_z double precision,
    precisio_h double precision,
    precisio_z double precision,
    idsistemareferenciarecurs character varying(100),
    coordenada_x_origen character varying(50),
    coordenada_y_origen character varying(50),
    coordenada_z_origen character varying(50),
    precisio_h_origen character varying(50),
    precisio_z_origen character varying(50),
    idpersona character varying(100),
    observacions text,
    idrecursgeoref character varying(100),
    idtoponim character varying(200),
    numero_versio integer,
    idqualificador character varying(100),
    coordenada_x_centroide character varying(50),
    coordenada_y_centroide character varying(50),
    iduser integer,
    last_version boolean
);


--
-- TOC entry 287 (class 1259 OID 407170)
-- Name: toponimsversio_api; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.toponimsversio_api (
    id character varying(200) NOT NULL,
    nom character varying(500),
    nomtoponim character varying(255),
    tipus character varying(100),
    versio integer,
    qualificadorversio character varying(500),
    recurscaptura character varying(500),
    sistrefrecurs character varying(1000),
    datacaptura date,
    coordxoriginal character varying(100),
    coordyoriginal character varying(100),
    coordz double precision,
    incertesaz double precision,
    georeferenciatper character varying(500),
    observacions text,
    coordxcentroide double precision,
    coordycentroide double precision,
    incertesacoord double precision,
    idtoponim character varying(200)
);


--
-- TOC entry 288 (class 1259 OID 407176)
-- Name: toponimsversiorecurs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.toponimsversiorecurs (
    idrecursgeoref character varying(100),
    idtoponimversio character varying(100)
);

--
-- TOC entry 4584 (class 2604 OID 407334)
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);


--
-- TOC entry 4588 (class 2606 OID 408101)
-- Name: autorrecursgeoref autorrecursgeoref_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.autorrecursgeoref
    ADD CONSTRAINT autorrecursgeoref_pkey PRIMARY KEY (id);


--
-- TOC entry 4593 (class 2606 OID 408109)
-- Name: capawms capawms_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.capawms
    ADD CONSTRAINT capawms_pkey PRIMARY KEY (id);


--
-- TOC entry 4595 (class 2606 OID 408113)
-- Name: capesrecurs capesrecurs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.capesrecurs
    ADD CONSTRAINT capesrecurs_pkey PRIMARY KEY (id);


--
-- TOC entry 4597 (class 2606 OID 408126)
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- TOC entry 4599 (class 2606 OID 408144)
-- Name: datum datum_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.datum
    ADD CONSTRAINT datum_pkey PRIMARY KEY (id);


--
-- TOC entry 4602 (class 2606 OID 408160)
-- Name: epsg_area epsg_area_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_area
    ADD CONSTRAINT epsg_area_pkey PRIMARY KEY (area_code);


--
-- TOC entry 4604 (class 2606 OID 408171)
-- Name: epsg_coordinatereferencesystem epsg_coordinatereferencesystem_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_coordinatereferencesystem
    ADD CONSTRAINT epsg_coordinatereferencesystem_pkey PRIMARY KEY (coord_ref_sys_code);


--
-- TOC entry 4612 (class 2606 OID 408173)
-- Name: epsg_coordinatesystem epsg_coordinatesystem_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_coordinatesystem
    ADD CONSTRAINT epsg_coordinatesystem_pkey PRIMARY KEY (coord_sys_code);


--
-- TOC entry 4614 (class 2606 OID 408187)
-- Name: epsg_datum epsg_datum_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_datum
    ADD CONSTRAINT epsg_datum_pkey PRIMARY KEY (datum_code);


--
-- TOC entry 4619 (class 2606 OID 408191)
-- Name: epsg_ellipsoid epsg_ellipsoid_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_ellipsoid
    ADD CONSTRAINT epsg_ellipsoid_pkey PRIMARY KEY (ellipsoid_code);


--
-- TOC entry 4622 (class 2606 OID 408196)
-- Name: epsg_primemeridian epsg_primemeridian_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_primemeridian
    ADD CONSTRAINT epsg_primemeridian_pkey PRIMARY KEY (prime_meridian_code);


--
-- TOC entry 4625 (class 2606 OID 408200)
-- Name: epsg_unitofmeasure epsg_unitofmeasure_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_unitofmeasure
    ADD CONSTRAINT epsg_unitofmeasure_pkey PRIMARY KEY (uom_code);


--
-- TOC entry 4629 (class 2606 OID 408209)
-- Name: geometries_api geometries_api_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.geometries_api
    ADD CONSTRAINT geometries_api_pkey PRIMARY KEY (id);


--
-- TOC entry 4631 (class 2606 OID 408247)
-- Name: pais pais_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pais
    ADD CONSTRAINT pais_pkey PRIMARY KEY (id);


--
-- TOC entry 4633 (class 2606 OID 408252)
-- Name: paraulaclau paraulaclau_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paraulaclau
    ADD CONSTRAINT paraulaclau_pkey PRIMARY KEY (id);


--
-- TOC entry 4637 (class 2606 OID 408254)
-- Name: paraulaclaurecursgeoref paraulaclaurecursgeoref_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paraulaclaurecursgeoref
    ADD CONSTRAINT paraulaclaurecursgeoref_pkey PRIMARY KEY (id);


--
-- TOC entry 4586 (class 2606 OID 408257)
-- Name: authority pkauthority; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.authority
    ADD CONSTRAINT pkauthority PRIMARY KEY (id);


--
-- TOC entry 4639 (class 2606 OID 408281)
-- Name: prefs_visibilitat_capes prefs_visibilitat_capes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prefs_visibilitat_capes
    ADD CONSTRAINT prefs_visibilitat_capes_pkey PRIMARY KEY (id);


--
-- TOC entry 4641 (class 2606 OID 408300)
-- Name: qualificadorversio qualificadorversio_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.qualificadorversio
    ADD CONSTRAINT qualificadorversio_pkey PRIMARY KEY (id);


--
-- TOC entry 4649 (class 2606 OID 408302)
-- Name: recursgeoref recursgeoref_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recursgeoref
    ADD CONSTRAINT recursgeoref_pkey PRIMARY KEY (id);


--
-- TOC entry 4654 (class 2606 OID 408304)
-- Name: recursgeoreftoponim recursgeoreftoponim_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recursgeoreftoponim
    ADD CONSTRAINT recursgeoreftoponim_pkey PRIMARY KEY (id);


--
-- TOC entry 4660 (class 2606 OID 408321)
-- Name: sistemareferencia sistemareferencia_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sistemareferencia
    ADD CONSTRAINT sistemareferencia_pkey PRIMARY KEY (id);


--
-- TOC entry 4662 (class 2606 OID 408323)
-- Name: sistemareferenciamm sistemareferenciamm_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sistemareferenciamm
    ADD CONSTRAINT sistemareferenciamm_pkey PRIMARY KEY (id);


--
-- TOC entry 4666 (class 2606 OID 408325)
-- Name: sistemareferenciarecurs sistemareferenciarecurs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sistemareferenciarecurs
    ADD CONSTRAINT sistemareferenciarecurs_pkey PRIMARY KEY (id);


--
-- TOC entry 4668 (class 2606 OID 408329)
-- Name: suport suport_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.suport
    ADD CONSTRAINT suport_pkey PRIMARY KEY (id);


--
-- TOC entry 4670 (class 2606 OID 408335)
-- Name: tipusrecursgeoref tipusrecursgeoref_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipusrecursgeoref
    ADD CONSTRAINT tipusrecursgeoref_pkey PRIMARY KEY (id);


--
-- TOC entry 4672 (class 2606 OID 408337)
-- Name: tipustoponim tipustoponim_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipustoponim
    ADD CONSTRAINT tipustoponim_pkey PRIMARY KEY (id);


--
-- TOC entry 4674 (class 2606 OID 408339)
-- Name: tipusunitats tipusunitats_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipusunitats
    ADD CONSTRAINT tipusunitats_pkey PRIMARY KEY (id);


--
-- TOC entry 4679 (class 2606 OID 408341)
-- Name: toponim toponim_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toponim
    ADD CONSTRAINT toponim_pkey PRIMARY KEY (id);


--
-- TOC entry 4683 (class 2606 OID 408347)
-- Name: toponims_api toponims_api_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toponims_api
    ADD CONSTRAINT toponims_api_pkey PRIMARY KEY (id);


--
-- TOC entry 4692 (class 2606 OID 408349)
-- Name: toponimsversio_api toponimsversio_api_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toponimsversio_api
    ADD CONSTRAINT toponimsversio_api_pkey PRIMARY KEY (id);


--
-- TOC entry 4689 (class 2606 OID 408352)
-- Name: toponimversio toponimversio_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toponimversio
    ADD CONSTRAINT toponimversio_pkey PRIMARY KEY (id);


--
-- TOC entry 4591 (class 2606 OID 408364)
-- Name: autorrecursgeoref unautorrecursgeoref; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.autorrecursgeoref
    ADD CONSTRAINT unautorrecursgeoref UNIQUE (idpersona, idrecursgeoref);


--
-- TOC entry 4656 (class 2606 OID 408368)
-- Name: recursgeoreftoponim unrecursgeoreftoponim; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recursgeoreftoponim
    ADD CONSTRAINT unrecursgeoreftoponim UNIQUE (idtoponim, idrecursgeoref);


--
-- TOC entry 4605 (class 1259 OID 408456)
-- Name: fk_area_of_use_code1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fk_area_of_use_code1 ON public.epsg_coordinatereferencesystem USING btree (area_of_use_code);


--
-- TOC entry 4615 (class 1259 OID 408457)
-- Name: fk_area_of_use_code21; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fk_area_of_use_code21 ON public.epsg_datum USING btree (area_of_use_code);


--
-- TOC entry 4606 (class 1259 OID 408462)
-- Name: fk_cmpd_horizcrs_code1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fk_cmpd_horizcrs_code1 ON public.epsg_coordinatereferencesystem USING btree (cmpd_horizcrs_code);


--
-- TOC entry 4607 (class 1259 OID 408463)
-- Name: fk_cmpd_vertcrs_code1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fk_cmpd_vertcrs_code1 ON public.epsg_coordinatereferencesystem USING btree (cmpd_vertcrs_code);


--
-- TOC entry 4608 (class 1259 OID 408478)
-- Name: fk_coord_sys_code21; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fk_coord_sys_code21 ON public.epsg_coordinatereferencesystem USING btree (coord_sys_code);


--
-- TOC entry 4609 (class 1259 OID 408481)
-- Name: fk_datum_code1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fk_datum_code1 ON public.epsg_coordinatereferencesystem USING btree (datum_code);


--
-- TOC entry 4616 (class 1259 OID 408482)
-- Name: fk_ellipsoid_code1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fk_ellipsoid_code1 ON public.epsg_datum USING btree (ellipsoid_code);


--
-- TOC entry 4617 (class 1259 OID 408488)
-- Name: fk_prime_meridian_code1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fk_prime_meridian_code1 ON public.epsg_datum USING btree (prime_meridian_code);


--
-- TOC entry 4610 (class 1259 OID 408491)
-- Name: fk_source_geogcrs_code1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fk_source_geogcrs_code1 ON public.epsg_coordinatereferencesystem USING btree (source_geogcrs_code);


--
-- TOC entry 4626 (class 1259 OID 408494)
-- Name: fk_target_uom_code1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fk_target_uom_code1 ON public.epsg_unitofmeasure USING btree (target_uom_code);


--
-- TOC entry 4623 (class 1259 OID 408495)
-- Name: fk_uom_code1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fk_uom_code1 ON public.epsg_primemeridian USING btree (uom_code);


--
-- TOC entry 4620 (class 1259 OID 408498)
-- Name: fk_uom_code41; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fk_uom_code41 ON public.epsg_ellipsoid USING btree (uom_code);


--
-- TOC entry 4589 (class 1259 OID 408503)
-- Name: fkautorrecursgeorefr1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fkautorrecursgeorefr1 ON public.autorrecursgeoref USING btree (idrecursgeoref);


--
-- TOC entry 4600 (class 1259 OID 408506)
-- Name: fkdatummr1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fkdatummr1 ON public.datum USING btree (idmarcreferencia);


--
-- TOC entry 4642 (class 1259 OID 408509)
-- Name: fkrecgeotv1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fkrecgeotv1 ON public.recursgeoref USING btree (idambit);


--
-- TOC entry 4643 (class 1259 OID 408510)
-- Name: fkrecursgeorefs1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fkrecursgeorefs1 ON public.recursgeoref USING btree (idsuport);


--
-- TOC entry 4650 (class 1259 OID 408518)
-- Name: fkrecursgeoreftoponimt1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fkrecursgeoreftoponimt1 ON public.recursgeoreftoponim USING btree (idtoponim);


--
-- TOC entry 4657 (class 1259 OID 408520)
-- Name: fksistemareferenciaepsg1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fksistemareferenciaepsg1 ON public.sistemareferencia USING btree (idepsg);


--
-- TOC entry 4675 (class 1259 OID 408521)
-- Name: fktoponimos1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fktoponimos1 ON public.toponim USING btree (id);


--
-- TOC entry 4693 (class 1259 OID 408522)
-- Name: fktvrrecursgeoref1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fktvrrecursgeoref1 ON public.toponimsversiorecurs USING btree (idrecursgeoref);


--
-- TOC entry 4694 (class 1259 OID 408523)
-- Name: fktvrversio1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fktvrversio1 ON public.toponimsversiorecurs USING btree (idtoponimversio);


--
-- TOC entry 4627 (class 1259 OID 408529)
-- Name: geometries_api_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX geometries_api_idx ON public.geometries_api USING gist (geometria);


--
-- TOC entry 4680 (class 1259 OID 408538)
-- Name: idtipus_toponimapi_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idtipus_toponimapi_idx ON public.toponims_api USING btree (idtipus);


--
-- TOC entry 4690 (class 1259 OID 408539)
-- Name: idtoponim_toponimvapi_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idtoponim_toponimvapi_idx ON public.toponimsversio_api USING btree (idtoponim);


--
-- TOC entry 4676 (class 1259 OID 408540)
-- Name: idx_linia_fitxer_importacio; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_linia_fitxer_importacio ON public.toponim USING btree (linia_fitxer_importacio);


--
-- TOC entry 4644 (class 1259 OID 408590)
-- Name: idxrecursgeorefepsg; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxrecursgeorefepsg ON public.recursgeoref USING btree (idsistemareferenciaepsg);


--
-- TOC entry 4634 (class 1259 OID 408591)
-- Name: idxrecursgeorefparaula; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxrecursgeorefparaula ON public.paraulaclaurecursgeoref USING btree (idparaula);


--
-- TOC entry 4635 (class 1259 OID 408592)
-- Name: idxrecursgeorefrecursgeoref; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxrecursgeorefrecursgeoref ON public.paraulaclaurecursgeoref USING btree (idrecursgeoref);


--
-- TOC entry 4651 (class 1259 OID 408593)
-- Name: idxrecursgeoreftoponimrg; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxrecursgeoreftoponimrg ON public.recursgeoreftoponim USING btree (idrecursgeoref);


--
-- TOC entry 4652 (class 1259 OID 408594)
-- Name: idxrecursgeoreftoponimt; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxrecursgeoreftoponimt ON public.recursgeoreftoponim USING btree (idtoponim);


--
-- TOC entry 4645 (class 1259 OID 408595)
-- Name: idxrecursgeoreftr; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxrecursgeoreftr ON public.recursgeoref USING btree (idtipusrecursgeoref);


--
-- TOC entry 4646 (class 1259 OID 408596)
-- Name: idxrecurssistemarefmm; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxrecurssistemarefmm ON public.recursgeoref USING btree (idsistemareferenciamm);


--
-- TOC entry 4647 (class 1259 OID 408597)
-- Name: idxrecurstipusunitats; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxrecurstipusunitats ON public.recursgeoref USING btree (idtipusunitatscarto);


--
-- TOC entry 4658 (class 1259 OID 408603)
-- Name: idxsistemareferenciaepsg; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxsistemareferenciaepsg ON public.sistemareferencia USING btree (idepsg);


--
-- TOC entry 4663 (class 1259 OID 408604)
-- Name: idxsistemareferenciarecursrg; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxsistemareferenciarecursrg ON public.sistemareferenciarecurs USING btree (idrecursgeoref);


--
-- TOC entry 4664 (class 1259 OID 408605)
-- Name: idxsistemareferenciarecurssrmm; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxsistemareferenciarecurssrmm ON public.sistemareferenciarecurs USING btree (idsistemareferenciamm);


--
-- TOC entry 4684 (class 1259 OID 408607)
-- Name: idxtoponimr; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxtoponimr ON public.toponimversio USING btree (idrecursgeoref);


--
-- TOC entry 4677 (class 1259 OID 408608)
-- Name: idxtoponimtt; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxtoponimtt ON public.toponim USING btree (idtipustoponim);


--
-- TOC entry 4685 (class 1259 OID 408609)
-- Name: idxtoponimversioqualificador; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxtoponimversioqualificador ON public.toponimversio USING btree (idqualificador);


--
-- TOC entry 4686 (class 1259 OID 408610)
-- Name: idxtoponimvp; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxtoponimvp ON public.toponimversio USING btree (idpersona);


--
-- TOC entry 4687 (class 1259 OID 408611)
-- Name: idxtoponimvsr; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idxtoponimvsr ON public.toponimversio USING btree (idsistemareferenciarecurs);


--
-- TOC entry 4681 (class 1259 OID 408614)
-- Name: nomtoponim_toponimapi_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX nomtoponim_toponimapi_idx ON public.toponims_api USING btree (nomtoponim);

-- Completed on 2019-10-01 16:37:24 CEST

--
-- PostgreSQL database dump complete
--

