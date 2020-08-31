import numpy as np

def rounding(x):
    def pipage_round(x):
        y = x.clone()
        T = []
        for i in range(len(y)):
            if (0 < y[i] and y[i] < 1):
                T.append(i)

        try:
            while (len(T) > 0):
                i, j = T[0], T[1]
                if (y[i] + y[j] < 1):
                    p = y[j] / (y[i] + y[j])
                    if (np.random.rand() < p):
                        y[j] += y[i]
                        y[i] = 0.
                        del T[0]
                    else:
                        y[i] += y[j]
                        y[j] = 0.
                        del T[1]
                else:
                    p = (1. - y[i]) / (2. - y[i] - y[j])
                    if (np.random.rand() < p):
                        y[i] += y[j] - 1.
                        y[j] = 1.
                        del T[1]
                        if (y[i] == 0.):
                            del T[0]
                    else:
                        y[j] += y[i] - 1.
                        y[i] = 1.
                        del T[0]
                        if (y[j] == 0.):
                            del T[0]
        except:
            return y
        return y

    def regularize_answer(ans):
        pp = pipage_round(ans)
        pp[pp < 1] = 0.
        return pp

    px = regularize_answer(x)
    return px
    # v = [i for i in range(len(x)) if px[i] != 0]
    # return v[0]