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
                "tstar_land", 
                "sea_ice_pensolar", 
                "ashtf_prime_sea", 
                "dtstar_sea", 
                "ashtf_prime", 
                "dtstar_sice", 
                "heat_flux_bl", 
                "moist_flux_bl", 
                "tile_heat_flux", 
                "tile_moisture_flux", 
                "tile_temperature", 
                "screen_temperature", 
                "tile_heat_flux", 
                "tile_moisture_flux", 
                "snowice_sublimation", 
                "surf_heat_flux", 
                "canopy_evap", 
                "snowice_melt", 
                "time_since_transition", 
                "surf_ht_flux", 
                "water_extraction", 
                "lake_evap", 
                "snomlt_surf_htf", 
                "soil_evap", 
                "soil_surf_ht_flux", 
                "t1p5m", 
                "q1p5m", 
                "qcl1p5m", 
                "rh1p5m", 
                "t1p5m_ssi", 
                "q1p5m_ssi", 
                "qcl1p5m_ssi", 
                "rh1p5m_ssi", 
                "t1p5m_land_loc", 
                "q1p5m_land_loc", 
                "t1p5m_land", 
                "q1p5m_land", 
                "qcl1p5m_land", 
                "rh1p5m_land", 
                "t1p5m_surft", 
                "q1p5m_surft", 
                "latent_heat", 
                "surf_sw_net", 
                "surf_radnet", 
                "surf_lw_up", 
                "surf_lw_down", 
                "sea_ice_temperature", 
                "latent_heat", 
                ],
                "node-type-check": False}
            try:
                omp_transform_par_do.apply(loop, options)

            except (TransformationError, IndexError) as err:
                logging.warning(
                    "Could not transform because:\n %s", err)

#Ignore loops setting these as order dependent: land_field l ainfo%land_index sice_pts ainfo%sice_index sea_pts ainfo%sea_inde ainfo%sice_pts_ncat 

