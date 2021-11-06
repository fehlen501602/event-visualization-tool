import numpy as np


def generate_event_histogram(events, shape):
         """
         Events: N x 4, where cols are x, y, t, polarity, and polarity is in {0,1}. x and y correspond to image
         coordinates u and v.
         """
         H, W = shape
         #x, y, t, p = events #ValueError: too many values to unpack (expected 4)
         x, y, t, p = events.T
         x = x.astype(np.int)
         y = y.astype(np.int)

         img_pos = np.zeros((H * W,), dtype="float32")
         img_neg = np.zeros((H * W,), dtype="float32")

         np.add.at(img_pos, x[p == 1] + W * y[p == 1], 1)
         np.add.at(img_neg, x[p == -1] + W * y[p == -1], 1)

         histogram = np.stack([img_neg, img_pos], -1).reshape((H, W, 2))

         return histogram