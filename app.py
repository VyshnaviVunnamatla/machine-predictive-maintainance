import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the trained model
rfc = joblib.load('model.joblib')

# App Title
st.title("🔧 Machine Predictive Maintenance System")
st.write("### Predict machine failure based on sensor data!")

# Sidebar Information
st.sidebar.header("ℹ️ About This App")
st.sidebar.write("""
This app predicts whether a machine will fail based on input parameters.
- 📊 **Real-time Analysis**
- 🛠 **Failure Prevention Measures**
- 🔍 **Actionable Insights**
""")

# User Input
st.write("### 🔢 Enter Machine Parameters")

col1, col2 = st.columns(2)

with col1:
    selected_type = st.selectbox('Select a Type', ['Low', 'Medium', 'High'])
    type_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
    selected_type = type_mapping[selected_type]

with col2:
    air_temperature = st.number_input('🌡️ Air Temperature [K]', min_value=250, max_value=400, value=300)

with col1:
    process_temperature = st.number_input('🔥 Process Temperature [K]', min_value=250, max_value=400, value=350)

with col2:
    rotational_speed = st.number_input('🔄 Rotational Speed [rpm]', min_value=500, max_value=5000, value=1500)

with col1:
    torque = st.number_input('⚙️ Torque [Nm]', min_value=0, max_value=100, value=50)

with col2:
    tool_wear = st.number_input('🔧 Tool Wear [min]', min_value=0, max_value=200, value=120)

# Prediction Logic
failure_pred = ""
prediction_probabilities = ""

if st.button('🔍 Predict Failure'):
    input_data = np.array([[selected_type, air_temperature, 
                             process_temperature, rotational_speed,
                             torque, tool_wear]])

    # Make prediction and get probabilities
    failure_pred = rfc.predict(input_data)
    prediction_probabilities = rfc.predict_proba(input_data)  # Get probability for each class

    # Display result based on prediction
    if failure_pred[0] == 1:
        st.error("⚠️ Machine will suffer Failure")

        # Reasons for failure
        st.subheader("❗ Possible Reasons for Failure:")
        failure_reasons = []

        if process_temperature > 350:
            failure_reasons.append("🔥 **High Process Temperature**: Risk of overheating.")
        if torque > 60:
            failure_reasons.append("⚙️ **High Torque**: Excessive load on machine components.")
        if rotational_speed > 2000:
            failure_reasons.append("🔄 **High Rotational Speed**: Increased wear and tear.")
        if tool_wear > 150:
            failure_reasons.append("🔧 **Tool Wear**: Worn-out tools may cause failure.")
        if air_temperature > 310:
            failure_reasons.append("🌡️ **High Air Temperature**: Inefficient cooling.")

        for reason in failure_reasons:
            st.write(f"- {reason}")

        # Precautions to prevent failure
        st.subheader("✅ Precautionary Measures:")
        st.write("""- 🛠 **Regularly inspect and maintain machine components.**  
                    - ⚙️ **Reduce excessive torque and ensure proper lubrication.**  
                    - 🌡️ **Monitor and control process temperature to avoid overheating.**  
                    - 🔧 **Replace worn-out tools before they cause damage.**  
                    - ❄️ **Maintain an optimal air temperature for efficient operation.**""")

    else:
        st.success("✅ Machine Will Not suffer Failure")

    # Show Prediction Probability
    st.write("### Prediction Confidence:")
    st.write(f"Probability of No Failure: {prediction_probabilities[0][0]}")
    st.write(f"Probability of Failure: {prediction_probabilities[0][1]}")

    # Save result in a dataframe
    result_data = {
        "Machine Type": selected_type,
        "Air Temp (K)": air_temperature,
        "Process Temp (K)": process_temperature,
        "Rotational Speed (rpm)": rotational_speed,
        "Torque (Nm)": torque,
        "Tool Wear (min)": tool_wear,
        "Failure Prediction": "Failure" if failure_pred[0] == 1 else "No Failure"
    }
    df = pd.DataFrame([result_data])

    # Show result table
    st.write("📋 **Prediction Data:**")
    st.dataframe(df)

    # Visualization - Bar Chart of Inputs
    st.write("📊 **Parameter Overview**")
    fig, ax = plt.subplots()
    params = ["Air Temp", "Process Temp", "Rotational Speed", "Torque", "Tool Wear"]
    values = [air_temperature, process_temperature, rotational_speed, torque, tool_wear]
    ax.barh(params, values, color=["blue", "red", "green", "orange", "purple"])
    ax.set_xlabel("Value")
    ax.set_title("Input Parameters")
    st.pyplot(fig)

# Footer
st.write("🛠 **Developed for Machine Health Monitoring**")
