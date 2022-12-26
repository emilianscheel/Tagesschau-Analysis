import numpy as np
import pandas as pd
from datetime import datetime as dt
from scipy.interpolate import interp1d


def week_year_to_timestamp(row):
    date = "{}-{}-1".format(row["year"], row["week"])
    return dt.strptime(date, "%Y-%W-%w").timestamp()


def create_interpolation_from(df, ucolumn='timestamp', columns=[]):
    """Gibt einen DataFrame mit interpolierten Werten zurück.

        Wird kein Parameter `unique` übergeben, wird `timestamp` als Wert verwendet.

        Parameters
        ----------
        df : DataFrame, required
            The DateFrame to be used
        ucolumn : str, optional
            Column of DataFrame for the x values
        columns : list
            Columns of DataFrame that should be adjusted
        """
    df_copy = df

    df_interpolation = pd.DataFrame()
    df_interpolation.index = np.arange(
        df_copy[ucolumn].min(), df_copy[ucolumn].max(), 100)

    for column in columns:
        cubic_interpolation = interp1d(
            df_copy[ucolumn], df[column], kind="cubic")
        df_interpolation[column] = cubic_interpolation(df_interpolation.index)

    df_interpolation.index.name = ucolumn
    df_interpolation = df_interpolation.reset_index(ucolumn)

    return df_interpolation


def plot_trendlines(df, on_axis=None, ucolumn='timestamp', colors=[], columns=[]):
    """Gibt einen DataFrame mit interpolierten Werten zurück.

        Wird kein Parameter `unique` übergeben, wird `timestamp` als Wert verwendet.

        Parameters
        ----------
        df : DataFrame, required
            The DateFrame to be used
        ucolumn : str, optional
            Column of DataFrame for the x values
        columns : list
            Columns of DataFrame that should be adjusted
        """
    for index in range(len(columns)):
        z = np.polyfit(df[ucolumn], df[columns[index]], 1)
        p = np.poly1d(z)
        on_axis.plot(df[ucolumn], p(df[ucolumn]), color=colors[index])


def merge_data_week_year(df, from_column='topic', to_columns=[]):
    df_all = None
    for column in to_columns:
        # Betrachte nur die Artikel des aktuellen Themengebiets
        df_column = df.loc[df[from_column] == column]
        # Gruppiere die Artikel nach Woche (eindeutig) und aggregiere die Anzahl der Artikel pro Woche
        df_column = df_column.groupby(
            ["week", "year"]).size().reset_index(name=column)

        # Füge ein neues Feature hinzu: Datum
        df_column['date'] = "KW " + \
            df_column['week'].astype(str) + " " + df_column['year'].astype(str)
        df_column['timestamp'] = df_column.apply(
            week_year_to_timestamp, axis=1)

        # Lösche zwei Features: Woche, Jahr
        df_column.drop(['week', 'year'], axis=1, inplace=True)

        # Falls der df der Gesamtdaten bereits Daten von vorherigen Themengebieten enthält, merge die Daten des aktuellen Themengebiets
        if (isinstance(df_all, pd.DataFrame)):
            df_all = pd.merge(df_all, df_column, how='outer',
                              on=["timestamp", "date"])
        # Initialisiere den df der Gesamtdaten mit den Daten des aktuellen Themengebiets
        else:
            df_all = df_column

    return df_all


def merge_data_week_year2(df, from_column='topic', to_columns=[], perform_group=None):
    df_all = None
    for column in to_columns:
        # Betrachte nur die Artikel des aktuellen Themengebiets
        df_column = df.loc[df[from_column] == column]
        # Gruppiere die Artikel nach Woche (eindeutig) und aggregiere die Anzahl der Artikel pro Woche
        df_column = perform_group(df_column, column)

        # Füge ein neues Feature hinzu: Datum
        df_column['date'] = "KW " + \
            df_column['week'].astype(str) + " " + df_column['year'].astype(str)
        df_column['timestamp'] = df_column.apply(
            week_year_to_timestamp, axis=1)

        # Lösche zwei Features: Woche, Jahr
        df_column.drop(['week', 'year'], axis=1, inplace=True)

        # Falls der df der Gesamtdaten bereits Daten von vorherigen Themengebieten enthält, merge die Daten des aktuellen Themengebiets
        if (isinstance(df_all, pd.DataFrame)):
            df_all = pd.merge(df_all, df_column, how='outer',
                              on=["timestamp", "date"])
        # Initialisiere den df der Gesamtdaten mit den Daten des aktuellen Themengebiets
        else:
            df_all = df_column

    return df_all
