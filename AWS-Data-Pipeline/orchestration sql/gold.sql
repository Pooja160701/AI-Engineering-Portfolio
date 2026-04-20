CREATE TABLE IF NOT EXISTS uber.fact_rides AS
SELECT
    ride_id,
    passenger_id,
    driver_id,
    vehicle_id,
    pickup_city_id,
    payment_method_id,
    total_fare,
    distance_miles
FROM uber.silver_obt;