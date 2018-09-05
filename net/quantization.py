import torch
import numpy as np
from sklearn.cluster import KMeans
from scipy.sparse import csc_matrix, csr_matrix


def apply_weight_sharing(model):
    """
    Applies weight sharing to the given model
    """
    for module in model.children():
        dev = module.weight.device
        weight = module.weight.data.cpu().numpy()
        original_shape = weight.shape
        csr = csr_matrix(weight)
        min_ = min(csr.data)
        max_ = max(csr.data)
        space = np.linspace(min_, max_, num=32)
        kmeans = KMeans(n_clusters=len(space), init=space.reshape(-1,1), n_init=1, precompute_distances=True, algorithm="full")
        kmeans.fit(csr.data.reshape(-1,1))
        new_weight = kmeans.cluster_centers_[kmeans.labels_].reshape(-1)
        csr.data = new_weight
        module.weight.data = torch.from_numpy(csr.toarray()).to(dev)


