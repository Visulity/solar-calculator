# calculations_engine.py
import pandas as pd
import numpy as np
from client_database import SYSTEM_MODES

class LoadCalculator:
    """Replicates the load assessment calculations from your Excel template"""
    
    def __init__(self):
        # Appliance database matching your Excel categories
        self.appliance_database = {
            "Lighting": [
                {"name": "LED Bulb", "power_w": 10, "category": "Lighting"},
                {"name": "Fluorescent Tube", "power_w": 40, "category": "Lighting"},
                {"name": "Street Light", "power_w": 50, "category": "Lighting"},
            ],
            "Entertainment": [
                {"name": "TV", "power_w": 100, "category": "Entertainment"},
                {"name": "Decoder", "power_w": 20, "category": "Entertainment"},
                {"name": "Sound System", "power_w": 200, "category": "Entertainment"},
            ],
            "Kitchen": [
                {"name": "Refrigerator", "power_w": 150, "category": "Kitchen"},
                {"name": "Blender", "power_w": 300, "category": "Kitchen"},
                {"name": "Microwave", "power_w": 1000, "category": "Kitchen"},
                {"name": "Electric Kettle", "power_w": 1500, "category": "Kitchen"},
            ],
            "Computing": [
                {"name": "Laptop", "power_w": 60, "category": "Computing"},
                {"name": "Desktop Computer", "power_w": 200, "category": "Computing"},
                {"name": "Printer", "power_w": 50, "category": "Computing"},
                {"name": "Router", "power_w": 10, "category": "Computing"},
            ],
            "HVAC": [
                {"name": "Ceiling Fan", "power_w": 75, "category": "HVAC"},
                {"name": "Standing Fan", "power_w": 60, "category": "HVAC"},
                {"name": "1HP AC Unit", "power_w": 750, "category": "HVAC"},
                {"name": "1.5HP AC Unit", "power_w": 1125, "category": "HVAC"},
            ],
            "Water Systems": [
                {"name": "Water Pump 0.5HP", "power_w": 375, "category": "Water Systems"},
                {"name": "Water Pump 1HP", "power_w": 750, "category": "Water Systems"},
                {"name": "Water Heater", "power_w": 2000, "category": "Water Systems"},
            ],
            "Industrial": [
                {"name": "Industrial Machine", "power_w": 1500, "category": "Industrial"},
                {"name": "Welding Machine", "power_w": 2000, "category": "Industrial"},
                {"name": "Compressor", "power_w": 750, "category": "Industrial"},
            ]
        }
    
    def calculate_load_assessment(self, appliances_list):
        """
        Replicates your Excel load assessment calculations
        Input: List of appliances with [name, power_w, quantity, hours_per_day]
        Returns: Total daily energy and peak load matching your Excel formulas
        """
        
        # Initialize totals (matching your Excel columns)
        total_daily_energy_wh = 0
        total_connected_load_w = 0
        
        # Calculate for each appliance (matching your Excel formulas)
        load_details = []
        for appliance in appliances_list:
            name = appliance['name']
            power_w = appliance['power_w']
            quantity = appliance['quantity']
            hours = appliance['hours_per_day']
            
            # Daily energy calculation (matches your Excel: =Power * Quantity * Hours)
            daily_energy = power_w * quantity * hours
            
            # Connected load (matches your Excel: =Power * Quantity)
            connected_load = power_w * quantity
            
            total_daily_energy_wh += daily_energy
            total_connected_load_w += connected_load
            
            load_details.append({
                'Appliance': name,
                'Power (W)': power_w,
                'Quantity': quantity,
                'Hours/Day': hours,
                'Daily Energy (Wh)': daily_energy,
                'Connected Load (W)': connected_load
            })
        
        # Convert to kWh (matching your Excel conversion)
        total_daily_energy_kwh = total_daily_energy_wh / 1000
        
        return {
            'load_details': pd.DataFrame(load_details),
            'total_daily_energy_wh': total_daily_energy_wh,
            'total_daily_energy_kwh': total_daily_energy_kwh,
            'total_connected_load_w': total_connected_load_w,
            'peak_load_w': total_connected_load_w
        }
    
    def get_appliance_suggestions(self, category=None):
        """Get appliance suggestions by category (matching your Excel categories)"""
        if category:
            return self.appliance_database.get(category, [])
        else:
            # Return all appliances flattened
            all_appliances = []
            for category_items in self.appliance_database.values():
                all_appliances.extend(category_items)
            return all_appliances

