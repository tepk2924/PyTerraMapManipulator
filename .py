import numpy as np

A = np.zeros((5, 5, 3), dtype=np.int32)
A[2, 2, :] = [5, 5, False]
print(A)