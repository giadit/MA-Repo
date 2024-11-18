# Function to extract investment for a given component
def extract_investment(results, component_label):
    """
    Extract the investment amount for a specific component.
    """
    # Search for the specific component in the results
    for key in results.keys():
        if component_label in str(key):
            try:
                investment = results[key]["scalars"]["invest"]
                print(f"Investment for {component_label}: {investment}")
                return investment
            except KeyError:
                print(f"No investment data found for {component_label}.")
                return None
    print(f"{component_label} not found in results.")
    return None
