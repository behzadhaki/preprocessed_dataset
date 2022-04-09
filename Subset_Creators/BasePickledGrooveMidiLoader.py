
####################################################
# Test 1 -> single subset with all examples
####################################################
from .subsetters import GrooveMidiSubsetter

gmd_all = GrooveMidiSubsetter(
            pickle_source_path="datasets_extracted_locally/GrooveMidi/hvo_0.3.0/Processed_On_13_05_2021_at_12_56_hrs",
            subset="GrooveMIDI_processed_test",
            hvo_pickle_filename="hvo_sequence_data.obj",
            list_of_filter_dicts_for_subsets=None,
    )
tags, subsets = gmd_all.create_subsets()


####################################################
# Test 2 -> Separated by styles
####################################################
from .subsetters import GrooveMidiSubsetter


styles = ["afrobeat", "afrocuban", "blues", "country", "dance",
          "funk", "gospel", "highlife", "hiphop", "jazz",
          "latin", "middleeastern", "neworleans", "pop",
          "punk", "reggae", "rock", "soul"]


list_of_filter_dicts_for_subsets = [{"style_primary": [style]} for style in styles]

gmd_by_style = GrooveMidiSubsetter(
            pickle_source_path="datasets_extracted_locally/GrooveMidi/hvo_0.3.0/Processed_On_13_05_2021_at_12_56_hrs",
            subset="GrooveMIDI_processed_test",
            hvo_pickle_filename="hvo_sequence_data.obj",
            list_of_filter_dicts_for_subsets=list_of_filter_dicts_for_subsets,
    )
tags_by_style, subsets_by_style = gmd_by_style.create_subsets()
for ix, (tag, subset) in enumerate(zip(tags_by_style, subsets_by_style)):
    print("Subset {} --> Tag {} --> n_samples {}".format(ix, tag, len(subset)))

####################################################
# Test 3 -> Separated by styles and beat type
####################################################
from .subsetters import GrooveMidiSubsetter

styles = ["afrobeat", "afrocuban", "blues", "country", "dance",
          "funk", "gospel", "highlife", "hiphop", "jazz",
          "latin", "middleeastern", "neworleans", "pop",
          "punk", "reggae", "rock", "soul"]


list_of_filter_dicts_for_subsets = [{"style_primary": [style], "beat_type": ["beat"]} for style in styles]

gmd_by_styl_and_beat = GrooveMidiSubsetter(
            pickle_source_path="datasets_extracted_locally/GrooveMidi/hvo_0.3.0/Processed_On_13_05_2021_at_12_56_hrs",
            subset="GrooveMIDI_processed_train",
            hvo_pickle_filename="hvo_sequence_data.obj",
            list_of_filter_dicts_for_subsets=list_of_filter_dicts_for_subsets,
    )

tags_by_style_and_beat, subsets_by_style_and_beat = gmd_by_styl_and_beat.create_subsets()
for ix, (tag, subset) in enumerate(zip(tags_by_style_and_beat, subsets_by_style_and_beat)):
    print("Subset {} --> Tag {} --> n_samples {}".format(ix, tag, len(subset)))



####################################################
# Test 3 -> Separated by styles and beat type
#                           and time_signature
####################################################
from .subsetters import GrooveMidiSubsetter

styles = ["afrobeat", "afrocuban", "blues", "country", "dance",
          "funk", "gospel", "highlife", "hiphop", "jazz",
          "latin", "middleeastern", "neworleans", "pop",
          "punk", "reggae", "rock", "soul"]


list_of_filter_dicts_for_subsets = [
    {"style_primary": [style], "beat_type": ["beat"], "time_signature": ["4-4"]} for style in styles]

gmd_by_styl_and_beat = GrooveMidiSubsetter(
            pickle_source_path="datasets_extracted_locally/GrooveMidi/hvo_0.3.0/Processed_On_13_05_2021_at_12_56_hrs",
            subset="GrooveMIDI_processed_train",
            hvo_pickle_filename="hvo_sequence_data.obj",
            list_of_filter_dicts_for_subsets=list_of_filter_dicts_for_subsets,
    )

tags_by_style_and_beat, subsets_by_style_and_beat = gmd_by_styl_and_beat.create_subsets()
for ix, (tag, subset) in enumerate(zip(tags_by_style_and_beat, subsets_by_style_and_beat)):
    print("Subset {} --> Tag {} --> n_samples {}".format(ix, tag, len(subset)))


####################################################
# Test 4 -> Multiple feature values for a feature
####################################################
from .subsetters import GrooveMidiSubsetter

styles = ["afrobeat", "afrocuban", "blues", "country", "dance",
          "funk", "gospel", "highlife", "hiphop", "jazz",
          "latin", "middleeastern", "neworleans", "pop",
          "punk", "reggae", "rock", "soul"]


list_of_filter_dicts_for_subsets = [
    {"style_primary": [style, "rock"], "beat_type": ["beat"], "time_signature": ["4-4"]} for style in styles]

gmd_by_styl_and_beat = GrooveMidiSubsetter(
            pickle_source_path="datasets_extracted_locally/GrooveMidi/hvo_0.3.0/Processed_On_13_05_2021_at_12_56_hrs",
            subset="GrooveMIDI_processed_train",
            hvo_pickle_filename="hvo_sequence_data.obj",
            list_of_filter_dicts_for_subsets=list_of_filter_dicts_for_subsets,
    )

tags_by_style_and_beat, subsets_by_style_and_beat = gmd_by_styl_and_beat.create_subsets()
for ix, (tag, subset) in enumerate(zip(tags_by_style_and_beat, subsets_by_style_and_beat)):
    print("Subset {} --> Tag {} --> n_samples {}".format(ix, tag, len(subset)))


###############################################

# FIXME these filters give error
from .subsetters import GrooveMidiSubsetter

gmd_1 = GrooveMidiSubsetter(
            pickle_source_path="datasets_extracted_locally/GrooveMidi/hvo_0.3.0/Processed_On_13_05_2021_at_12_56_hrs",
            subset="GrooveMIDI_processed_test",
            hvo_pickle_filename="hvo_sequence_data.obj",
            list_of_filter_dicts_for_subsets=[{"new_key": [1], "new_key2": [1, 2], "beat_type": ["beat"]}]
    )
tags1, subsets1 = gmd_1.create_subsets()
for ix, (tag, subset) in enumerate(zip(tags1, subsets1)):
    print("Subset {} --> Tag {} --> n_samples {}".format(ix, tag, len(subsets1)))

# FIXME these filters give error
gmd_1 = GrooveMidiSubsetter(
            pickle_source_path="datasets_extracted_locally/GrooveMidi/hvo_0.3.0/Processed_On_13_05_2021_at_12_56_hrs",
            subset="GrooveMIDI_processed_test",
            hvo_pickle_filename="hvo_sequence_data.obj",
            list_of_filter_dicts_for_subsets=[{"new_key": [None], "new_key2": None, "new_key2": [1]}]
    )
tags1, subsets1 = gmd_1.create_subsets()

