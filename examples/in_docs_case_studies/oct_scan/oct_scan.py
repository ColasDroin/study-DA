# ==================================================================================================
# --- Imports
# ==================================================================================================

# Import standard library modules
import os

# Import third-party modules
# Import user-defined modules
from study_da import create, submit
from study_da.utils import load_template_configuration_as_dic, write_dic_to_path

# ==================================================================================================
# --- Script to generate a study
# ==================================================================================================

# Load the template configuration
name_template_config = "config_runIII.yaml"
config, ryaml = load_template_configuration_as_dic(name_template_config)

# Do changes if needed
# config["config_simulation"]["n_turns"] = 1000000

# Drop the configuration locally
write_dic_to_path(config, "config_runIII.yaml", ryaml)

# Now generate the study in the local directory
path_tree, name_main_config = create(path_config_scan="config_scan.yaml", force_overwrite=False)

# Delete the configuration
os.remove("config_runIII.yaml")

# ==================================================================================================
# --- Script to submit the study
# ==================================================================================================

# In case gen_1 is submitted locally
dic_additional_commands_per_gen = {
    # To clean up the folder after the first generation if submitted locally
    1: "rm -rf final_* modules optics_repository optics_toolkit tools tracking_tools temp mad_collider.log __pycache__ twiss* errors fc* optics_orbit_at* \n"
    # To copy back the particles folder from the first generation if submitted to HTC
    # "cp -r particles $path_job/particles \n",
}

# Dependencies for the executable of each generation. Only needed if one uses HTC or Slurm.
dic_dependencies_per_gen = {
    1: ["acc-models-lhc"],
    2: ["path_collider_file_for_configuration_as_input", "path_distribution_folder_input"],
}

# Submit the study
submit(
    path_tree=path_tree,
    path_python_environment="/afs/cern.ch/work/c/cdroin/private/study-DA/.venv",
    path_python_environment_container="/usr/local/DA_study/miniforge_docker",
    path_container_image="/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/cdroin/da-study-docker:757f55da",
    dic_dependencies_per_gen=dic_dependencies_per_gen,
    name_config=name_main_config,
    dic_additional_commands_per_gen=dic_additional_commands_per_gen,
    one_generation_at_a_time=True,
)
