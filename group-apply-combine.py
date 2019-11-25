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


def main():
    df1 = generate_df(1000, ric="ric", ric2="ric2", isin="isin", isin2="isin2")
    identifiers = {"ric": ["ric", "ric2"], "isin": ["isin", "isin2"]}
    df1["x"] = ""

    for i, cols in identifiers.items():
        df1[i] = df1.groupby(["source", "symbol"])[cols].transform(" ".join)
    
    print(df1["ric"])


if __name__ == "__main__":
    main()
