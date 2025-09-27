# client_database.py
import pandas as pd
import streamlit as st
from datetime import datetime
import json

class ClientManager:
    def __init__(self):
        self.clients_file = "clients.json"
        self.load_clients()
    
    def load_clients(self):
        """Load client data from JSON file"""
        try:
            with open(self.clients_file, 'r') as f:
                self.clients = json.load(f)
        except FileNotFoundError:
            self.clients = {}
    
    def save_clients(self):
        """Save client data to JSON file"""
        with open(self.clients_file, 'w') as f:
            json.dump(self.clients, f, indent=4)
    
    def add_client(self, client_data):
        """Add a new client to the database"""
        client_id = f"client_{len(self.clients) + 1:04d}"
        client_data['client_id'] = client_id
        client_data['created_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.clients[client_id] = client_data
        self.save_clients()
        return client_id
    
    def get_client(self, client_id):
        """Get client data by ID"""
        return self.clients.get(client_id)
    
    def get_all_clients(self):
        """Get all clients"""
        return self.clients

# Sample client data structure
SAMPLE_CLIENT = {
    "basic_info": {
        "name": "",
        "company": "",
        "email": "",
        "phone": ""
    },
    "location_info": {
        "address": "",
        "city": "",
        "state": "",
        "country": "Nigeria",
        "coordinates": ""
    },
    "project_info": {
        "project_type": "",
        "system_mode": "Basic Setup",
        "days_autonomy": 2,
        "system_efficiency": 80
    }
}

# Nigerian states list for dropdown
NIGERIAN_STATES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno",
    "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo", "Jigawa",
    "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger",
    "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara"
]

# System modes configuration
SYSTEM_MODES = {
    "Basic Setup (Residential/Small Office)": {
        "range": "0-1.5 kVA",
        "voltage": 12,
        "battery_type": "lead-acid",
        "min_power": 0,
        "max_power": 1500
    },
    "Standard Setup (Retail/Medium Business)": {
        "range": "1.5-3.5 kVA", 
        "voltage": 24,
        "battery_type": "lead-acid",
        "min_power": 1500,
        "max_power": 3500
    },
    "Advanced Setup (Commercial/Industrial)": {
        "range": "3.5 kVA and above",
        "voltage": 48,
        "battery_type": "lithium",
        "min_power": 3500,
        "max_power": 50000
    }
}