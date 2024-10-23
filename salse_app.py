import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('F:\\Ali Akber Ml models\\Datasets\\Streamlit\\data.csv', encoding='ISO-8859-1')
    data.dropna(subset=['CustomerID'], inplace=True)  # Remove null customers
    data['TotalPrice'] = data['Quantity'] * data['UnitPrice']  # Calculate total price
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    return data

df = load_data()
st.title('Sales Dashboard for E-commerce')
# Sidebar filters
st.sidebar.header('Filters')
start_date = st.sidebar.date_input('Start Date', df['InvoiceDate'].min())
end_date = st.sidebar.date_input('End Date', df['InvoiceDate'].max())
country = st.sidebar.multiselect('Select Country', df['Country'].unique())

# Filter data based on input
filtered_df = df[(df['InvoiceDate'] >= pd.Timestamp(start_date)) &
                 (df['InvoiceDate'] <= pd.Timestamp(end_date))]

if country:
    filtered_df = filtered_df[filtered_df['Country'].isin(country)]

st.dataframe(filtered_df.head())  # Display a preview of the filtered data
# Calculate KPIs
total_sales = filtered_df['TotalPrice'].sum()
avg_order_value = filtered_df['TotalPrice'].mean()
num_orders = filtered_df['InvoiceNo'].nunique()

# Display KPIs
st.subheader('Key Performance Indicators')
col1, col2, col3 = st.columns(3)
col1.metric('Total Sales', f'${total_sales:,.2f}')
col2.metric('Avg Order Value', f'${avg_order_value:,.2f}')
col3.metric('Total Orders', num_orders)
import plotly.express as px

# Sales Trend over Time
sales_trend = filtered_df.groupby(filtered_df['InvoiceDate'].dt.date)['TotalPrice'].sum().reset_index()
fig1 = px.line(sales_trend, x='InvoiceDate', y='TotalPrice', title='Sales Trend Over Time')
st.plotly_chart(fig1)

# Sales by Country
sales_by_country = filtered_df.groupby('Country')['TotalPrice'].sum().reset_index()
fig2 = px.bar(sales_by_country, x='Country', y='TotalPrice', title='Sales by Country')
st.plotly_chart(fig2)
# Export filtered data
st.download_button(
    label='Download Filtered Data as CSV',
    data=filtered_df.to_csv(index=False),
    file_name='filtered_sales_data.csv',
    mime='text/csv'
)
# redirect URLs
github_redirect_url = "https://github.com/AliAkber12/Ali-Akber"
kaggle_redirect_url = "https://www.kaggle.com/"
linkedin_redirect_url = "https://www.linkedin.com/in/ali-akber-chandio-480344329/"

# Footer with social media icons
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f5f5f5;
        color: #000000;
        text-align: center;
        padding: 10px;
    }
    .footer img {
        margin: 0 10px;
        vertical-align: middle;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="footer">
        Made with ❤️ by Ali Akber
        <a href="{github_redirect_url}" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="30" height="30" alt="GitHub">
        </a>
        <a href="{kaggle_redirect_url}" target="_blank">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/kaggle/kaggle-original-wordmark.svg" width="30" height="30" alt="Kaggle">
        </a>
        <a href="{linkedin_redirect_url}" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30" height="30" alt="LinkedIn">
        </a>
    </div>
    """, 
    unsafe_allow_html=True
)

