import pickle
import os
import numpy as np
from copy import deepcopy
import sys

from hvo_sequence import HVO_Sequence


# todo append subset to beginning of the tags
# todo for None cases name the tag as full_set
# implement sort by samples


class GrooveMidiSubsetterAndSampler(object):
    def __init__(
        self,
        pickle_source_path="datasets_extracted_locally/GrooveMidi/hvo_0.3.0/Processed_On_13_05_2021_at_12_56_hrs",
        subset="GrooveMIDI_processed_test",
        hvo_pickle_filename="hvo_sequence_data.obj",
        list_of_filter_dicts_for_subsets=None,
        number_of_samples=1024,
        max_hvo_shape=(32, 27),
        at_least_one_hit_in_voices=None  # should be a list of voices where at least 1 hit == required
        # example:  [0, 1, 2]
    ):
        tags_all, subsets_all = GrooveMidiSubsetter(
            pickle_source_path=pickle_source_path,
            subset=subset,
            hvo_pickle_filename=hvo_pickle_filename,
            list_of_filter_dicts_for_subsets=list_of_filter_dicts_for_subsets,
            max_len=max_hvo_shape[0],
            at_least_one_hit_in_voices=at_least_one_hit_in_voices,
        ).create_subsets()

        set_sampler = Set_Sampler(
            tags_all,
            subsets_all,
            number_of_samples=number_of_samples,
            max_hvo_shape=max_hvo_shape,
        )

        self.sampled_tags, self.sampled_subsets = set_sampler.get_sampled_tags_subsets()

        (
            self.hvos_array_tags,
            self.hvos_array,
            self.hvo_seq_templates,
        ) = set_sampler.get_hvos_array()

    def get_subsets(self):
        return self.sampled_tags, self.sampled_subsets

    def get_hvos_array(self):
        return self.hvos_array_tags, self.hvos_array, self.hvo_seq_templates


