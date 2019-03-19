import numpy as np
from typing import Union
import xarray as xr

from .external import closedform_glm_mean, closedform_glm_scale
from .external import SparseXArrayDataArray


def closedform_norm_glm_mean(
        X: Union[xr.DataArray, SparseXArrayDataArray],
        design_loc,
        constraints_loc,
        size_factors=None,
        link_fn=lambda x: x,
        inv_link_fn=lambda x: x
):
    r"""
    Calculates a closed-form solution for the `mean` parameters of normal GLMs.

    :param X: The sample data
    :param design_loc: design matrix for location
    :param constraints: tensor (all parameters x dependent parameters)
        Tensor that encodes how complete parameter set which includes dependent
        parameters arises from indepedent parameters: all = <constraints, indep>.
        This form of constraints is used in vector generalized linear models (VGLMs).
    :param size_factors: size factors for X
    :return: tuple: (groupwise_means, mean, rmsd)
    """
    return closedform_glm_mean(
        X=X,
        dmat=design_loc,
        constraints=constraints_loc,
        size_factors=size_factors,
        weights=None,
        link_fn=link_fn,
        inv_link_fn=inv_link_fn
    )


def closedform_norm_glm_logsd(
        X: Union[xr.DataArray, SparseXArrayDataArray],
        design_scale: xr.DataArray,
        constraints=None,
        size_factors=None,
        groupwise_means=None,
        link_fn=np.log
):
    r"""
    Calculates a closed-form solution for the log-scale parameters of normal GLMs.

    :param X: The sample data
    :param design_scale: design matrix for scale
    :param constraints: some design constraints
    :param size_factors: size factors for X
    :param weights: the weights of the arrays' elements; if `none` it will be ignored.
    :param mean: optional, if there are for example different mean's per observation.
    :param groupwise_means: optional, in case if already computed this can be specified to spare double-calculation
    :return: tuple (groupwise_scales, logsd, rmsd)
    """

    def compute_scales_fun(variance, mean):
        groupwise_scales = np.sqrt(variance)
        return groupwise_scales

    return closedform_glm_scale(
        X=X,
        design_scale=design_scale,
        constraints=constraints,
        size_factors=size_factors,
        groupwise_means=groupwise_means,
        link_fn=link_fn,
        compute_scales_fun=compute_scales_fun
    )