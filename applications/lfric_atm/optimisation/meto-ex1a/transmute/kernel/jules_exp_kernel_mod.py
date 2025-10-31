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
from psyclone.psyir.nodes import Call, Loop


omp_transform_par_do = OMPLoopTrans(
    omp_schedule="static",
    omp_directive="paralleldo")

SAFE_IMPURE_CALLS = ["qsat_mix"]

def trans(psyir):
    '''
    PSyclone function call, run through psyir object,
    each schedual (or subroutine) and apply paralleldo transformations
    to each loop in large scale precip.
    '''

    for loop in psyir.walk(Loop):
        if not loop.ancestor(Loop):
            options = {"ignore_dependencies_for": [
                "z0msea_2d", 
                "tstar_land", 
                "sea_ice_pensolar", 
                "rhostar_2d", 
                "recip_l_mo_sea_2d", 
                "h_blend_orog_2d", 
                "t1_sd_2d", 
                "q1_sd_2d", 
                "surf_interp", 
                "rhokm_bl", 
                "rhokh_bl", 
                "moist_flux_bl", 
                "heat_flux_bl", 
                "gradrinr", 
                "alpha1_tile", 
                "fracaero_t_tile", 
                "fracaero_s_tile", 
                "z0h_tile", 
                "z0m_tile", 
                "chr1p5m_tile", 
                "resfs_tile", 
                "gc_tile", 
                "canhc_tile", 
                "ashtf_prime_tile", 
                "dtstar_tile", 
                "rhokh_tile", 
                "blend_height_tq", 
                "z0m_eff", 
                "ustar", 
                "soil_moist_avail", 
                "snow_unload_rate", 
                "tile_temperature", 
                "tile_heat_flux", 
                "tile_moisture_flux", 
                "z0m_2d", 
                "dust_div_flux", 
                "tile_water_extract", 
                "net_prim_prod", 
                "surface_conductance", 
                "thermal_cond_wet_soil", 
                "soil_respiration", 
                "gross_prim_prod", 
                "z0h_eff",
                "fluxes%tstar_ij",
                ],
                "node-type-check": False}
            try:
                impure_calls = [c for c in loop.walk(Call) if not c.is_pure]
                for call in impure_calls:
                    if call.routine.symbol.name in SAFE_IMPURE_CALLS:
                        print(call.routine.name)
                        call.routine.symbol.is_pure = True
                omp_transform_par_do.apply(loop, options)

            except (TransformationError, IndexError) as err:
                logging.warning(
                    "Could not transform because:\n %s", err)

#Ignore loops setting these as order dependent: land_field l ainfo%land_index sea_pts ainfo%sea_index ainfo%sice_pts_ncat ainfo%sice_index_ncat
#Ignore as calls subroutine: qsat_mix
