# Basic imports
import pandas as pd
import os
import pycountry
import glob
from sqlalchemy import create_engine
import config 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
sns.set_theme()

# Combining and Sort CSV Files into a Single DataFrame
def process_files(path: str, filename_convention: str, year_range: tuple):
    """
    Reads CSV files based on the provided path, filename convention, and year range,
    concatenates them into a single DataFrame and sorts the DataFrame.
    
    Args:
    - path (str): Directory path where the files are located.
    - filename_convention (str): Filename pattern, e.g., "ImportsExports_Coffee".
    - year_range (tuple): Range of years to process, e.g., (2018, 2024).

    Returns:
    - final_df (pd.DataFrame): The concatenated, cleaned, and sorted DataFrame.
    """

    all_sorted_dfs = []

    # Loop through years in the specified range
    for year in range(year_range[0], year_range[1] + 1):
        # Construct the search pattern with wildcard for country codes
        search_pattern = os.path.join(path, f"{filename_convention}_*_WORLD_{year}.csv")

        # Use glob to find all files matching the pattern
        files = glob.glob(search_pattern)

        if not files:
            print(f"No files found for the pattern: {search_pattern}")
            continue  # Skip if no files are found

        # Read each file found by glob
        for file_path in files:
            # Read the CSV file
            df = pd.read_csv(file_path, encoding='ISO-8859-1')

            # Append the raw DataFrame to the list for now (will clean and sort later)
            all_sorted_dfs.append(df)

    # If no files were processed, return an empty DataFrame
    if not all_sorted_dfs:
        print("No files were processed.")
        return pd.DataFrame()

    # Concatenate all DataFrames into one
    final_df = pd.concat(all_sorted_dfs).reset_index(drop=True)

    # Sort the DataFrame by period and country
    final_df = final_df.sort_values(by=['Period', 'ReporterDesc', 'PartnerDesc']).reset_index(drop=True)
    
    return final_df

# Dataframe Cleaning
def clean_and_prepare_dataframe(df: pd.DataFrame):
    """
    This function performs the cleaning of a dataframe:
    - Rename specific columns to improve readability.
    - Define and Drop unnecessary columns, based on the data profiling.
    - Correct Country Names
    - Filter out rows with invalid country codes
    
    If any step has already been performed or the necessary columns do not exist, it will be skipped.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    
    Returns:
    pd.DataFrame: A cleaned and prepared DataFrame.
    """
    
    # Rename specific columns to improve readability.
    coffee_columns_rename_dict  = {
        'Qty': 'Qty_in_kg',
        'RefYear': 'Year',
        'RefMonth': 'Month'
    }
    existing_columns_to_rename = {k: v for k, v in coffee_columns_rename_dict.items() if k in df.columns}
    if existing_columns_to_rename:
        df.rename(columns=existing_columns_to_rename, inplace=True)
    else:
        print("Specified columns to rename are either already renamed or do not exist.")
    
    # Define columns to drop based on data profiling
    coffee_constant_columns = ['TypeCode', 'FreqCode', 'ReporterCode', 'Partner2Code', 'Partner2ISO', 'Partner2Desc', 'ClassificationCode', 'ClassificationSearchCode', 'IsOriginalClassification', 'AggrLevel', 'IsLeaf', 'CustomsCode', 'CustomsDesc', 'MosCode', 'MotCode', 'MotDesc', 'QtyUnitCode', 'QtyUnitAbbr', 'IsQtyEstimated', 'AltQtyUnitCode', 'AltQtyUnitAbbr', 'IsAltQtyEstimated', 'IsNetWgtEstimated', 'GrossWgt', 'IsGrossWgtEstimated', 'LegacyEstimationFlag', 'IsReported', 'IsAggregate']
    coffee_high_correlated_columns = ['Fobvalue', 'RefPeriodId', 'PartnerCode', 'AltQty', 'NetWgt']
    coffee_missing_values_columns = ['Cifvalue', 'Unnamed: 47']
    coffee_columns_to_drop = coffee_constant_columns + coffee_high_correlated_columns + coffee_missing_values_columns 

    # Drop the specified columns if they exist in the DataFrame
    existing_columns_to_drop = [col for col in coffee_columns_to_drop if col in df.columns]
    if existing_columns_to_drop:
        df = df.drop(columns=existing_columns_to_drop, axis=1)
    else:
        print("Specified columns to drop are either already removed or do not exist.")
    
    # Correct Country Names
    # - Iterate through each row to checks if the country code is valid, when it isn't remove entries with invalid PartnerISO codes.
    # - Replace the country name with the standardized one.
    valid_country_codes = {country.alpha_3: country.name for country in pycountry.countries}

    for index, row in df.iterrows():
        code = row['PartnerISO']
        if code in valid_country_codes:
            df.at[index, 'PartnerDesc'] = valid_country_codes[code]

    # Filter out rows with invalid country codes
    df_cleaned = df[df['PartnerISO'].isin(valid_country_codes.keys())]
    
    # The cleaned and prepared DataFrame with renamed columns, unnecessary columns removed, 
    # invalid country codes filtered out, and correct country names applied.
    return df_cleaned

# Creating an engine to connect to MySQL 
def create_sqlalchemy_engine(user: str, password: str, host: str, database: str, port=3306):
    """
    Create a SQLAlchemy engine for connecting to a MySQL database.

    :param user: MySQL username.
    :param password: MySQL password.
    :param host: MySQL server host (e.g., 'localhost').
    :param database: Database name to connect to.
    :param port: MySQL port, default is 3306.
    :return: SQLAlchemy engine.
    """
    connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)
    return engine

