# Importing classes from collections pandas, json, datetime
from pandas import json_normalize
import json
import pandas as pd
import datetime

def convertXlsx(source_name="host_resources.json"):
    # Read JSON file and write out EXCEL file
    with open(source_name, 'r') as f:
        data = json.loads(f.read())
    
    # Create DataFrame df1 for resource path resources:permissions with hostid column preserved in table header
    df1 = pd.json_normalize(
        data,
        record_path='resources',
        meta=['hostid'],
        errors='ignore'
    )
    
    # Drop unnecessary columns from JSON response in DataFrame df1
    df1 = df1.drop(
        columns=['replication_sets', 'policy_versions', 'annotations', 'permissions', 'secrets'],
        errors='ignore'
    )
    
    # Rename columns to descriptive label of data
    df1 = df1.rename(
        columns={"id": "resourceid"}
    )
    
    # Create DataFrame df2 for resource path resources:permissions with hostid column preserved in table header
    df2 = pd.json_normalize(
        data,
        record_path=['resources', 'permissions'],
        meta=['hostid', ['resource', 'id']],
        sep='',
        errors='ignore'
    )
    
    # Drop unnecessary columns from JSON response in DataFrame df2
    df2 = df2.drop(
        columns=['replication_sets', 'policy'],
        errors='ignore'
    )
    
    # Rename columns to descriptive label of data
    df2 = df2.rename(
        columns={"hostid": "member ( hostid )", "role": "role ( groupid | hostid )"}
    )
    
    # Create pivot table of resource:permissions
    df3 = df2.drop(
        columns=['role ( groupid | hostid )']
    )
    df3 = df3.pivot_table(
        index = ["member ( hostid )", "resourceid", "privilege"],
        values = ["member ( hostid )", "resourceid", "privilege"]
    )
    
    # Current date object for output .xlsx file
    current_date = datetime.date.today()
    
    # Write DataFrames df1, df2, df3 out to Excel-based output
    with pd.ExcelWriter(str(current_date) + '_resources-by-apphost.xlsx') as writer:
        df1.to_excel(writer, sheet_name="resources by hostid", index=False)
        for column in df1:
            column_length = max(df1[column].astype(str).map(len).max(), len(column))
            col_idx = df1.columns.get_loc(column)
            writer.sheets['resources by hostid'].set_column(col_idx, col_idx, column_length)
        df2.to_excel(writer, sheet_name="permissions", index=False)
        for column in df2:
            column_length = max(df2[column].astype(str).map(len).max(), len(column))
            col_idx = df2.columns.get_loc(column)
            writer.sheets['permissions'].set_column(col_idx, col_idx, column_length)
        df3.to_excel(writer, sheet_name="permissions by hostid")

def __main__():
    if __name__ == "__main__":
        convertXlsx
