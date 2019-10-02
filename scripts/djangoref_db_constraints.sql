--
-- TOC entry 4700 (class 2606 OID 408689)
-- Name: epsg_coordinatereferencesystem fk_area_of_use_code; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_coordinatereferencesystem
    ADD CONSTRAINT fk_area_of_use_code FOREIGN KEY (area_of_use_code) REFERENCES public.epsg_area(area_code) MATCH FULL;


--
-- TOC entry 4706 (class 2606 OID 408694)
-- Name: epsg_datum fk_area_of_use_code2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_datum
    ADD CONSTRAINT fk_area_of_use_code2 FOREIGN KEY (area_of_use_code) REFERENCES public.epsg_area(area_code) MATCH FULL;


--
-- TOC entry 4701 (class 2606 OID 408719)
-- Name: epsg_coordinatereferencesystem fk_cmpd_horizcrs_code; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_coordinatereferencesystem
    ADD CONSTRAINT fk_cmpd_horizcrs_code FOREIGN KEY (cmpd_horizcrs_code) REFERENCES public.epsg_coordinatereferencesystem(coord_ref_sys_code) MATCH FULL;


--
-- TOC entry 4702 (class 2606 OID 408724)
-- Name: epsg_coordinatereferencesystem fk_cmpd_vertcrs_code; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_coordinatereferencesystem
    ADD CONSTRAINT fk_cmpd_vertcrs_code FOREIGN KEY (cmpd_vertcrs_code) REFERENCES public.epsg_coordinatereferencesystem(coord_ref_sys_code) MATCH FULL;


--
-- TOC entry 4703 (class 2606 OID 408759)
-- Name: epsg_coordinatereferencesystem fk_coord_sys_code2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_coordinatereferencesystem
    ADD CONSTRAINT fk_coord_sys_code2 FOREIGN KEY (coord_sys_code) REFERENCES public.epsg_coordinatesystem(coord_sys_code) MATCH FULL;


--
-- TOC entry 4704 (class 2606 OID 408764)
-- Name: epsg_coordinatereferencesystem fk_datum_code; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_coordinatereferencesystem
    ADD CONSTRAINT fk_datum_code FOREIGN KEY (datum_code) REFERENCES public.epsg_datum(datum_code) MATCH FULL;


--
-- TOC entry 4707 (class 2606 OID 408769)
-- Name: epsg_datum fk_ellipsoid_code; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_datum
    ADD CONSTRAINT fk_ellipsoid_code FOREIGN KEY (ellipsoid_code) REFERENCES public.epsg_ellipsoid(ellipsoid_code) MATCH FULL;


--
-- TOC entry 4708 (class 2606 OID 408789)
-- Name: epsg_datum fk_prime_meridian_code; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_datum
    ADD CONSTRAINT fk_prime_meridian_code FOREIGN KEY (prime_meridian_code) REFERENCES public.epsg_primemeridian(prime_meridian_code) MATCH FULL;


--
-- TOC entry 4705 (class 2606 OID 408804)
-- Name: epsg_coordinatereferencesystem fk_source_geogcrs_code; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_coordinatereferencesystem
    ADD CONSTRAINT fk_source_geogcrs_code FOREIGN KEY (source_geogcrs_code) REFERENCES public.epsg_coordinatereferencesystem(coord_ref_sys_code) MATCH FULL;


--
-- TOC entry 4711 (class 2606 OID 408814)
-- Name: epsg_unitofmeasure fk_target_uom_code; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_unitofmeasure
    ADD CONSTRAINT fk_target_uom_code FOREIGN KEY (target_uom_code) REFERENCES public.epsg_unitofmeasure(uom_code) MATCH FULL;


--
-- TOC entry 4710 (class 2606 OID 408819)
-- Name: epsg_primemeridian fk_uom_code; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_primemeridian
    ADD CONSTRAINT fk_uom_code FOREIGN KEY (uom_code) REFERENCES public.epsg_unitofmeasure(uom_code) MATCH FULL;


