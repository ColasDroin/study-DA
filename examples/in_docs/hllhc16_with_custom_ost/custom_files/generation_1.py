"""This is a template script for generation 1 of simulation study, in which ones generates a
particle distribution and a collider from a MAD-X model."""

# ==================================================================================================
# --- Imports
# ==================================================================================================

# Import standard library modules
import logging
import os
import sys

# Import user-defined modules
from study_da.generate import MadCollider, ParticlesDistribution
from study_da.utils import (
    load_dic_from_path,
    set_item_in_dic,
    write_dic_to_path,
)

# Add path to custom_mad_collider (might need to add ../.., etc. depending on the generation)
sys.path.append("..")
import custom_ost

# Set up the logger here if needed


# ==================================================================================================
# --- Override the MadCollider class
# ==================================================================================================
class MadColliderCustom(MadCollider):
    def __init__(self, configuration: dict):
        super().__init__(configuration)

        self._ost = custom_ost


# ==================================================================================================
# --- Script functions
# ==================================================================================================
def build_distribution(config_particles):
    # Build object for generating particle distribution
    distr = ParticlesDistribution(config_particles)

    # Build particle distribution
    particle_list = distr.return_distribution_as_list()

    # Write particle distribution to file
    distr.write_particle_distribution_to_disk(particle_list)


def build_collider(config_mad):
    # Build object for generating collider from custom MadCollider class
    mc = MadColliderCustom(config_mad)

    # Alternatively, you could directly use the MadCollider class and just update the OST
    # mc = MadCollider(config_mad)
    # mc._ost = custom_ost

    # Or even more precise, you could define a function yourself and override it in the default ost
    # ! Note that the number of arguments must be the same as the original function
    # mc = MadCollider(config_mad)
    # mc.ost.check_madx_lattices = lambda a: print("This is a fake check")

    # Build mad model
    mad_b1b2, mad_b4 = mc.prepare_mad_collider()

    # Build collider from mad model
    collider = mc.build_collider(mad_b1b2, mad_b4)

    # Twiss to ensure everything is ok
    mc.activate_RF_and_twiss(collider)

    # Clean temporary files
    mc.clean_temporary_files()

    # Save collider to json
    mc.write_collider_to_disk(collider)


# ==================================================================================================
# --- Parameters definition
# ==================================================================================================
dict_mutated_parameters = {}  ###---parameters---###
path_configuration = "{} ###---main_configuration---###"

# ==================================================================================================
# --- Script for execution
# ==================================================================================================

if __name__ == "__main__":
    logging.info("Starting script to build particle distribution and collider")

    # Load full configuration
    full_configuration, ryaml = load_dic_from_path(path_configuration)

    # Mutate parameters in configuration
    for key, value in dict_mutated_parameters.items():
        set_item_in_dic(full_configuration, key, value)

    # Dump configuration
    name_configuration = os.path.basename(path_configuration)
    write_dic_to_path(full_configuration, name_configuration, ryaml)

    # Build and save particle distribution
    build_distribution(full_configuration["config_particles"])

    # Build and save collider
    build_collider(full_configuration["config_mad"])

    logging.info("Script finished")
