/* Remove unnecessary columns */
ALTER TABLE AIRLINE_SATISFACTION.PUBLIC.AIRLINE_SATISFACTION_CHARACTERISTICS 
    DROP COLUMN id, gender;

/* Add encoded columns */
ALTER TABLE AIRLINE_SATISFACTION.PUBLIC.AIRLINE_SATISFACTION_CHARACTERISTICS 
    ADD COLUMN customer_type_onehot INT, travel_type_onehot INT, class_type_encoded INT, satisfaction_onehot INT;

/* Fill in newly added encoded columns */
UPDATE AIRLINE_SATISFACTION.PUBLIC.AIRLINE_SATISFACTION_CHARACTERISTICS SET customer_type_onehot = CASE
    WHEN customer_type = 'Loyal Customer' THEN 0
    WHEN customer_type = 'disloyal Customer' THEN 1
END;

UPDATE AIRLINE_SATISFACTION.PUBLIC.AIRLINE_SATISFACTION_CHARACTERISTICS SET travel_type_onehot = CASE
    WHEN travel_type = 'Personal Travel' THEN 0
    WHEN travel_type = 'Business travel' THEN 1
END;

UPDATE AIRLINE_SATISFACTION.PUBLIC.AIRLINE_SATISFACTION_CHARACTERISTICS SET class_type_encoded = CASE
    WHEN class_type = 'Eco' THEN 0
    WHEN class_type = 'Eco Plus' THEN 1
    WHEN class_type = 'Business' THEN 2
END;

UPDATE AIRLINE_SATISFACTION.PUBLIC.AIRLINE_SATISFACTION_CHARACTERISTICS SET satisfaction_onehot = CASE
    WHEN satisfaction = 'neutral or dissatisfied' THEN 0
    WHEN satisfaction = 'satisfied' THEN 1
END;

/* Display table to confirm correctness */
DESC TABLE AIRLINE_SATISFACTION.PUBLIC.AIRLINE_SATISFACTION_CHARACTERISTICS;