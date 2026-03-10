import xarray as xr
import numpy as np
import pandas as pd
import cftime

class ClimateFile: 
    def __init__(self, file_path, variable_name, output_name):
        self.file_path = file_path
        self.variable_name = variable_name
        self.output_name = output_name

# ADAPT for your one
files = [#ClimateFile("whiplash/data/wb/TIPPECC_b_CLMcom-KIT-CCLM5-0-15_v1_MOHC-HadGEM2-ES__water_budget_1950_2099__mm_bb_26.34_32.28_-31.18_-25.02.nc", "water_budget_from_tas", "water_budget"), 
         #ClimateFile("whiplash/data/wb/TIPPECC_b_GERICS-REMO2015_v1_MPI-M-MPI-ESM-LR__water_budget_1970_2100__mm_bb_26.34_32.28_-31.18_-25.02.nc", "water_budget_from_tas", "water_budget"),
         # ClimateFile("whiplash/data/wb/TIPPECC_b_GERICS-REMO2015_v1_NCC-NorESM1-M__water_budget_1970_2100__mm_bb_26.34_32.28_-31.18_-25.02.nc", "water_budget_from_tas", "water_budget")
]

lat = -30
lon = 27
beg = 2000
end = 2020
out_file = "summer_school_Tippecc/output/test.txt"

def calculate_day_of_year(time_values):
    """
    Calculate the day of the year for a given calendar type.

    Args:
        time_values: Array of cftime datetime objects.
        calendar_type: Type of calendar ('standard', 'noleap', '360_day').

    Returns:
        List of day of year values.
    """
    day_of_year = []
    for t in time_values:
        if isinstance(t, cftime.DatetimeNoLeap) or isinstance(t, cftime.DatetimeGregorian) or isinstance(t, cftime.Datetime360Day):
            # Handle cftime objects
            if isinstance(t, cftime.Datetime360Day):
                doy = (t.month - 1) * 30 + t.day
            else:
                doy = t.dayofyr
        else:
            # Handle numpy.datetime64 objects
            t_pd = pd.Timestamp(t)
            doy = t_pd.dayofyear
        day_of_year.append(doy)
    return day_of_year

def transform_time(time):

    # Check if time_values are cftime or numpy.datetime64
    is_cftime = hasattr(time[0], 'year')

    # Calculate last two digits of year and day of year
    if is_cftime:
        year = [t.year for t in time]
    else:
        year = [pd.Timestamp(t).year for t in time]

    day_of_year = calculate_day_of_year(time)
    time_new = [f"{str(y)[2:]}{d:03d}" for y, d in zip(year, day_of_year)]
    return time_new
    

has_time = False
value_list = []
for file in files:
    dataset = xr.open_dataset(file.file_path)
    dataset = dataset.sel(time=slice(str(beg), str(end)))
    if not has_time:
        time = transform_time(dataset.time.values)
        has_time = True
    variable = dataset[file.variable_name]
    # Do something with the variable, e.g., extract values at specific coordinates
    values = variable.sel(lat=lat, lon=lon, method="nearest")
    value_list.append(values.values)

with open(out_file, "w") as f:
    f.write(f"@ INSI LAT LONG  ELEV TAV  AMP REFHT WNDHT\n")
    f.write(f"- {round(lat, 2)} {round(lon, 2)} 0 0 0 0 0\n")
    f.write(f"@Date ")
    for file in files:
        f.write(f"{file.output_name} ")
    f.write("\n")
    for i in range(len(time)):
        f.write(f"{time[i]} ")
        for v in value_list:
            f.write(f"{round(v[i], 2)} ")
        f.write("\n")
