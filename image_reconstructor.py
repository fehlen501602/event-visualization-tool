import numpy as np
import matplotlib.pyplot as plt


def image_reconstructor(histogram, path_name=None):
    """Visualizes the input histogram"""
    height, width, _ = histogram.shape
    np_image = np.zeros([height, width, 3])

    if histogram.shape[-1] != 2:
        height, width, nr_channels = histogram.shape
        # If histogram has not 2 channels, the event representation is a event queue. Get polarity
        polarity_histogram = histogram[:, :, -(nr_channels//2):].copy()
        histogram = np.zeros([height, width, 2])
        histogram[:, :, 0] = np.abs((polarity_histogram * (polarity_histogram == -1)).sum(-1))
        histogram[:, :, 1] = (polarity_histogram * (polarity_histogram == 1)).sum(-1)

    np_image += (histogram[:, :, 1])[:, :, None] * np.array([0, 1, 0])[None, None, :]
    np_image += (histogram[:, :, 0])[:, :, None] * np.array([1, 0, 0])[None, None, :]
    np_image = np_image.clip(0, 1)

    if path_name is None:
        return np_image
    else:
        fig, ax = plt.subplots()
        ax.imshow(np_image.astype(np.float))
        ax.axis('off')
        fig.savefig(path_name)
        plt.close()
