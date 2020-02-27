from pandas import DataFrame, unique


def generate_df(rows, **kwargs):
    data = []
    columns = ["source", "symbol"]
    if kwargs:
        columns.extend([k for k in kwargs.keys()])

    source = "foo"
    symbol = "bar"
    count = 0

    for i in range(rows):
        if i % 3 == 0:
            count += 1

        d = {
            "source": source,
            "symbol": f"{symbol}_{count}"
        }

        if kwargs:
            items = {k: f"{v}_{i}" for k, v in kwargs.items()}
            d.update(items)

        data.append(d)

    return DataFrame(data, columns=columns)


def merge(df):
    values = [v for v in unique(df.values.ravel("K")).tolist() if v]

    return "[\"{}\"]".format("\", \"".join(values)) if values else "[]"


def main():
    # df1 = generate_df(1000, ric1="ric", ric2="ric2", isin1="isin", isin2="isin2")
    df1 = DataFrame([{"SOURCE": "foo", "SYMBOL": "bar",
                      "RIC1": "a", "ISIN1": "b"},
                     {"SOURCE": "foo", "SYMBOL": "bar",
                      "RIC1": "a", "RIC2": "aa"},
                     {"SOURCE": "foo", "SYMBOL": "bar",
                      "ISIN1": "bb", "ISIN2": "bbb"},
                     {"SOURCE": "foo", "SYMBOL": "baz",
                      "RIC1": "aaa", "ISIN2": "bbb"},
                     {"SOURCE": "foo", "SYMBOL": "baz",
                      "RIC1": "a", "RIC2": "aa", "ISIN1": "b", "ISIN2": "bb"}],
                    columns=["SOURCE", "SYMBOL", "RIC1", "RIC2", "ISIN1", "ISIN2"]).fillna("")
    identifiers = {"RIC": ["RIC1", "RIC2"], "ISIN": ["ISIN1", "ISIN2"]}

    bmrx_df = df1.copy(deep=False)
    bmrx_df = bmrx_df.set_index(["SOURCE", "SYMBOL"])

    for i, cols in identifiers.items():
        df1[i] = df1[i] if i in df1.columns else ""
        for c in cols:
            df1[c] = df1[c] if c in df1.columns else ""

        bmrx_df[i] = df1.groupby(["SOURCE", "SYMBOL"])[cols].apply(merge)

    bmrx_df = bmrx_df.reset_index()

    # drop duplicate rows as all identifiers have been squashed above
    dedupe = ["SOURCE", "SYMBOL"]
    dedupe.extend(list(identifiers.keys()))
    bmrx_df = bmrx_df.drop_duplicates(subset=dedupe).reset_index(drop=True)
    print(bmrx_df)


if __name__ == "__main__":
    main()