class SolarSizer:
    """Complete solar system sizing calculations matching your Excel template"""
    
    def __init__(self):
        # African solar database with major Nigerian cities
        self.african_solar_db = {
            "Lagos": {"daily_sun_hours": 5.2, "source": "NASA POWER"},
            "Abuja": {"daily_sun_hours": 5.5, "source": "NASA POWER"}, 
            "Kano": {"daily_sun_hours": 5.8, "source": "NASA POWER"},
            "Port Harcourt": {"daily_sun_hours": 4.8, "source": "NASA POWER"},
            "Ibadan": {"daily_sun_hours": 5.3, "source": "NASA POWER"},
            "Benin City": {"daily_sun_hours": 5.1, "source": "NASA POWER"},
            "Kaduna": {"daily_sun_hours": 5.6, "source": "NASA POWER"},
            "Maiduguri": {"daily_sun_hours": 5.9, "source": "NASA POWER"},
            "Default": {"daily_sun_hours": 5.0, "source": "Average Nigeria"}
        }
        
        # Battery specifications based on your system modes
        self.battery_specs = {
            "lead-acid": {"dod": 0.5, "efficiency": 0.85, "voltage_options": [6, 12]},
            "lithium": {"dod": 0.8, "efficiency": 0.95, "voltage_options": [12, 24, 48, 51.2]}
        }
    
    def get_solar_data(self, location):
        """Get solar data for African location"""
        location_key = location.title()
        return self.african_solar_db.get(location_key, self.african_solar_db["Default"])
    
    def calculate_solar_requirements(self, daily_energy_wh, location, system_mode, 
                                   days_autonomy=2, system_efficiency=0.8):
        """
        Complete solar system sizing matching your Excel formulas
        """
        # Get solar data for location
        solar_data = self.get_solar_data(location)
        sun_hours = solar_data["daily_sun_hours"]
        
        # Solar panel sizing (matches your Excel: =Daily_Energy / (Sun_Hours * Efficiency))
        required_solar_wattage = daily_energy_wh / (sun_hours * system_efficiency)
        
        # Get system mode configuration
        mode_config = SYSTEM_MODES[system_mode]
        system_voltage = mode_config["voltage"]
        battery_type = mode_config["battery_type"]
        
        # Battery bank sizing (matches your Excel logic)
        battery_spec = self.battery_specs[battery_type]
        usable_energy_per_day = daily_energy_wh / battery_spec["efficiency"]
        total_usable_energy = usable_energy_per_day * days_autonomy
        battery_capacity_ah = total_usable_energy / (system_voltage * battery_spec["dod"])
        
        # Inverter sizing (with 25% safety margin as per industry standard)
        inverter_power_w = daily_energy_wh / 5 * 1.25  # Based on 5-hour usage peak
        inverter_size_kva = inverter_power_w / 1000
        
        # Charge controller sizing
        charge_controller_current = required_solar_wattage / system_voltage * 1.25  # 25% safety margin
        
        return {
            'required_solar_w': required_solar_wattage,
            'required_solar_kw': required_solar_wattage / 1000,
            'sun_hours_used': sun_hours,
            'system_voltage': system_voltage,
            'battery_type': battery_type,
            'battery_capacity_ah': battery_capacity_ah,
            'battery_capacity_kwh': (battery_capacity_ah * system_voltage) / 1000,
            'inverter_size_kva': inverter_size_kva,
            'charge_controller_a': charge_controller_current,
            'days_autonomy': days_autonomy,
            'system_efficiency': system_efficiency
        }
    
    def calculate_battery_configuration(self, battery_capacity_ah, system_voltage, battery_type):
        """
        Calculate series/parallel battery configuration
        Matches your Excel battery arrangement logic
        """
        # Common battery sizes
        common_batteries = {
            "lead-acid": [100, 150, 200, 250],
            "lithium": [100, 200, 300, 400, 500]
        }
        
        # Find optimal battery size
        available_sizes = common_batteries[battery_type]
        optimal_size = min(available_sizes, key=lambda x: abs(x - battery_capacity_ah/2))
        
        # Calculate configuration
        batteries_in_parallel = max(1, int(np.ceil(battery_capacity_ah / optimal_size)))
        
        if battery_type == "lithium" and system_voltage == 48:
            batteries_in_series = 4  # 12V batteries in series for 48V system
        elif battery_type == "lithium" and system_voltage == 24:
            batteries_in_series = 2
        else:
            batteries_in_series = 1  # 12V systems or lead-acid
        
        total_batteries = batteries_in_series * batteries_in_parallel
        actual_capacity_ah = optimal_size * batteries_in_parallel
        
        return {
            'batteries_in_series': batteries_in_series,
            'batteries_in_parallel': batteries_in_parallel,
            'total_batteries': total_batteries,
            'battery_size_ah': optimal_size,
            'actual_capacity_ah': actual_capacity_ah,
            'configuration': f"{batteries_in_series}S × {batteries_in_parallel}P"
        }

