# -*- coding: utf-8 -*-
"""scipy 없이 쓰는 작은 형태 연산(내장 파이썬에 scipy 가 없다)."""
import numpy as np

def dilate(m, r):
    """정사각 r 반경 팽창(누적합)."""
    m = m.astype(np.int32)
    p = np.pad(m, r)
    c = p.cumsum(0).cumsum(1)
    c = np.pad(c, ((1, 0), (1, 0)))
    k = 2 * r + 1
    s = c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]
    return s > 0
