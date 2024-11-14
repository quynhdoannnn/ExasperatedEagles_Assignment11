# Name: [Your Name]
# Email: [Your Email]
# Assignment Number: Assignment 11
# Due Date: 11/21/2024
# Course #/Section: IS 4010-001
# Semester/Year: Fall Semester 2024
# Brief Description of the assignment: Clean and analyze fuel purchase data.
# Brief Description of what this module does: Provides methods to load, clean, and save processed data.
# Citations: Pandas library documentation, Zipcodebase API documentation.
# Anything else that's relevant: The API key is required for the `fill_missing_zip_codes` method.

# dataCleaner.py
import pandas as pd
import requests

class DataCleaner:
    def __init__(self, file_path):
        self.file_path = file_path  # Path to the input CSV file
        self.data = None
        # Define output file paths within the Data folder
        self.anomalies_file = 'Data/dataAnomalies.csv'
        self.cleaned_file = 'Data/cleanedData.csv'
        self.api_key = 'ce77b5b0-a28c-11ef-8490-17b0a6a93aa1'  # Provided API key

    def load_data(self):
        """Load data from CSV file."""
        self.data = pd.read_csv(self.file_path, low_memory=False)
        print("Data loaded successfully.")
        print("Column names:", self.data.columns)  # Print column names for debugging

    def clean_gross_price(self):
        """Ensure Gross Price is rounded to 2 decimal places."""
        self.data['Gross Price'] = pd.to_numeric(self.data['Gross Price'], errors='coerce').round(2)
        print("Gross Price rounded to 2 decimal places.")

    def remove_duplicates(self):
        """Remove duplicate rows."""
        initial_row_count = len(self.data)
        self.data = self.data.drop_duplicates()
        final_row_count = len(self.data)
        print(f"Removed {initial_row_count - final_row_count} duplicate rows.")

    def handle_anomalies(self):
        """Separate rows where Fuel Type is 'Pepsi' instead of fuel."""
        pepsi_data = self.data[self.data['Fuel Type'] == 'Pepsi']
        fuel_data = self.data[self.data['Fuel Type'] != 'Pepsi']

        # Save anomalies to a new CSV and update main data
        pepsi_data.to_csv(self.anomalies_file, index=False)
        self.data = fuel_data
        print("Pepsi purchases separated and saved as data anomalies.")

    def fill_missing_zip_codes(self):
        """Fill in missing zip codes using the Zipcodebase API."""
        missing_zip_data = self.data[self.data['Full Address'].isnull()]

        for index, row in missing_zip_data.iterrows():
            city = row['Full Address'].split(',')[0]
            # Make API call to get zip code for the city
            response = requests.get(
                f'https://app.zipcodebase.com/api/v1/search?apikey={self.api_key}&city={city}&country=US'
            )
            if response.status_code == 200:
                zip_codes = response.json().get('results', {}).get(city, [])
                if zip_codes:
                    # Assign the first zip code as a fallback option
                    self.data.at[index, 'Full Address'] = f"{row['Full Address']}, {zip_codes[0]}"
                    print(f"Zip code {zip_codes[0]} added for city {city}")
            else:
                print(f"Failed to retrieve zip code for city {city}.")

    def save_clean_data(self):
        """Save the cleaned data to a new CSV file."""
        self.data.to_csv(self.cleaned_file, index=False)
        print(f"Cleaned data saved to {self.cleaned_file}.")