class GrooveMidiSubsetter(object):
    def __init__(
        self,
        pickle_source_path="datasets_extracted_locally/GrooveMidi/hvo_0.3.0/Processed_On_13_05_2021_at_12_56_hrs",
        subset="GrooveMIDI_processed_test",
        hvo_pickle_filename="hvo_sequence_data.obj",
        list_of_filter_dicts_for_subsets=None,
        max_len=None,
        at_least_one_hit_in_voices=None,
    ):
        self.list_of_filter_dicts_for_subsets = list_of_filter_dicts_for_subsets
        # load preprocessed hvo_sequences from pickle file
        self.pickled_hvo_set_filename = open(
            os.path.join(pickle_source_path, subset, hvo_pickle_filename), "rb"
        )
        self.full_hvo_set_pre_filters = pickle.load(self.pickled_hvo_set_filename)
        self.at_least_one_hit_in_voices = at_least_one_hit_in_voices

        if max_len != None:
            for hvo_seq in self.full_hvo_set_pre_filters:
                # pad with zeros or trim to match max_len
                pad_count = max(max_len - hvo_seq.hvo.shape[0], 0)
                hvo_seq.hvo = np.pad(hvo_seq.hvo, ((0, pad_count), (0, 0)), "constant")
                hvo_seq.hvo = hvo_seq.hvo[
                    :max_len, :
                ]  # In case, sequence exceeds max_len

        self.subset_tags = None
        self.hvo_subsets = None

    def create_subsets(self, force_create=False):
        """
        Creates a set of subsets from a hvo_sequence dataset using a set of filters specified in constructor

        :param      force_create: If True, this method re-creates subsets even if it has already done so
        :return:    subset_tags, hvo_subsets
        """

        # Don't recreate if already haven't done so ( and if force_create == false)
        if self.subset_tags != None and self.hvo_subsets != None:
            if len(self.subset_tags) == len(self.hvo_subsets) and force_create == False:
                return self.subset_tags, self.hvo_subsets

        # if no filters, return a SINGLE dataset containing all hvo_seq sequences
        if (
            self.list_of_filter_dicts_for_subsets == None
            or self.list_of_filter_dicts_for_subsets == [None]
        ):
            hvo_subsets = [self.full_hvo_set_pre_filters]
            subset_tags = ["Complete_Groove_MIDI_Set"]

        else:
            hvo_subsets = []
            subset_tags = []
            for i in range(len(self.list_of_filter_dicts_for_subsets)):
                hvo_subsets.append([])
                subset_tags.append([""])

            for subset_ix, filter_dict_for_subset in enumerate(
                self.list_of_filter_dicts_for_subsets
            ):
                # if current filter == None or a dict with None values
                # add all the dataset in its entirety to current subset
                if filter_dict_for_subset == None:
                    hvo_subsets[subset_ix] = self.full_hvo_set_pre_filters
                elif isinstance(filter_dict_for_subset, dict) and all(
                    value == None for value in filter_dict_for_subset.values()
                ):
                    hvo_subsets[subset_ix] = self.full_hvo_set_pre_filters

                else:
                    # Check which samples meet all filter specifications and add them to the current subset
                    subset_tags[subset_ix] = "_AND_".join(
                        str(x) for x in filter_dict_for_subset.values()
                    )
                    for hvo_sample in self.full_hvo_set_pre_filters:
                        if self.does_pass_filter(hvo_sample, filter_dict_for_subset):
                            if self.at_least_one_hit_in_voices != None:
                                # Check that there == at least one hit in the required subset of voices
                                if (
                                    1
                                    in hvo_sample.hvo[
                                        :, self.at_least_one_hit_in_voices
                                    ]
                                ):
                                    hvo_subsets[subset_ix].append(hvo_sample)
                            else:
                                hvo_subsets[subset_ix].append(hvo_sample)

        return subset_tags, hvo_subsets

    def does_pass_filter(self, hvo_sample, filter_dict):
        # Ensure correct formatting of the filter values (specifications)
        for (filter_dict_key, filter_dict_vals) in filter_dict.items():
            assert isinstance(filter_dict_vals, type(None)) or isinstance(
                filter_dict_vals, list
            ), (
                "The filter values for key ({}) in subset {} should be either None "
                "or specified in a list"
            )

        # Start checking each hvo_sample feature against the specified values in filter
        for (filter_key, filter_values) in filter_dict.items():
            if filter_key == "time_signature":
                sample_passes_filter = []
                for time_signature in filter_dict[filter_key]:
                    numerator = int(time_signature.split("-")[0])
                    denominator = int(time_signature.split("-")[1])
                    if (
                        hvo_sample.time_signatures[0].numerator == numerator
                        and hvo_sample.time_signatures[0].denominator == denominator
                    ):
                        sample_passes_filter.append(True)
                    else:
                        sample_passes_filter.append(False)
                if not any(sample_passes_filter):  # no need to check
                    return False

            elif filter_key == "bpm":
                sample_passes_filter = []
                for bpm_lower_b, bpm_upper_b in filter_dict[filter_key]:
                    if bpm_lower_b < hvo_sample.tempos[0].qpm < bpm_upper_b:
                        sample_passes_filter.append(True)
                    else:
                        sample_passes_filter.append(False)
                if not any(sample_passes_filter):
                    return False

            elif filter_key == "number_of_instruments":
                sample_passes_filter = []
                for n_instruments_lower_bound, n_instruments_upper_bound in filter_dict[
                    filter_key
                ]:
                    if (
                        n_instruments_lower_bound
                        < hvo_sample.get_number_of_active_voices()
                        < n_instruments_upper_bound
                    ):
                        sample_passes_filter.append(True)
                    else:
                        sample_passes_filter.append(False)
                if not any(sample_passes_filter):
                    return False

            else:

                feat_value_in_hvo = []

                if filter_key == "drummer":
                    feat_value_in_hvo = hvo_sample.metadata.drummer
                if filter_key == "session":
                    feat_value_in_hvo = hvo_sample.metadata.session
                if filter_key == "loop_id":
                    feat_value_in_hvo = hvo_sample.metadata.loop_id
                if filter_key == "master_id":
                    feat_value_in_hvo = hvo_sample.metadata.master_id
                if filter_key == "style_primary":
                    feat_value_in_hvo = hvo_sample.metadata.style_primary
                if filter_key == "style_secondary":
                    feat_value_in_hvo = hvo_sample.metadata.style_secondary
                if filter_key == "beat_type":
                    feat_value_in_hvo = hvo_sample.metadata.beat_type
                if filter_key == "full_midi_filename":
                    feat_value_in_hvo = hvo_sample.metadata.full_midi_filename
                if filter_key == "full_audio_filename":
                    feat_value_in_hvo = hvo_sample.metadata.full_audio_filename

                # Check whether at least one of the current filter_key values == met
                if not isinstance(filter_values, list):
                    filter_values = [[filter_values]]
                else:
                    if not isinstance(filter_values[0], list):
                        filter_values = [filter_values]

                sample_passes_filter = [
                    True if feat_value_in_hvo in filter_val_set else False
                    for filter_val_set in filter_values
                ]

                if not any(sample_passes_filter):
                    return False

        return True


