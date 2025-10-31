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
                "canopy_water", 
                "tile_snow_mass", 
                "n_snow_layers", 
                "snow_depth", 
                "tile_snow_rgrain", 
                "snow_under_canopy", 
                "snowpack_density", 
                "snowice_melt", 
                "soil_sat_frac", 
                "water_table", 
                "wetness_under_soil", 
                "surface_runoff", 
                "sub_surface_runoff", 
                "soil_moisture_content", 
                "grid_snow_mass", 
                "throughfall", 
                "snow_layer_thickness", 
                "snow_layer_ice_mass", 
                "snow_layer_liq_mass", 
                "snow_layer_temp", 
                "snow_layer_rgrain", 
                "soil_temperature", 
                "soil_moisture", 
                "unfrozen_soil_moisture", 
                "frozen_soil_moisture", 
                ],
                "node-type-check": False}
            try:
                omp_transform_par_do.apply(loop, options)

            except (TransformationError, IndexError) as err:
                logging.warning(
                    "Could not transform because:\n %s", err)

#Ignore loops setting these as order dependent: land_pts l ainfo%land_index soil_pts ainfo%soil_index lice_pts ainfo%lice_index
