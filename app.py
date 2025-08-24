import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Expanded Places in Karnataka (with approximate distances in km)
# ----------------------------
places_data = {
    "Bangalore": {
        "Mysore": 150, "Hampi": 340, "Coorg": 270, "Chikmagalur": 245, "Hubli": 410, "Mangalore": 352,
        "Udupi": 403, "Gokarna": 485, "Belur": 220, "Halebidu": 210
    },
    "Mysore": {
        "Bangalore": 150, "Coorg": 120, "Chikmagalur": 180, "Mangalore": 255, "Udupi": 310, "Bandipur": 80,
        "Wayanad": 120
    },
    "Hampi": {
        "Bangalore": 340, "Hubli": 165, "Hospet": 13, "Bellary": 60, "Chitradurga": 145
    },
    "Coorg": {
        "Mysore": 120, "Bangalore": 270, "Chikmagalur": 150, "Mangalore": 150, "Wayanad": 110
    },
    "Chikmagalur": {
        "Mysore": 180, "Coorg": 150, "Hubli": 250, "Bangalore": 245, "Belur": 25, "Halebidu": 35
    },
    "Hubli": {
        "Hampi": 165, "Chikmagalur": 250, "Bangalore": 410, "Dharwad": 20, "Belgaum": 100, "Gokarna": 150
    },
    "Mangalore": {
        "Bangalore": 352, "Mysore": 255, "Coorg": 150, "Udupi": 55, "Chikmagalur": 150, "Gokarna": 230
    },
    "Udupi": {
        "Mangalore": 55, "Bangalore": 403, "Gokarna": 180, "Murudeshwar": 100
    },
    "Gokarna": {
        "Bangalore": 485, "Mangalore": 230, "Udupi": 180, "Hubli": 150, "Murudeshwar": 60, "Karwar": 60
    },
    "Belur": {
        "Bangalore": 220, "Chikmagalur": 25, "Halebidu": 15
    },
    "Halebidu": {
        "Bangalore": 210, "Chikmagalur": 35, "Belur": 15
    },
    "Bandipur": {
        "Mysore": 80, "Wayanad": 60
    },
    "Wayanad": {
        "Mysore": 120, "Coorg": 110, "Bandipur": 60
    },
    "Dharwad": {
        "Hubli": 20, "Belgaum": 75
    },
    "Belgaum": {
        "Hubli": 100, "Dharwad": 75, "Goa": 125
    },
    "Murudeshwar": {
        "Udupi": 100, "Gokarna": 60, "Karwar": 120
    },
    "Karwar": {
        "Gokarna": 60, "Murudeshwar": 120, "Goa": 75
    },
    "Hospet": {
        "Hampi": 13, "Bellary": 60
    },
    "Bellary": {
        "Hospet": 60, "Hampi": 60
    },
    "Chitradurga": {
        "Hampi": 145, "Bangalore": 200
    }
}

# ----------------------------
# Carbon emission factors (kg CO2 per km per vehicle type)
# ----------------------------
emission_factors = {
    "Car (Petrol)": 0.192,
    "Car (Diesel)": 0.171,
    "Bus": 0.089,
    "Train": 0.041,
    "Bike": 0.103
}

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Eco Travel Karnataka", page_icon="🌍", layout="wide")
st.title("🌍 Eco Travel Karnataka")
st.write("Plan your journey, calculate carbon emissions, and find eco-friendly travel options within Karnataka.")

# User Inputs
col1, col2 = st.columns(2)
with col1:
    start = st.selectbox("Select Start Location", list(places_data.keys()))
with col2:
    end = st.selectbox("Select Destination", list(places_data.keys()))

vehicle = st.selectbox("Select Mode of Transport", list(emission_factors.keys()))
fuel_type = st.radio("Fuel Type", ["Petrol", "Diesel"]) if "Car" in vehicle else None
people = st.number_input("Number of Travellers", min_value=1, value=1)

# Distance calculation
distance = places_data.get(start, {}).get(end, None)
if distance is None and start != end:
    st.error("⚠️ Route not available in dataset. Try another combination.")
elif start == end:
    st.info("📍 Start and destination are the same.")
else:
    st.success(f"🛣️ Distance between **{start}** and **{end}**: {distance} km")

    # Carbon emissions
    factor = emission_factors[vehicle]
    total_emission = distance * factor
    per_person_emission = total_emission / people

    st.metric("Total Carbon Emission (kg CO₂)", f"{total_emission:.2f}")
    st.metric("Per Person Emission (kg CO₂)", f"{per_person_emission:.2f}")

    # Suggestions
    if per_person_emission > 50:
        st.warning("⚠️ High carbon footprint! Consider using a bus or train.")
    else:
        st.success("✅ Eco-friendly choice!")

    # Visualization
    fig, ax = plt.subplots()
    ax.bar(["Total Emission", "Per Person"], [total_emission, per_person_emission], color=["green", "blue"])
    ax.set_ylabel("kg CO₂")
    ax.set_title("Carbon Emission Analysis")
    st.pyplot(fig)

    # Nearby suggestions
    st.subheader("📍 Suggested Nearby Places")
    if end in places_data:
        suggestions = places_data[end]
        nearby_df = pd.DataFrame(list(suggestions.items()), columns=["Place", "Distance (km)"]).sort_values("Distance (km)")
        st.table(nearby_df.head(5))

