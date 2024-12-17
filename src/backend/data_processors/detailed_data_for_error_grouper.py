from backend.json_config_loader import JSONConfigReader
def get_detailed_data_for_error_groups(ecl_df, error_grps, jcr: JSONConfigReader):
    detailed_error_groups = {}
    for grp_name, grp_df in error_grps.items():
        # Get the list of descriptions in this group
        descriptions = grp_df[jcr.get_error_description()].unique()
        # Filter the ecl_df for rows with these descriptions
        detailed_df = ecl_df[ecl_df[jcr.get_error_description()].isin(descriptions)].reset_index(drop=True)
        detailed_error_groups[grp_name] = detailed_df
    return detailed_error_groups