--
-- TOC entry 4709 (class 2606 OID 408834)
-- Name: epsg_ellipsoid fk_uom_code4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epsg_ellipsoid
    ADD CONSTRAINT fk_uom_code4 FOREIGN KEY (uom_code) REFERENCES public.epsg_unitofmeasure(uom_code) MATCH FULL;


--
-- TOC entry 4695 (class 2606 OID 408869)
-- Name: autorrecursgeoref fkautorrecursgeorefa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.autorrecursgeoref
    ADD CONSTRAINT fkautorrecursgeorefa FOREIGN KEY (idpersona) REFERENCES public.georef_addenda_autor(id) MATCH FULL;


--
-- TOC entry 4696 (class 2606 OID 408874)
-- Name: autorrecursgeoref fkautorrecursgeorefr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.autorrecursgeoref
    ADD CONSTRAINT fkautorrecursgeorefr FOREIGN KEY (idrecursgeoref) REFERENCES public.recursgeoref(id) MATCH FULL ON DELETE CASCADE;


--
-- TOC entry 4697 (class 2606 OID 408884)
-- Name: capesrecurs fkcapareccapa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.capesrecurs
    ADD CONSTRAINT fkcapareccapa FOREIGN KEY (idcapa) REFERENCES public.capawms(id) MATCH FULL;


--
-- TOC entry 4698 (class 2606 OID 408889)
-- Name: capesrecurs fkcaparecrec; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.capesrecurs
    ADD CONSTRAINT fkcaparecrec FOREIGN KEY (idrecurs) REFERENCES public.recursgeoref(id) MATCH FULL;


--
-- TOC entry 4699 (class 2606 OID 408919)
-- Name: comments fkcommentversio; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT fkcommentversio FOREIGN KEY (idversio) REFERENCES public.toponimversio(id) ON DELETE CASCADE;


--
-- TOC entry 4725 (class 2606 OID 409054)
-- Name: toponim fkpaistoponim; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toponim
    ADD CONSTRAINT fkpaistoponim FOREIGN KEY (idpais) REFERENCES public.pais(id) MATCH FULL DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 4726 (class 2606 OID 409059)
-- Name: toponim fkparetoponim; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toponim
    ADD CONSTRAINT fkparetoponim FOREIGN KEY (idpare) REFERENCES public.toponim(id) MATCH FULL ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 4728 (class 2606 OID 409159)
