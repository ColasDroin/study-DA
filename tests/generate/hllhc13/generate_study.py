# ==================================================================================================
# --- Imports
# ==================================================================================================

# Import standard library modules
import os

# Import third-party modules
# Import user-defined modules
from study_da import create
from study_da.utils import load_dic_from_path, write_dic_to_path

# ==================================================================================================
# --- Script to generate a study
# ==================================================================================================

# Load the configuration
config, ryaml = load_dic_from_path(
    "../../../study_da/generate/template_configurations/config_hllhc13.yaml"
)

# Update the location of acc-models
config["config_mad"]["links"]["acc-models-lhc"] = (
    "../../../../../external_dependencies/acc-models-lhc-v13"
)
# Adapt the number of turns
config["config_simulation"]["n_turns"] = 100

# Drop the configuration locally
write_dic_to_path(config, "config_hllhc13.yaml", ryaml)

# Now generate the study in the local directory
create(path_config="config_scan.yaml", tree_file=True, force_overwrite=True)

# Delete the configuration
os.remove("config_hllhc13.yaml")
