from flock.base import BaseMultiProc
from flock.tools import split_chunks
from pandas import concat


class DataFrameAsync(object):

    @classmethod
    def applyInRows(cls, args):
        func, block_df = args
        _df2 = block_df.copy()
        list_rows = []

        for i in range(len(_df2)):
            list_rows.append(_df2.iloc[i:i+1])

        bp2 = BaseMultiProc()
        res2 = bp2.executeAsync(func, list_rows)
        res2 = concat(res2)
        return res2

    @classmethod
    def apply(cls, dataframe, function, style="row-like",
              chunksize=100, poolSize=5):
        _df = dataframe.copy()
        iterator = split_chunks(_df, _type="dataframe", size=chunksize)

        bp = BaseMultiProc(poolSize=poolSize)

        if style == "row-like":
            iterator = [(function, el) for el in iterator]
            res = bp.executeAsync(cls.applyInRows, iterator)

        elif style == "block-like":
            res = bp.executeAsync(function, iterator)

        else:
            raise Exception("Style-type not supported")

        res = concat(res)
        res = res.sort_index()
        return res
