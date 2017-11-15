DO
$$
DECLARE
    row record;
BEGIN
    FOR row IN SELECT tablename,schemaname FROM pg_tables WHERE schemaname = 'sipan_mgeneral' or schemaname = 'sipan_mgeoreferenciacio' or schemaname = 'sipan_mgeoreferenciacio' or schemaname = 'sipan_mseguretat' -- and other conditions, if needed
    LOOP
        EXECUTE 'ALTER TABLE ' || quote_ident(row.schemaname) || '.' || quote_ident(row.tablename) || ' SET SCHEMA public;';
    END LOOP;
END;
$$;