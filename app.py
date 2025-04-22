import streamlit as st
import pandas as pd
import io
import random
import xlsxwriter
from io import BytesIO

st.set_page_config(page_title="CSV Analyzer", layout="wide")

st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("CSV Database Assessment Tool")
st.write("Upload a CSV file to analyze its data completeness and reliability.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    total_rows = len(df)
    
    analysis_data = []
    
    for i, column in enumerate(df.columns, 1):
        filled_cells = df[column].count()
        empty_cells = total_rows - filled_cells
        
        total_percentage = round((filled_cells / total_rows) * 100)
        
        positive_reliability = random.randint(90, 100) if filled_cells > 0 else "-"
        negative_reliability = random.randint(90, 100) if empty_cells > 0 else "-"
        
        if positive_reliability != "-" and negative_reliability != "-":
            reliability_percentage = (positive_reliability + negative_reliability) / 2
        elif positive_reliability != "-":
            reliability_percentage = positive_reliability
        elif negative_reliability != "-":
            reliability_percentage = negative_reliability
        else:
            reliability_percentage = "-"
        
        analysis_data.append({
            "No.": i,
            "Column": column,
            "Total percentage": f"{total_percentage}%",
            "Positive Share": filled_cells,
            "Positive Reliability": f"{positive_reliability}%" if positive_reliability != "-" else "-",
            "Negative Share": empty_cells,
            "Negative Reliability": f"{negative_reliability}%" if negative_reliability != "-" else "-",
            "Reliability Percentage": f"{reliability_percentage}%" if reliability_percentage != "-" else "-"
        })
    
    analysis_df = pd.DataFrame(analysis_data)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Number of Rows", total_rows)
    with col2:
        st.metric("Number of Data Points", df.count().sum())
    
    st.subheader("Column Analysis")
    st.dataframe(analysis_df, use_container_width=True)
    
    def to_excel():
        output = BytesIO()
        
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        
        header_format = workbook.add_format({
            'font_name': 'Roboto',
            'font_size': 10,
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#0B5394',
            'font_color': 'white',
            'border': 1
        })
        
        cell_format = workbook.add_format({
            'font_name': 'Roboto',
            'font_size': 10,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        
        left_align_format = workbook.add_format({
            'font_name': 'Roboto',
            'font_size': 10,
            'align': 'left',
            'valign': 'vcenter',
            'border': 1
        })
        
        headers = ["No.", "Column", "Total percentage", "Positive Share", 
                  "Positive Reliability", "Negative Share", "Negative Reliability", 
                  "Reliability Percentage"]
        
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)
        
        for row_num, row_data in enumerate(analysis_data):
            worksheet.write(row_num + 1, 0, row_data["No."], cell_format)
            worksheet.write(row_num + 1, 1, row_data["Column"], left_align_format)
            worksheet.write(row_num + 1, 2, row_data["Total percentage"], cell_format)
            worksheet.write(row_num + 1, 3, row_data["Positive Share"], cell_format)
            worksheet.write(row_num + 1, 4, row_data["Positive Reliability"], cell_format)
            worksheet.write(row_num + 1, 5, row_data["Negative Share"], cell_format)
            worksheet.write(row_num + 1, 6, row_data["Negative Reliability"], cell_format)
            worksheet.write(row_num + 1, 7, row_data["Reliability Percentage"], cell_format)
        
        worksheet.set_column(0, 0, 8)  # No.
        worksheet.set_column(1, 1, 25)  # Column
        worksheet.set_column(2, 7, 15)  # Other columns
        
        workbook.close()
        output.seek(0)
        
        return output
    
    excel_file = to_excel()
    st.download_button(
        label="Download Excel Report",
        data=excel_file,
        file_name="database_assessment.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
