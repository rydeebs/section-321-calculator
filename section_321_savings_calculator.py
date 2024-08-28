import streamlit as st
import plotly.graph_objects as go

def calculate_savings(units_per_po, num_pos_per_year, avg_cost_per_unit, freight_cost, hts_code_percentage):
    total_cost = (units_per_po * num_pos_per_year * avg_cost_per_unit) + freight_cost
    savings = total_cost * (hts_code_percentage / 100)
    return savings, total_cost

st.title("Section 321 Savings Calculator")

st.write("""
This calculator estimates the potential savings when using the Section 321 program 
based on your purchase orders, costs, and HTS code percentage.
""")

units_per_po = st.number_input("Average Number of Units in Purchase Order (PO)", min_value=1, value=1000)
num_pos_per_year = st.number_input("Number of Purchase Orders (POs) a Year", min_value=1, value=12)
avg_cost_per_unit = st.number_input("Average Cost of Goods per Unit ($)", min_value=0.01, value=50.00, step=0.01)
freight_cost = st.number_input("Freight Costs ($)", min_value=0.0, value=5000.00, step=0.01)
hts_code_percentage = st.number_input("HTS Code %", min_value=0.0, max_value=100.0, value=5.0, step=0.1)

if st.button("Calculate Savings"):
    savings, total_cost = calculate_savings(units_per_po, num_pos_per_year, avg_cost_per_unit, freight_cost, hts_code_percentage)

    st.subheader("Estimated Savings:")
    st.write(f"Total Cost of Goods and Freight: ${total_cost:,.2f}")
    st.write(f"Potential Savings with Section 321: ${savings:,.2f}")

    # Calculate percentage savings
    percentage_savings = (savings / total_cost) * 100
    st.write(f"Percentage Savings: {percentage_savings:.2f}%")

    # Visualize savings
    fig = go.Figure(data=[
        go.Bar(name='Total Cost', x=['Without Section 321', 'With Section 321'], 
               y=[total_cost, total_cost - savings]),
        go.Bar(name='Savings', x=['Without Section 321', 'With Section 321'], 
               y=[0, savings])
    ])
    fig.update_layout(barmode='stack', title='Cost Comparison: With and Without Section 321')
    st.plotly_chart(fig)

    # Additional insights
    st.subheader("Additional Insights:")
    st.write(f"Average Saving per PO: ${savings / num_pos_per_year:.2f}")
    st.write(f"Average Saving per Unit: ${savings / (units_per_po * num_pos_per_year):.2f}")

    # Breakeven analysis
    if savings > 0:
        breakeven_pos = freight_cost / (units_per_po * avg_cost_per_unit * (hts_code_percentage / 100))
        st.write(f"Breakeven Point: {breakeven_pos:.2f} Purchase Orders")
        if breakeven_pos < num_pos_per_year:
            st.write("You're above the breakeven point, Section 321 is beneficial.")
        else:
            st.write("You're below the breakeven point, but Section 321 can still provide savings.")
    else:
        st.write("No savings calculated. Please check your input values.")