-- Name: toponimversio fkqualificadorsversioqualificadors; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toponimversio
    ADD CONSTRAINT fkqualificadorsversioqualificadors FOREIGN KEY (idqualificador) REFERENCES public.qualificadorversio(id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4714 (class 2606 OID 409164)
-- Name: recursgeoref fkrecgeotv; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recursgeoref
    ADD CONSTRAINT fkrecgeotv FOREIGN KEY (idambit) REFERENCES public.toponimversio(id) MATCH FULL;


--
-- TOC entry 4715 (class 2606 OID 409174)
-- Name: recursgeoref fkrecursgeorefepsg; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recursgeoref
    ADD CONSTRAINT fkrecursgeorefepsg FOREIGN KEY (idsistemareferenciaepsg) REFERENCES public.sistemareferencia(id);


--
-- TOC entry 4712 (class 2606 OID 409179)
-- Name: paraulaclaurecursgeoref fkrecursgeorefparaula; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paraulaclaurecursgeoref
    ADD CONSTRAINT fkrecursgeorefparaula FOREIGN KEY (idparaula) REFERENCES public.paraulaclau(id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4713 (class 2606 OID 409184)
-- Name: paraulaclaurecursgeoref fkrecursgeorefrecursgeoref; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.paraulaclaurecursgeoref
    ADD CONSTRAINT fkrecursgeorefrecursgeoref FOREIGN KEY (idrecursgeoref) REFERENCES public.recursgeoref(id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4716 (class 2606 OID 409189)
-- Name: recursgeoref fkrecursgeorefs; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recursgeoref
    ADD CONSTRAINT fkrecursgeorefs FOREIGN KEY (idsuport) REFERENCES public.suport(id) MATCH FULL;


--
-- TOC entry 4720 (class 2606 OID 409194)
-- Name: recursgeoreftoponim fkrecursgeoreftoponimrg; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recursgeoreftoponim
    ADD CONSTRAINT fkrecursgeoreftoponimrg FOREIGN KEY (idrecursgeoref) REFERENCES public.recursgeoref(id) ON DELETE CASCADE;


--
-- TOC entry 4721 (class 2606 OID 409199)
-- Name: recursgeoreftoponim fkrecursgeoreftoponimt; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recursgeoreftoponim
    ADD CONSTRAINT fkrecursgeoreftoponimt FOREIGN KEY (idtoponim) REFERENCES public.toponim(id) MATCH FULL ON DELETE CASCADE;


--
-- TOC entry 4717 (class 2606 OID 409204)
-- Name: recursgeoref fkrecursgeoreftr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recursgeoref
    ADD CONSTRAINT fkrecursgeoreftr FOREIGN KEY (idtipusrecursgeoref) REFERENCES public.tipusrecursgeoref(id) MATCH FULL;


--
-- TOC entry 4718 (class 2606 OID 409209)
-- Name: recursgeoref fkrecurssistemarefmm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recursgeoref
    ADD CONSTRAINT fkrecurssistemarefmm FOREIGN KEY (idsistemareferenciamm) REFERENCES public.sistemareferenciamm(id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4719 (class 2606 OID 409214)
-- Name: recursgeoref fkrecurstipusunitat; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.recursgeoref
    ADD CONSTRAINT fkrecurstipusunitat FOREIGN KEY (idtipusunitatscarto) REFERENCES public.tipusunitats(id) MATCH FULL ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4722 (class 2606 OID 409239)
-- Name: sistemareferencia fksistemareferenciaepsg; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sistemareferencia
    ADD CONSTRAINT fksistemareferenciaepsg FOREIGN KEY (idepsg) REFERENCES public.epsg_coordinatereferencesystem(coord_ref_sys_code) MATCH FULL;


--
-- TOC entry 4723 (class 2606 OID 409244)
-- Name: sistemareferenciarecurs fksistemareferenciarecursrg; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sistemareferenciarecurs
    ADD CONSTRAINT fksistemareferenciarecursrg FOREIGN KEY (idrecursgeoref) REFERENCES public.recursgeoref(id) MATCH FULL ON DELETE CASCADE;


--
-- TOC entry 4724 (class 2606 OID 409249)
-- Name: sistemareferenciarecurs fksistemareferenciarecurssrmm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sistemareferenciarecurs
    ADD CONSTRAINT fksistemareferenciarecurssrmm FOREIGN KEY (idsistemareferenciamm) REFERENCES public.sistemareferenciamm(id) MATCH FULL ON DELETE CASCADE;


--
-- TOC entry 4727 (class 2606 OID 409269)
-- Name: toponim fktoponimtt; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toponim
    ADD CONSTRAINT fktoponimtt FOREIGN KEY (idtipustoponim) REFERENCES public.tipustoponim(id) MATCH FULL;


--
-- TOC entry 4729 (class 2606 OID 409274)
-- Name: toponimversio fktoponimversiotoponim; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toponimversio
    ADD CONSTRAINT fktoponimversiotoponim FOREIGN KEY (idtoponim) REFERENCES public.toponim(id) MATCH FULL ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 4730 (class 2606 OID 409284)
-- Name: toponimversio fktvrecgeo; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toponimversio
    ADD CONSTRAINT fktvrecgeo FOREIGN KEY (idrecursgeoref) REFERENCES public.recursgeoref(id);


--
-- TOC entry 4732 (class 2606 OID 409289)
-- Name: toponimsversiorecurs fktvrrecursgeoref; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toponimsversiorecurs
    ADD CONSTRAINT fktvrrecursgeoref FOREIGN KEY (idrecursgeoref) REFERENCES public.recursgeoref(id) MATCH FULL;


--
-- TOC entry 4731 (class 2606 OID 409294)
-- Name: toponimversio fktvsistrefmm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.toponimversio
    ADD CONSTRAINT fktvsistrefmm FOREIGN KEY (idsistemareferenciarecurs) REFERENCES public.sistemareferenciarecurs(id);