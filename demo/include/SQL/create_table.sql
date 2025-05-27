DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'cleaned_canada'
    ) THEN
        CREATE TABLE cleaned_canada (
            city TEXT,
            province TEXT,
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION,
            price DOUBLE PRECISION,
            bedrooms DOUBLE PRECISION,
            bathrooms DOUBLE PRECISION,
            acreage DOUBLE PRECISION,
            property_type TEXT,
            square_footage DOUBLE PRECISION,
            garage TEXT,
            parking TEXT,
            basement TEXT,
            exterior TEXT,
            fireplace TEXT,
            heating TEXT,
            flooring TEXT,
            roof TEXT,
            waterfront TEXT,
            sewer TEXT,
            pool TEXT,
            garden TEXT,
            view TEXT,
            balcony TEXT
        );
    END IF;
END $$;
