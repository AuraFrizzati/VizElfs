import pandas as pd
import os

def filter_cardiff(df, lookup, csv_name = "Cardiff_lookup"):
    try:
        print("function filter_cardiff started ...")
        # local_authority == "Cardiff"
        cardiff_codes = lookup.loc[lookup['local_authority'] == "Cardiff", 'small_area'].tolist()
        df = df[df['small_area'].isin(cardiff_codes)]
        df_lookup = pd.merge(df, lookup, how='inner', on='small_area')
        # Remove 'Unnamed' and 'nation' columns, move 'local_authority' as first
        cols = [col for col in df_lookup.columns if col not in ['Unnamed: 4', 'nation']]
        cols = ['local_authority'] + [col for col in cols if col != 'local_authority']
        df_lookup = df_lookup[cols]
        df_lookup.to_csv(f"data/{csv_name}.csv", index=False)
    except Exception as e:
        print(f"An error occurred in filter_cardiff: {e}")

    print("function filter_cardiff completed")

    return df_lookup 

def main():
    print(os.getcwd())
    # import level 3 raw data
    level_3 =  pd.read_excel("data/Level_3.xlsx")
    lookup = pd.read_excel("data/lookups.xlsx")
    filter_cardiff(level_3, lookup)

    return

if __name__ == "__main__":
    main()