class ProductRecommender:
    """Recommends actual products from your solar_products.csv"""
    
    def __init__(self):
        self.products = pd.read_csv("solar_products.csv")
    
    def recommend_panels(self, required_power_w, panel_type="mono"):
        """Recommend solar panels based on required power"""
        panels = self.products[
            (self.products['category'] == 'panel') & 
            (self.products['type'] == panel_type)
        ]
        
        if panels.empty:
            return None
            
        # Find panels that meet or slightly exceed requirement
        suitable_panels = panels[panels['capacity'] >= required_power_w * 0.8]
        if suitable_panels.empty:
            suitable_panels = panels.nlargest(3, 'capacity')
        
        return suitable_panels.head(3)
    
    def recommend_inverters(self, required_kva, system_voltage, inverter_type="hybrid"):
        """Recommend inverters based on system requirements"""
        inverters = self.products[
            (self.products['category'] == 'inverter') & 
            (self.products['voltage'] == system_voltage) &
            (self.products['type'] == inverter_type)
        ]
        
        if inverters.empty:
            return None
            
        # Find inverters that meet the requirement
        suitable_inverters = inverters[inverters['capacity'] >= required_kva * 1000 * 0.9]
        if suitable_inverters.empty:
            suitable_inverters = inverters.nlargest(3, 'capacity')
        
        return suitable_inverters.head(3)

# Enhanced test function
def test_complete_system():
    """Test the complete solar system calculations"""
    load_calc = LoadCalculator()
    solar_sizer = SolarSizer()
    recommender = ProductRecommender()
    
    # Test load calculation
    test_appliances = [
        {'name': 'LED Bulb', 'power_w': 10, 'quantity': 10, 'hours_per_day': 6},
        {'name': 'TV', 'power_w': 100, 'quantity': 2, 'hours_per_day': 5},
        {'name': 'Refrigerator', 'power_w': 150, 'quantity': 1, 'hours_per_day': 24},
    ]
    
    load_results = load_calc.calculate_load_assessment(test_appliances)
    
    # Test solar sizing
    solar_results = solar_sizer.calculate_solar_requirements(
        daily_energy_wh=load_results['total_daily_energy_wh'],
        location="Lagos",
        system_mode="Standard Setup (Retail/Medium Business)",
        days_autonomy=2
    )
    
    # Test battery configuration
    battery_config = solar_sizer.calculate_battery_configuration(
        battery_capacity_ah=solar_results['battery_capacity_ah'],
        system_voltage=solar_results['system_voltage'],
        battery_type=solar_results['battery_type']
    )
    
    print("=== COMPLETE SYSTEM TEST ===")
    print(f"📍 Location: Lagos")
    print(f"💡 Daily Energy: {load_results['total_daily_energy_kwh']:.1f} kWh")
    print(f"☀️ Required Solar: {solar_results['required_solar_kw']:.1f} kW")
    print(f"🔋 Battery Capacity: {solar_results['battery_capacity_kwh']:.1f} kWh")
    print(f"⚡ Inverter Size: {solar_results['inverter_size_kva']:.1f} kVA")
    print(f"🔧 Battery Config: {battery_config['configuration']}")
    print(f"📊 System Voltage: {solar_results['system_voltage']}V")
    print(f"🔋 Battery Type: {solar_results['battery_type']}")

if __name__ == "__main__":
    test_complete_system()