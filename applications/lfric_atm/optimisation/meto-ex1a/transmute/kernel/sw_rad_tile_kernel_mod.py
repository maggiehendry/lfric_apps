##############################################################################
# Copyright (c) 2025,  Met Office, on behalf of HMSO and Queen's Printer
# For further details please refer to the file LICENCE.original which you
# should have received as part of this distribution.
##############################################################################
'''
Bespoke Opt script for mphys_kernel_mod to add OpenMP to loops present in
the Kernel.
As Psyclone is detecting a number of lhs rhs dependencies due to the
copies in an out of the kernel, we are needing to provide a list of
ignore_dependencies_for in the transformation options list.
'''

import logging
from psyclone.transformations import (
    OMPLoopTrans,
    TransformationError)
from psyclone.psyir.nodes import Loop


omp_transform_par_do = OMPLoopTrans(
    omp_schedule="static",
    omp_directive="paralleldo")


def trans(psyir):
    '''
    PSyclone function call, run through psyir object,
    each schedual (or subroutine) and apply paralleldo transformations
    to each loop in large scale precip.
    '''

    for loop in psyir.walk(Loop):
        if not loop.ancestor(Loop):
            options = {"ignore_dependencies_for": [
                "albedo_obs_scaling", 
                "tile_sw_direct_albedo", 
                "tile_sw_diffuse_albedo", 
                "sea_ice_pensolar_frac_direct", 
                "sea_ice_pensolar_frac_diffuse", 
                ],
                "node-type-check": False}
            try:
                omp_transform_par_do.apply(loop, options)

            except (TransformationError, IndexError) as err:
                logging.warning(
                    "Could not transform because:\n %s", err)

#Ignore loops setting these as order dependent: land_field l ainfo%land_index sea_pts ainfo%sea_index ainfo%sice_pts_ncat ainfo%sice_index_ncat
