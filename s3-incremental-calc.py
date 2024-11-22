import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")
import pandas as pd

# Define pricing for S3 tiers by region
PRICING = {
    "us-east-1": {
        1: ("Standard", 0.023),
        2: ("Intelligent-Tiering (Frequent Access)", 0.024),
        3: ("Intelligent-Tiering (Infrequent Access)", 0.0125),
        4: ("Glacier Instant Retrieval", 0.004),
        5: ("Glacier Flexible Retrieval", 0.0036),
        6: ("Glacier Deep Archive", 0.00099),
    },
    "us-east-2": {
        1: ("Standard", 0.023),
        2: ("Intelligent-Tiering (Frequent Access)", 0.024),
        3: ("Intelligent-Tiering (Infrequent Access)", 0.0125),
        4: ("Glacier Instant Retrieval", 0.004),
        5: ("Glacier Flexible Retrieval", 0.0036),
        6: ("Glacier Deep Archive", 0.00099),
    },
    "us-west-1": {
        1: ("Standard", 0.025),
        2: ("Intelligent-Tiering (Frequent Access)", 0.026),
        3: ("Intelligent-Tiering (Infrequent Access)", 0.015),
        4: ("Glacier Instant Retrieval", 0.005),
        5: ("Glacier Flexible Retrieval", 0.004),
        6: ("Glacier Deep Archive", 0.002),
    },
    "us-west-2": {
        1: ("Standard", 0.023),
        2: ("Intelligent-Tiering (Frequent Access)", 0.024),
        3: ("Intelligent-Tiering (Infrequent Access)", 0.0125),
        4: ("Glacier Instant Retrieval", 0.004),
        5: ("Glacier Flexible Retrieval", 0.0036),
        6: ("Glacier Deep Archive", 0.00099),
    },
}

def calculate_s3_costs(storage_tier_name, monthly_rate, initial_storage, monthly_increment, months=12):
    """Calculate the monthly costs and total cost for S3 storage."""
    storage_data = []
    total_cost = 0
    current_storage = initial_storage

    for month in range(1, months + 1):
        monthly_cost = current_storage * monthly_rate
        total_cost += monthly_cost
        storage_data.append({
            "Month": month,
            "Storage (GB)": round(current_storage, 2),
            "Cost ($)": round(monthly_cost, 2),
        })
        current_storage += monthly_increment  # Increment storage for next month
    
    return pd.DataFrame(storage_data), total_cost

def get_user_choice(prompt, choices):
    """Helper function to get a valid user choice from a list of options."""
    while True:
        print(prompt)
        for key, value in choices.items():
            print(f"{key}: {value}")
        try:
            choice = int(input("Enter your choice: "))
            if choice in choices:
                return choice
        except ValueError:
            pass
        print("Invalid choice. Please try again.")

# Region selection
region_choices = {i + 1: region for i, region in enumerate(PRICING.keys())}
selected_region_index = get_user_choice("Select a region:", region_choices)
selected_region = region_choices[selected_region_index]

# Tier selection
tier_choices = {key: name for key, (name, _) in PRICING[selected_region].items()}
selected_tier_index = get_user_choice("\nSelect a storage tier:", tier_choices)
selected_tier_name, monthly_rate = PRICING[selected_region][selected_tier_index]

# Unit selection
unit_choices = {1: "GB", 2: "TB"}
selected_unit_index = get_user_choice("\nSelect the storage unit:", unit_choices)
unit_multiplier = 1 if selected_unit_index == 1 else 1024

# Get user inputs for storage
initial_storage = float(input("\nEnter the initial storage size: ")) * unit_multiplier
monthly_increment = float(input("Enter the amount of data added each month: ")) * unit_multiplier
months = int(input("Enter the number of months to project costs (e.g., 12): "))

# Calculate costs
cost_table, total_cost = calculate_s3_costs(
    selected_tier_name, monthly_rate, initial_storage, monthly_increment, months
)

# Display results
print("\nAmazon S3 Cost Projection:")
print(cost_table)

# Summary
print("\nSummary:")
print(f"Region: {selected_region}")
print(f"Storage Tier: {selected_tier_name}")
print(f"Total Storage Added: {round((initial_storage + monthly_increment * (months - 1)) / unit_multiplier, 2)} {unit_choices[selected_unit_index]}")
print(f"Total Cost: ${total_cost:.2f}")

# Optionally save to CSV
save_to_csv = input("\nWould you like to save the results to a CSV file? (yes/no): ").strip().lower()
if save_to_csv == "yes":
    file_name = input("Enter the filename (e.g., s3_cost_projection.csv): ").strip()
    cost_table.to_csv(file_name, index=False)
    print(f"Results saved to {file_name}")
