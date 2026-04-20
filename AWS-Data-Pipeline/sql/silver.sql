CREATE OR REPLACE VIEW uber.silver_obt AS
SELECT DISTINCT
    ride_id,
    passenger_id,
    driver_id,
    vehicle_id,

    date_parse(replace(substr(booking_timestamp,1,19),'T',' '), '%Y-%m-%d %H:%i:%s') AS booking_time,

    distance_miles,
    duration_minutes,
    total_fare,
    tip_amount,
    surge_multiplier,

    (total_fare - tip_amount) AS net_fare

FROM uber.bronze_rides;