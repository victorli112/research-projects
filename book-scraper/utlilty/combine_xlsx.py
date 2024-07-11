import pandas as pd

def combine_xlsx(doc1, doc2, output_file):
    # Load the Excel files
    xls1 = pd.ExcelFile(doc1)
    xls2 = pd.ExcelFile(doc2)

    # Get the sheet names
    sheet_names1 = xls1.sheet_names
    sheet_names2 = xls2.sheet_names

    # Check if both documents have the same sheet names
    assert sheet_names1 == sheet_names2, "The documents have different sheets."

    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    # Iterate over each sheet
    for sheet in sheet_names1:
        df1 = pd.read_excel(xls1, sheet_name=sheet)
        df2 = pd.read_excel(xls2, sheet_name=sheet)

        # Print the initial number of rows
        print(f"Initial number of rows in '{sheet}' of document 1: {len(df1)}")
        print(f"Initial number of rows in '{sheet}' of document 2: {len(df2)}")

        # Concatenate the dataframes
        df = pd.concat([df1, df2])

        # Drop duplicates based on 'title' and 'author'
        df = df.drop_duplicates(subset=['Title', 'Author'])

        # Write each dataframe to a different worksheet
        df.to_excel(writer, sheet_name=sheet, index=False)

        # Print the final number of rows
        print(f"Final number of rows in '{sheet}' after combining: {len(df)}\n")

    # Close the Pandas Excel writer and output the Excel file
    writer.close()

combine_xlsx("rest.xlsx", "comtempAndLiteraria.xlsx", "groupo_planeta_books.xlsx")