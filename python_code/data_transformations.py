import pandas as pd
import os
# 
def filter_cardiff(csv_name = "Cardiff_lookup_wimd"):
    try:
        print("function filter_cardiff started ...")
        print("reading level 3 data...")
        level_3 =  pd.read_excel("data/Level_3.xlsx")
        print("reading lookup data...")
        lookup = pd.read_excel("data/lookups.xlsx")
        wimd_url = "https://www.gov.wales/sites/default/files/statistics-and-research/2025-11/wimd-2025-index-and-domain-ranks-by-small-area.ods"
        wimd_df = pd.read_excel(wimd_url, engine='odf', 
                                sheet_name='Deciles_quintiles_quartiles'
                                ,skiprows=3)

        cardiff_codes = lookup.loc[lookup['local_authority'] == "Cardiff", 'small_area'].tolist()
        df = df[df['small_area'].isin(cardiff_codes)]
        
        print("merge with lookup ...")
        df_lookup = pd.merge(df, lookup, how='inner', on='small_area')
        # Remove 'Unnamed' and 'nation' columns, move 'local_authority' as first
        cols = [col for col in df_lookup.columns if col not in ['Unnamed: 4', 'nation']]
        cols = ['local_authority'] + [col for col in cols if col != 'local_authority']
        df_lookup = df_lookup[cols]

        # merge with wimd data
        print("merge with WIMD data ...")
        df_lookup_wimd = pd.merge(df_lookup, wimd_df, how='inner', left_on='small_area', right_on = 'LSOA code')
        
        df_lookup_wimd = df_lookup_wimd.drop(columns=[
            'local_authority',
            'small_area',
            'Local Authority name (Eng)',
            'WIMD 2025 overall quartile',
            'WIMD 2025 overall deprivation group'
            ])


        df_lookup_wimd.to_csv(f"data/{csv_name}.csv", index=False)
    except Exception as e:
        print(f"An error occurred in filter_cardiff: {e}")

    print("function filter_cardiff completed")

    # return df_lookup 

def main():
    print(os.getcwd())
    # filter_cardiff()
    cardiff_lookup_wimd = pd.read_csv("data/Cardiff_lookup_wimd.csv")
    print(cardiff_lookup_wimd.head())
    print(cardiff_lookup_wimd.dtypes)



    
if __name__ == "__main__":
    main()