class Set_Sampler(object):
    def __init__(self, tags_, hvo_subsets_, number_of_samples, max_hvo_shape=(32, 27)):
        tags = []
        hvo_subsets = []
        self.subsets_dict = {}

        total_samples = sum([len(x) for x in hvo_subsets_])
        number_of_samples = (
            number_of_samples if number_of_samples != None else total_samples
        )

        # delete empty sets
        for tag, hvo_subset in zip(tags_, hvo_subsets_):
            if hvo_subset:
                tags.append(tag)
                hvo_subsets.append(hvo_subset)

        # remove empty subsets
        self.hvos_array_tags = []
        self.hvos_array = np.zeros(
            (number_of_samples, max_hvo_shape[0], max_hvo_shape[1])
        )
        self.hvo_seqs = []
        self.empty_hvo_seqs = []

        sample_count = 0
        while sample_count < number_of_samples:
            # Sample a subset
            subset_ix = int(np.random.choice(range(len(tags)), 1))
            tag = tags[subset_ix]

            # Sample an example if subset != fully emptied out
            if hvo_subsets[subset_ix]:
                sample_ix = int(np.random.choice(range(len(hvo_subsets[subset_ix])), 1))
                hvo_seq = hvo_subsets[subset_ix][sample_ix]
                if tag not in self.subsets_dict.keys():
                    self.subsets_dict.update({tag: [deepcopy(hvo_seq)]})
                else:
                    self.subsets_dict[tag].append(hvo_seq)

                hvo = hvo_seq.get("hvo")
                max_time = min(max_hvo_shape[0], hvo.shape[0])

                self.hvos_array[sample_count, :max_time, :] = hvo
                self.hvos_array_tags.append(tag)
                self.hvo_seqs.append(hvo_seq)
                self.empty_hvo_seqs.append(hvo_seq.copy_empty())
                del hvo_subsets[subset_ix][
                    sample_ix
                ]  # remove the sample from future selections

                sample_count += 1

        del tags
        del hvo_subsets

    def get_hvos_array(self):
        return self.hvos_array_tags, self.hvos_array, self.empty_hvo_seqs

    def get_sampled_tags_subsets(self):
        return list(self.subsets_dict.keys()), list(self.subsets_dict.values())


def convert_hvos_array_to_subsets(
    hvos_array_tags, hvos_array_predicted, hvo_seqs_templates_
):
    hvo_seqs_templates = deepcopy(hvo_seqs_templates_)

    tags = list(set(hvos_array_tags))
    temp_dict = {tag: [] for tag in tags}

    for i in range(hvos_array_predicted.shape[0]):
        hvo_seqs_templates[i].hvo = hvos_array_predicted[i, :, :]
        temp_dict[hvos_array_tags[i]].append(hvo_seqs_templates[i])

    tags = list(temp_dict.keys())
    subsets = list(temp_dict.values())

    return tags, subsets
