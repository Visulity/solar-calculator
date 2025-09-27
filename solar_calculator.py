# solar_calculator.py
import streamlit as st
import pandas as pd
import numpy as np
from client_database import ClientManager, SYSTEM_MODES, NIGERIAN_STATES
from calculations_engine import LoadCalculator, SolarSizer, ProductRecommender

# Page configuration
st.set_page_config(
    page_title="Professional Solar PV Calculator",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2e75b6;
        border-bottom: 3px solid #2e75b6;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-weight: 600;
    }
    .metric-card {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2e75b6;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        color: #666;
        border-top: 1px solid #ddd;
    }
    .appliance-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

class SolarCalculatorApp:
    def __init__(self):
        self.load_calc = LoadCalculator()
        self.solar_sizer = SolarSizer()
        self.product_recommender = ProductRecommender()
        self.client_manager = ClientManager()
        
        # Initialize session state
        if 'loads' not in st.session_state:
            st.session_state.loads = []
        if 'current_client' not in st.session_state:
            st.session_state.current_client = None
        if 'calculation_results' not in st.session_state:
            st.session_state.calculation_results = None

    def show_welcome(self):
        """Welcome page with app explanation"""
        st.markdown('<h1 class="main-header">Professional Solar PV System Calculator</h1>', unsafe_allow_html=True)
        st.markdown("### Design complete solar systems for commercial and residential applications")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            #### Welcome to the Professional Solar Design Calculator
            
            This tool helps you design complete off-grid solar PV systems with:
            
            - Accurate load assessment based on appliance usage
            - Location-based solar resource data for African regions
            - Professional system sizing for solar panels, batteries, and inverters
            - Actual product recommendations from leading manufacturers
            - Commercial-grade calculations matching industry standards
            
            ##### How to Use:
            1. Client Information - Enter project details and location
            2. Load Assessment - Add electrical appliances and usage patterns
            3. System Design - Review automated system sizing calculations
            4. Product Recommendations - Select from recommended components
            5. Project Summary - Export complete system specification
            """)
        
        with col2:
            st.info("""
            **Quick Start:**
            - Begin with Client Information
            - Use preset appliance categories
            - Get instant professional results
            """)

    def show_client_info(self):
        """Client information page"""
        st.markdown('<div class="section-header">Client Information</div>', unsafe_allow_html=True)
        
        with st.form("client_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Basic Information")
                name = st.text_input("Full Name *", placeholder="John Doe")
                company = st.text_input("Company/Organization", placeholder="ABC Enterprises")
                email = st.text_input("Email Address *", placeholder="john@company.com")
                phone = st.text_input("Phone Number *", placeholder="+234 XXX XXX XXXX")
            
            with col2:
                st.subheader("Project Location")
                address = st.text_input("Street Address", placeholder="123 Main Street")
                city = st.text_input("City *", placeholder="Lagos")
                state = st.selectbox("State", NIGERIAN_STATES, index=23)  # Lagos as default
                country = st.text_input("Country", value="Nigeria")
            
            st.subheader("Project Requirements")
            col3, col4 = st.columns(2)
            with col3:
                system_mode = st.selectbox("System Mode *", list(SYSTEM_MODES.keys()), 
                                         help="Select based on project scale and requirements")
            with col4:
                project_type = st.selectbox("Project Type *", 
                                          ["Residential", "Commercial", "Industrial", "Agricultural", "Institutional"])
            
            # Additional parameters
            st.subheader("Design Parameters")
            col5, col6 = st.columns(2)
            with col5:
                days_autonomy = st.slider("Days of Autonomy (Backup)", 1, 5, 2,
                                         help="Number of days system should run without sunlight")
            with col6:
                system_efficiency = st.slider("System Efficiency (%)", 70, 95, 80,
                                            help="Overall system efficiency factor")
            
            # Form submission
            if st.form_submit_button("Save Client Information", type="primary"):
                if name and email and phone and city:
                    client_data = {
                        "basic_info": {"name": name, "company": company, "email": email, "phone": phone},
                        "location_info": {"address": address, "city": city, "state": state, "country": country},
                        "project_info": {
                            "project_type": project_type, 
                            "system_mode": system_mode,
                            "days_autonomy": days_autonomy,
                            "system_efficiency": system_efficiency/100
                        }
                    }
                    client_id = self.client_manager.add_client(client_data)
                    st.session_state.current_client = client_id
                    st.success(f"Client information saved successfully! Client ID: {client_id}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (*)")

    def show_load_assessment(self):
        """Load assessment with interactive appliance input"""
        st.markdown('<div class="section-header">Load Assessment</div>', unsafe_allow_html=True)
        
        st.info("Add electrical appliances to calculate total energy consumption. Use preset categories or add custom appliances.")
        
        # Appliance input form
        with st.form("appliance_form"):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                # Category and appliance selection
                category = st.selectbox("Appliance Category", 
                                      [""] + list(self.load_calc.appliance_database.keys()))
                
                if category:
                    appliances = self.load_calc.get_appliance_suggestions(category)
                    appliance_options = [app["name"] for app in appliances]
                    selected_appliance = st.selectbox("Select Appliance", [""] + appliance_options)
                    
                    if selected_appliance:
                        # Auto-fill power for selected appliance
                        appliance_data = next(app for app in appliances if app["name"] == selected_appliance)
                        power_w = appliance_data["power_w"]
                    else:
                        power_w = st.number_input("Power Rating (W)", min_value=1, value=100)
                        selected_appliance = st.text_input("Custom Appliance Name", placeholder="e.g., Custom Device")
                else:
                    selected_appliance = st.text_input("Appliance Name *", placeholder="e.g., LED Light")
                    power_w = st.number_input("Power Rating (W) *", min_value=1, value=100)
            
            with col2:
                quantity = st.number_input("Quantity *", min_value=1, value=1)
            
            with col3:
                hours_per_day = st.number_input("Hours/Day *", min_value=1, max_value=24, value=8)
            
            with col4:
                st.write("")  # Spacer for alignment
                st.write("")
                if st.form_submit_button("Add Appliance", type="secondary"):
                    if selected_appliance and power_w and quantity and hours_per_day:
                        new_load = {
                            'name': selected_appliance,
                            'power_w': power_w,
                            'quantity': quantity,
                            'hours_per_day': hours_per_day
                        }
                        st.session_state.loads.append(new_load)
                        st.success(f"Added {selected_appliance}")
                        st.rerun()
                    else:
                        st.error("Please fill all required fields")
        
        # Display current loads
        if st.session_state.loads:
            st.subheader("Current Electrical Loads")
            
            # Calculate and display load summary
            load_results = self.load_calc.calculate_load_assessment(st.session_state.loads)
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Daily Energy", f"{load_results['total_daily_energy_kwh']:.2f} kWh")
            with col2:
                st.metric("Total Connected Load", f"{load_results['total_connected_load_w']/1000:.2f} kW")
            with col3:
                st.metric("Number of Appliances", len(st.session_state.loads))
            with col4:
                st.metric("Peak Power Demand", f"{load_results['peak_load_w']/1000:.2f} kW")
            
            # Detailed load table
            st.dataframe(load_results['load_details'], use_container_width=True)
            
            # Individual appliance cards with delete buttons
            st.subheader("Manage Appliances")
            for i, load in enumerate(st.session_state.loads):
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                    with col1:
                        st.write(f"**{load['name']}**")
                    with col2:
                        st.write(f"{load['power_w']} W")
                    with col3:
                        st.write(f"{load['quantity']} units")
                    with col4:
                        st.write(f"{load['hours_per_day']} hrs")
                    with col5:
                        if st.button("Delete", key=f"del_{i}"):
                            st.session_state.loads.pop(i)
                            st.rerun()
                    st.markdown("---")
            
            # Clear all button
            if st.button("Clear All Loads", type="primary"):
                st.session_state.loads = []
                st.rerun()
        else:
            st.info("No appliances added yet. Use the form above to add electrical loads.")

    def show_system_design(self):
        """System design calculations and results"""
        st.markdown('<div class="section-header">System Design</div>', unsafe_allow_html=True)
        
        # Check prerequisites
        if not st.session_state.current_client:
            st.warning("Please complete Client Information first.")
            return
        
        if not st.session_state.loads:
            st.warning("Please add electrical loads in Load Assessment first.")
            return
        
        # Get client data
        client_data = self.client_manager.get_client(st.session_state.current_client)
        location = client_data['location_info']['city']
        system_mode = client_data['project_info']['system_mode']
        days_autonomy = client_data['project_info']['days_autonomy']
        system_efficiency = client_data['project_info']['system_efficiency']
        
        # Calculate load
        load_results = self.load_calc.calculate_load_assessment(st.session_state.loads)
        
        # Perform solar system calculations
        solar_results = self.solar_sizer.calculate_solar_requirements(
            daily_energy_wh=load_results['total_daily_energy_wh'],
            location=location,
            system_mode=system_mode,
            days_autonomy=days_autonomy,
            system_efficiency=system_efficiency
        )
        
        # Calculate battery configuration
        battery_config = self.solar_sizer.calculate_battery_configuration(
            battery_capacity_ah=solar_results['battery_capacity_ah'],
            system_voltage=solar_results['system_voltage'],
            battery_type=solar_results['battery_type']
        )
        
        # Store results
        st.session_state.calculation_results = {
            'load': load_results,
            'solar': solar_results,
            'battery': battery_config,
            'client': client_data
        }
        
        # Display results
        st.success("System design completed successfully!")
        
        # Key metrics
        st.subheader("System Specification")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Solar Array Size", f"{solar_results['required_solar_kw']:.2f} kW")
        with col2:
            st.metric("Battery Bank", f"{solar_results['battery_capacity_kwh']:.2f} kWh")
        with col3:
            st.metric("Inverter Capacity", f"{solar_results['inverter_size_kva']:.2f} kVA")
        with col4:
            st.metric("Charge Controller", f"{solar_results['charge_controller_a']:.1f} A")
        
        # Detailed specifications
        st.subheader("Detailed Design Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Location & Resources**")
            st.write(f"- Location: {location}")
            st.write(f"- Daily Sun Hours: {solar_results['sun_hours_used']} hours")
            st.write(f"- System Voltage: {solar_results['system_voltage']}V")
            st.write(f"- Battery Type: {solar_results['battery_type'].title()}")
            
            st.write("**Load Information**")
            st.write(f"- Daily Energy: {load_results['total_daily_energy_kwh']:.2f} kWh")
            st.write(f"- Peak Demand: {load_results['peak_load_w']/1000:.2f} kW")
            st.write(f"- Connected Load: {load_results['total_connected_load_w']/1000:.2f} kW")
        
        with col2:
            st.write("**Battery Configuration**")
            st.write(f"- Configuration: {battery_config['configuration']}")
            st.write(f"- Total Batteries: {battery_config['total_batteries']}")
            st.write(f"- Battery Size: {battery_config['battery_size_ah']} Ah each")
            st.write(f"- Actual Capacity: {battery_config['actual_capacity_ah']} Ah")
            
            st.write("**Design Parameters**")
            st.write(f"- Days of Autonomy: {days_autonomy}")
            st.write(f"- System Efficiency: {system_efficiency*100}%")
            st.write(f"- System Mode: {system_mode.split('(')[0]}")

    def show_product_recommendations(self):
        """Product recommendations based on system design"""
        st.markdown('<div class="section-header">Product Recommendations</div>', unsafe_allow_html=True)
        
        if not st.session_state.calculation_results:
            st.warning("Please complete System Design first.")
            return
        
        results = st.session_state.calculation_results
        solar_results = results['solar']
        
        st.info("Based on your system design, here are recommended products from our catalogue.")
        
        # Solar Panel Recommendations
        st.subheader("Recommended Solar Panels")
        panels = self.product_recommender.recommend_panels(solar_results['required_solar_w'])
        
        if panels is not None and not panels.empty:
            # Display panels in cards
            for _, panel in panels.iterrows():
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.write(f"**{panel['manufacturer']} {panel['model']}**")
                        st.write(f"{panel['description']}")
                    with col2:
                        st.write(f"**{panel['capacity']}W**")
                    with col3:
                        st.write(f"₦{panel['price_ngn']:,.0f}")
                    with col4:
                        if st.button("Select", key=f"panel_{panel['model']}"):
                            st.success(f"Selected {panel['model']}")
                    st.markdown("---")
        else:
            st.warning("No suitable solar panels found in database.")
        
        # Inverter Recommendations
        st.subheader("Recommended Inverters")
        inverters = self.product_recommender.recommend_inverters(
            solar_results['inverter_size_kva'],
            solar_results['system_voltage']
        )
        
        if inverters is not None and not inverters.empty:
            for _, inverter in inverters.iterrows():
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.write(f"**{inverter['manufacturer']} {inverter['model']}**")
                        st.write(f"{inverter['description']}")
                    with col2:
                        st.write(f"**{inverter['capacity']/1000}kVA**")
                    with col3:
                        st.write(f"₦{inverter['price_ngn']:,.0f}")
                    with col4:
                        if st.button("Select", key=f"inv_{inverter['model']}"):
                            st.success(f"Selected {inverter['model']}")
                    st.markdown("---")
        else:
            st.warning("No suitable inverters found in database.")

    def show_project_summary(self):
        """Complete project summary and export"""
        st.markdown('<div class="section-header">Project Summary</div>', unsafe_allow_html=True)
        
        if not st.session_state.calculation_results:
            st.warning("Please complete all previous sections first.")
            return
        
        results = st.session_state.calculation_results
        client_data = results['client']
        
        st.success("Your commercial solar PV system design is complete!")
        
        # Project overview
        st.subheader("Project Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Client Information**")
            st.write(f"Name: {client_data['basic_info']['name']}")
            st.write(f"Company: {client_data['basic_info']['company']}")
            st.write(f"Email: {client_data['basic_info']['email']}")
            st.write(f"Phone: {client_data['basic_info']['phone']}")
        
        with col2:
            st.write("**Project Location**")
            st.write(f"Address: {client_data['location_info']['address']}")
            st.write(f"City: {client_data['location_info']['city']}")
            st.write(f"State: {client_data['location_info']['state']}")
            st.write(f"Country: {client_data['location_info']['country']}")
        
        # System specification
        st.subheader("System Specification")
        
        # Cost estimation
        st.subheader("Cost Estimation")
        solar_kw = results['solar']['required_solar_kw']
        battery_kwh = results['solar']['battery_capacity_kwh']
        
        # Rough cost estimates (Nigerian market)
        solar_cost = solar_kw * 1200000  # ₦1.2M per kW
        battery_cost = battery_kwh * 600000  # ₦600k per kWh
        inverter_cost = results['solar']['inverter_size_kva'] * 400000  # ₦400k per kVA
        installation_cost = (solar_cost + battery_cost + inverter_cost) * 0.3  # 30% installation
        
        total_cost = solar_cost + battery_cost + inverter_cost + installation_cost
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Solar Panels", f"₦{solar_cost:,.0f}")
        with col2:
            st.metric("Battery Bank", f"₦{battery_cost:,.0f}")
        with col3:
            st.metric("Inverter System", f"₦{inverter_cost:,.0f}")
        with col4:
            st.metric("Total Project", f"₦{total_cost:,.0f}")
        
        # Export options
        st.subheader("Export Project")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Generate PDF Report", type="primary"):
                st.info("PDF report generation would be implemented here")
        
        with col2:
            if st.button("Export to Excel"):
                st.info("Excel export would be implemented here")
        
        with col3:
            if st.button("Save Project"):
                st.info("Project saving would be implemented here")
        
        # Footer
        st.markdown('<div class="footer">Developed by Moshood • Professional Solar PV Design</div>', unsafe_allow_html=True)

def main():
    app = SolarCalculatorApp()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio("Select Section", [
        "Welcome",
        "Client Information", 
        "Load Assessment", 
        "System Design",
        "Product Recommendations",
        "Project Summary"
    ])
    
    # Page routing
    if page == "Welcome":
        app.show_welcome()
    elif page == "Client Information":
        app.show_client_info()
    elif page == "Load Assessment":
        app.show_load_assessment()
    elif page == "System Design":
        app.show_system_design()
    elif page == "Product Recommendations":
        app.show_product_recommendations()
    elif page == "Project Summary":
        app.show_project_summary()

if __name__ == "__main__":
    main()