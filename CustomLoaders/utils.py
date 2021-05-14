def check_if_passes_filters_using_csv_df(df_row, filters):
    meets_filter = []
    for filter_key, filter_values in zip(filters.keys(), filters.values()):
        if filters[filter_key] is not None:
            if df_row.at[filter_key] in filter_values:
                meets_filter.append(True)
            else:
                meets_filter.append(False)
    return all(meets_filter)

