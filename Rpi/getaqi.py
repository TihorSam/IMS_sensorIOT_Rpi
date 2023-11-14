def calculate_aqi_pm(pm_value, pm_breakpoints):
    # Find the appropriate AQI range for PM value
    for i in range(len(pm_breakpoints) - 1):
        if pm_value >= pm_breakpoints[i] and pm_value <= pm_breakpoints[i + 1]:
            C_low, C_high = pm_breakpoints[i], pm_breakpoints[i + 1]
            I_low, I_high = i, i + 1
            break

    # Calculate AQI for PM value
    aqi = ((I_high - I_low) / (C_high - C_low)) * (pm_value - C_low) + I_low
    return round(aqi)

def calculate_aqi_co2(co2_value, co2_breakpoints):
    # Find the appropriate AQI range for CO2 value
    for i in range(len(co2_breakpoints) - 1):
        if co2_value >= co2_breakpoints[i] and co2_value <= co2_breakpoints[i + 1]:
            C_low, C_high = co2_breakpoints[i], co2_breakpoints[i + 1]
            I_low, I_high = i, i + 1
            break

    # Calculate AQI for CO2 value
    aqi = ((I_high - I_low) / (C_high - C_low)) * (co2_value - C_low) + I_low
    return round(aqi)

def calculate_overall_aqi(pm25_value, pm10_value, co2_value):
    # Define AQI breakpoints for PM2.5, PM10, and CO2
    pm25_breakpoints = [0, 12, 35.4, 55.4, 150.4, 250.4, 350.4, 500.4]
    pm10_breakpoints = [0, 54, 154, 254, 354, 424, 504, 604]
    co2_breakpoints = [0, 400, 800, 1200, 1600, 2000, 2400, 3200]

    # Calculate sub-indices for PM2.5, PM10, and CO2
    aqi_pm25 = calculate_aqi_pm(pm25_value, pm25_breakpoints)
    aqi_pm10 = calculate_aqi_pm(pm10_value, pm10_breakpoints)
    aqi_co2 = calculate_aqi_co2(co2_value, co2_breakpoints)

    # Calculate overall AQI as the maximum of the sub-indices
    overall_aqi = max(aqi_pm25, aqi_pm10, aqi_co2)
    return overall_aqi

# # Example usage:
# pm25_value = 30  # Replace with your PM2.5 value
# pm10_value = 40  # Replace with your PM10 value
# co2_value = 1000  # Replace with your CO2 value

# aqi = calculate_overall_aqi(pm25_value, pm10_value, co2_value)
# print(f"Overall AQI: {aqi}")