# Include dataframe into MySQL
def insert_dataframe_to_mysql(df: pd.DataFrame, table_name: str, engine: str, if_exists='replace'):
    """
    Insert a pandas DataFrame into a MySQL table using SQLAlchemy.

    :param df: pandas DataFrame to be inserted.
    :param table_name: Name of the target table in the MySQL database.
    :param engine: SQLAlchemy engine connected to the target database.
    :param if_exists: How to behave if the table already exists ('fail', 'replace', 'append').
    :return: None
    """
    df.to_sql(name=table_name, con=engine, if_exists=if_exists, index=False)

## EDA FUNCTIONS

# Data Preprocessing for Trade Report Enhancement
def process_trade_data(df: pd.DataFrame):
    """
    Process the trade data by renaming columns and mapping CmdCode to short descriptions.

    Parameters:
    df (pd.DataFrame): The DataFrame containing trade data.

    Returns:
    pd.DataFrame: The processed DataFrame with renamed columns and short descriptions.
    """
    # Rename columns for clarity
    df = df.rename(columns={
        'ReporterISO': 'Origin_CountryISO',
        'ReporterDesc': 'Origin_CountryName',
        'PartnerDesc': 'Partner_CountryName',          
        'FlowDesc': 'Trade_Type',
        'PrimaryValue': 'Trade_Amount'
    })

    # Map CmdCode to short descriptions
    cmdcode_mapping = {
        90111: 'Coffee, Green',
        90112: 'Coffee, Green Decaf',
        90121: 'Coffee, Roasted',
        90122: 'Coffee, Roasted Decaf'
    }

    # Apply the mapping to create a new column with short descriptions
    df['Product_Type'] = df['CmdCode'].map(cmdcode_mapping)

    # Reorder columns to place 'Product_Type' after 'CmdDesc'
    cols = list(df.columns)
    cmd_desc_index = cols.index('CmdDesc')
    cols.insert(cmd_desc_index + 1, cols.pop(cols.index('Product_Type')))
    df = df[cols]

    return df


# Function to get Top 5 Export Countries per Year
def top_export_countries_per_year(df: pd.DataFrame):
    # Filter Data for Imports using the updated 'Trade_Type' column
    exports_df = df[df['Trade_Type'] == 'Export']
    # Group by Year, Partner_CountryName (partner country for the export), and Product_Type (commodity code)
    top_exports = (exports_df.groupby(['Year', 'Partner_CountryName', 'Product_Type'])
                   # Calculate the sum of quantity (Qty_in_kg) and monetary value of the trade (Trade_Amount) for each group.
                   .agg({'Qty_in_kg': 'sum', 'Trade_Amount': 'sum'})
                   .reset_index())
    
    top_exports = (top_exports.sort_values(['Year', 'Qty_in_kg'], ascending=[True, False])
                   .groupby('Year')
                   .head(5))  # Get top 5 entries for each year
    return top_exports

# To visualize the top 5 export countries for a given range of years
def plot_top_export_countries(df: pd.DataFrame):
    plt.figure(figsize=(12, 8))
    # The x-axis of the bar plot represents the quantity exported
    # The y-axis represents the names of the partner countries (countries to which the goods are exported).
    sns.barplot(x='Qty_in_kg', y='Partner_CountryName', hue='Year', data=df, palette='Paired', errorbar=None)
    plt.title('Top 5 Export Countries per Year')
    plt.xlabel('Quantity Exported (Billions kg)')
    plt.ylabel('Partner Country')
    plt.legend(title='Year', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()

# Function to get Top 5 Import Countries per Year
def top_import_countries_per_year(df: pd.DataFrame):
    # Filter Data for Imports using the updated 'Trade_Type' column
    imports_df = df[df['Trade_Type'] == 'Import']
    
    # Group by Year, Partner_CountryName (partner country for the import), and Product_Type (commodity code)
    top_imports = (imports_df.groupby(['Year', 'Partner_CountryName', 'Product_Type'])
                   # Calculate the sum of quantity (Qty_in_kg) and monetary value of the trade (Trade_Amount) for each group.
                   .agg({'Qty_in_kg': 'sum', 'Trade_Amount': 'sum'})
                   .reset_index())
    
    # Sort and Identify Top 10 Importers per year based on the quantity (Qty_in_kg)
    top_imports = (top_imports.sort_values(['Year', 'Qty_in_kg'], ascending=[True, False])
                   .groupby('Year')
                   .head(5))  # Get top 5 entries for each year
    
    return top_imports

def plot_top_import_countries(top_imports: pd.DataFrame):
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Qty_in_kg', y='Partner_CountryName', hue='Year', data=top_imports, errorbar=None)
    plt.title('Top 10 Import Countries per Year')
    plt.xlabel('Quantity Imported (kg)')
    plt.ylabel('Partner Country')
    plt.legend(title='Year', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()

# Function to get Coffee Trading data grouped per period by Year, Trade_Type and Product_Type
def calculate_grouped_coffee_data(df: pd.DataFrame):
    grouped_df = (df.groupby(['Year', 'Trade_Type', 'Product_Type'])
                  .agg({'Qty_in_kg': 'sum', 'Trade_Amount': 'sum'})
                  .reset_index())
    return grouped_df