import datetime
# import pandas as pd

def add_hour_timestamp(timestamp_str, format_timestamp="%Y%m%d_%H%M%S", hours=7):
    timestamp_date = datetime.datetime.fromisoformat(timestamp_str)
    timestamp_date = timestamp_date + datetime.timedelta(hours=hours)
    timestamp_str = datetime.datetime.strftime(timestamp_date, format_timestamp)

    return timestamp_date, timestamp_str

def changeTimestampFormatFromISO(timestamp_iso_str, format_timestamp="%Y%m%d_%H%M%S"):
    timestamp_date = datetime.datetime.fromisoformat(timestamp_iso_str)
    # timestamp_date = timestamp_date + datetime.timedelta(hours=hours)
    timestamp_str = datetime.datetime.strftime(timestamp_date, format_timestamp)

    return timestamp_str, timestamp_date

def changeTimestampToDatetime(df, header_time, format_time='iso'):
    timestamp_str = df[header_time].values
    timestamp_str = timestamp_str.astype(datetime64)
    if format_time == 'iso':
        timestamp_date = datetime.datetime.fromisoformat(timestamp_str)

    df[header_time] = timestamp_date

    return df
