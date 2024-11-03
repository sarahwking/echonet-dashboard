import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('EchoNet_Dynamic_Dashboard_Data.csv')

# Set title and description
st.title("EchoNet-Dynamic Dashboard")
st.markdown("This dashboard provides insights into patient-specific LVEF trends, demographics, and health metrics.")

# Sidebar for filtering options
st.sidebar.header("Filters")
selected_patient = st.sidebar.selectbox("Select Patient ID", data['Patient_ID'].unique())
selected_gender = st.sidebar.selectbox("Select Gender", ['All'] + list(data['Gender'].unique()))
selected_risk_level = st.sidebar.multiselect("Select Risk Level", options=['Normal', 'Borderline', 'High'])

# Apply filters based on sidebar selections
filtered_data = data[data['Patient_ID'] == selected_patient]

if selected_gender != 'All':
    filtered_data = filtered_data[filtered_data['Gender'] == selected_gender]
if selected_risk_level:
    filtered_data = filtered_data[filtered_data['Risk_Level'].isin(selected_risk_level)]

# Display filtered data
st.write("Filtered Patient Data", filtered_data)

# 1. LVEF Trend Over Time (Line Chart)
st.subheader("LVEF Trend Over Time")
fig, ax = plt.subplots()
ax.plot(filtered_data['Measurement_Date'], filtered_data['LVEF_Automated'], label="Automated LVEF", marker='o')
ax.plot(filtered_data['Measurement_Date'], filtered_data['LVEF_Manual'], label="Manual LVEF", marker='x')
ax.set_xlabel("Measurement Date")
ax.set_ylabel("LVEF (%)")
ax.legend()
st.pyplot(fig)

# 2. Gender Breakdown (Pie Chart)
st.subheader("Gender Breakdown")
gender_counts = data['Gender'].value_counts()
fig, ax = plt.subplots()
ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
st.pyplot(fig)

# 3. Risk Level Distribution (Bar Chart)
st.subheader("Risk Level Distribution")
risk_counts = data['Risk_Level'].value_counts()
st.bar_chart(risk_counts)

# 4. Health Metrics (Heart Rate, Oxygen Level, Temperature)
st.subheader("Health Metrics Overview")
st.line_chart(filtered_data[['Heart_Rate', 'Oxygen_Level', 'Temperature']])

# 5. Add Insights and Descriptions
st.markdown("""
### Insights
- **LVEF Trends**: View individual trends for automated vs. manual LVEF measurements over time.
- **Demographics**: The Gender Breakdown and Risk Level Distribution charts provide a demographic overview.
- **Health Metrics**: Continuous tracking of heart rate, oxygen level, and temperature for selected patients.
""")
