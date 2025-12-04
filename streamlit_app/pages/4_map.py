import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

df_l3 = pd.read_excel("data/Level_3.xlsx")
df_lkup = pd.read_excel("data/lookups.xlsx")


df_lkup = df_lkup.drop('Unnamed: 4', axis=1)
df_lkupCardiff = df_lkup[df_lkup['local_authority'] == "Cardiff"]


df_l3Car = df_l3[
    df_l3['small_area'].isin(df_lkupCardiff['small_area'])
]


shapefile_path = "data/shapefile/small_areas_british_grid.shp"

lsoa_gdf = gpd.read_file(shapefile_path)



lsoa_gdfCar = lsoa_gdf[
    lsoa_gdf['small_area'].isin(df_lkupCardiff['small_area'])
]


lsoa_gdfCar = lsoa_gdfCar.to_crs(epsg=4326)

df_air_2025 = df_l3Car[
    df_l3Car['co-benefit_type'] == 'air_quality'
]



wimd = pd.read_excel(
    "/Users/owenevans/VizElfs/data/wimd-2025-index-and-domain-ranks-by-small-area.ods",
    sheet_name = "Deciles_quintiles_quartiles",
    skiprows=3,
    engine="odf"
)



# Merging main table + lookup + wimd
df_l3Car_lookup = pd.merge(df_l3Car, df_lkupCardiff, how='left', on=['small_area'])

#df_l3Car_lookup.shape
df_l3Car_lookup_wimd= pd.merge(df_l3Car_lookup, wimd, how='left', left_on=['small_area'], right_on=['LSOA code'])



df_l3Car_lookup_wimd.drop(
    columns=['small_area',
             'local_authority',
             'nation',
             'Local Authority name (Eng)',
             'WIMD 2025 overall quartile',
             'WIMD 2025 overall deprivation group'],
    inplace=True
)


unique_values = df_l3Car_lookup_wimd['co-benefit_type'].unique()
print(unique_values)


df_wimd_2025_grouped = (
    df_l3Car_lookup_wimd
    .groupby(['LSOA name (Eng)','LSOA code'], as_index=False)['WIMD 2025 overall quintile']
    .first()
)
df_wimd_2025_grouped.head()


df_wimd_2025_grouped = df_wimd_2025_grouped.rename(
    columns={'LSOA code': 'small_area'}
)

lsoa_cardiff_wimd = lsoa_gdfCar.merge(
    df_wimd_2025_grouped[['small_area', 'WIMD 2025 overall quintile']],
    on='small_area',
    how='left'
)

fig, ax = plt.subplots(figsize=(7, 7))


lsoa_cardiff_wimd.plot(
    column='WIMD 2025 overall quintile',
    cmap='RdYlBu_r',      # red = most deprived, blue = least
    linewidth=0.3,
    edgecolor='black',
    legend=True,
    categorical=True,    # ✅ important for quintiles
    ax=ax,
    missing_kwds={
        "color": "lightgrey",
        "label": "No data"
    }
)

ax.set_title("Cardiff LSOA – WIMD 2025 Overall Quintile", fontsize=14)
ax.set_axis_off()

plt.tight_layout()
plt.show()