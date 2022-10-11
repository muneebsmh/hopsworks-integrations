import pandas as pd
from itertools import cycle

def is_scalar(obj):
    if isinstance(obj, str):
        return True
    elif hasattr(obj, "__iter__"):
        return False
    else:
        return True

def multi_melt(
        df: pd.DataFrame,
        id_vars=None,
        value_vars=None,
        var_name=None,
        value_name="value",
        col_level=None,
        ignore_index=True,
    ) -> pd.DataFrame:
    value_vars = value_vars if not is_scalar(value_vars[0]) else [value_vars]
    var_name = var_name if not is_scalar(var_name) else cycle([var_name])
    value_name = value_name if not is_scalar(value_name) else cycle([value_name])

    melted_dfs = [
        (
            df.melt(
                id_vars,
                *melt_args,
                col_level,
                ignore_index,
            ).pipe(lambda df: df.set_index([*id_vars, df.groupby(id_vars).cumcount()]))
        )
        for melt_args in zip(value_vars, var_name, value_name)
    ]

    return (
        pd.concat(melted_dfs, axis=1)
        .reset_index()
    )

def call_multi_melt(df: pd.DataFrame, id_vars: list, value_vars: list, value_name: list):
    df_melted = df.pipe(
        multi_melt,
        id_vars=id_vars,
        value_vars=value_vars,
        value_name=value_name,
    )
    return df_melted