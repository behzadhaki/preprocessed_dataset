import pickle
import os
import pandas as pd
import warnings

import sys
sys.path.insert(1, "../../hvo_sequence")
sys.path.insert(1, "../hvo_sequence")

from hvo_sequence.hvo_seq import HVO_Sequence                           # required for loading pickles
import note_seq
from CustomLoaders.filters import GROOVEMIDI_FILTER_TEMPLATE

import math

class BasePickledGrooveMidiLoader(object):
    def __init__(
            self,
            pickle_source_path="datasets_extracted_locally/GrooveMidi/hvo_0.3.0/Processed_On_13_05_2021_at_12_56_hrs",
            subset="GrooveMIDI_processed_test",
            hvo_pickle_filename="hvo_sequence_data.obj",
            list_of_filter_dicts_for_subsets=None,
    ):
        self.list_of_filter_dicts_for_subsets = list_of_filter_dicts_for_subsets
        # load preprocessed hvo_sequences from pickle file
        self.pickled_hvo_set_filename = open(os.path.join(pickle_source_path, subset, hvo_pickle_filename), 'rb')
        self.full_hvo_set_pre_filters = pickle.load(self.pickled_hvo_set_filename)

    def create_subsets(self):
        # if no filters, return a SINGLE dataset containing all hvo_seq sequences
        if self.list_of_filter_dicts_for_subsets is None or self.list_of_filter_dicts_for_subsets == [None]:
            hvo_subsets = [self.full_hvo_set_pre_filters]
            subset_tags = ['Complete_Groove_MIDI_Set']
            print("CASE 1")

        else:
            print("CASE 2")
            hvo_subsets = []
            subset_tags = []
            for i in range(len(self.list_of_filter_dicts_for_subsets)):
                hvo_subsets.append([])
                subset_tags.append([''])

            for subset_ix, filter_dict_for_subset in enumerate(self.list_of_filter_dicts_for_subsets):
                # if current filter is None or a dict with None values
                # add all the dataset in its entirety to current subset
                if filter_dict_for_subset is None:
                    hvo_subsets[subset_ix] = self.full_hvo_set_pre_filters
                elif isinstance(filter_dict_for_subset, dict) and \
                        all(value is None for value in filter_dict_for_subset.values()):
                    hvo_subsets[subset_ix] = self.full_hvo_set_pre_filters

                else:
                    # Check which samples meet all filter specifications and add them to the current subset
                    subset_tags[subset_ix] = '_AND_'.join(str(x) for x in filter_dict_for_subset.values())
                    for hvo_sample in self.full_hvo_set_pre_filters:
                        if self.does_pass_filter(hvo_sample, filter_dict_for_subset):
                            hvo_subsets[subset_ix].append(hvo_sample)

        return subset_tags, hvo_subsets

    def does_pass_filter(self, hvo_sample, filter_dict):
            # Ensure correct formatting of the filter values (specifications)
            for (filter_dict_key, filter_dict_vals) in filter_dict.items():
                assert isinstance(filter_dict_vals, type(None)) or isinstance(filter_dict_vals, list), \
                    "The filter values for key ({}) in subset {} should be either None " \
                    "or specified in a list"

            # Start checking each hvo_sample feature against the specified values in filter
            for (filter_key, filter_values) in filter_dict.items():
                if filter_key is "time_signature":
                    sample_passes_filter = []
                    for time_signature in filter_dict[filter_key]:
                        numerator = int(time_signature.split("-")[0])
                        denominator = int(time_signature.split("-")[1])
                        if hvo_sample.time_signatures[0].numerator == numerator and  \
                                hvo_sample.time_signatures[0].denominator == denominator:
                            sample_passes_filter.append(True)
                        else:
                            sample_passes_filter.append(False)
                    if not any(sample_passes_filter):   # no need to check
                        return False

                elif filter_key is "bpm":
                    sample_passes_filter = []
                    for bpm_lower_b, bpm_upper_b in filter_dict[filter_key]:
                        if bpm_lower_b < hvo_sample.tempos[0].qpm < bpm_upper_b:
                            sample_passes_filter.append(True)
                        else:
                            sample_passes_filter.append(False)
                    if not any(sample_passes_filter):
                        return False
                else:

                    feat_value_in_hvo = []

                    if filter_key is "drummer":
                        feat_value_in_hvo = hvo_sample.metadata.drummer
                    if filter_key is "session":
                        feat_value_in_hvo = hvo_sample.metadata.session
                    if filter_key is "loop_id":
                        feat_value_in_hvo = hvo_sample.metadata.loop_id
                    if filter_key is "master_id":
                        feat_value_in_hvo = hvo_sample.metadata.master_id
                    if filter_key is "style_primary":
                        feat_value_in_hvo = hvo_sample.metadata.style_primary
                    if filter_key is "style_secondary":
                        feat_value_in_hvo = hvo_sample.metadata.style_secondary
                    if filter_key is "beat_type":
                        feat_value_in_hvo = hvo_sample.metadata.beat_type
                    if filter_key is "full_midi_filename":
                        feat_value_in_hvo = hvo_sample.metadata.full_midi_filename
                    if filter_key is "full_audio_filename":
                        feat_value_in_hvo = hvo_sample.metadata.full_audio_filename


                    # Check whether at least one of the current filter_key values is met
                    if not isinstance(filter_values, list):
                        filter_values = [[filter_values]]
                    else:
                        if not isinstance(filter_values[0], list):
                            filter_values = [filter_values]

                    sample_passes_filter = [True if feat_value_in_hvo in filter_val_set else False
                                            for filter_val_set in filter_values]

                    if not any(sample_passes_filter):
                        return False

            return True
