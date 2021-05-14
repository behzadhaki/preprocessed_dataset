Use this class to create multiple subsets with specific requirements for each subset

### Procedure

### <u> A. </u>  Create a list of filter dictionaries for creating the subsets

##### Filters are lists of dictionaries. Each element in the list (which is a dict) refers to a set of specifications 

##### THE VALUES IN THE DICTIONARY SHOULD ALSO BE LISTS (SEE FORMATTING BELOW). THIS ENSURES THAT MULTIPLE SPECIFICATIONS PER FEATURE IS ALLOWED IN THE SUBSETTING PROCESS




GROOVEMIDI_FILTER_TEMPLATE = [{

    "drummer": ,                                    # ["drummer1", ..., and/or "session9"]
    "session": ,                                    # ["session1", "session2", and/or "session3"]
    "loop_id": ,
    "master_id": ,
    "style_primary": ,                              #   ["afrobeat", "afrocuban", "blues", "country", "dance", "funk",                                                          "gospel", "highlife", "hiphop", "jazz",
                                                         "latin", "middleeastern", "neworleans", "pop", 
                                                         "punk", "reggae", "rock", "soul"]
    "style_secondary": ,
    "bpm": None,                                    # [(range_0_lower_bound, range_0_upper_bound), ...,
                                                    #   (range_n_lower_bound, range_n_upper_bound)]
    "beat_type": ,                                  # ["beat" or "fill"]
    "time_signature": ,                             # ["4-4", "3-4", "6-8"]
    "full_midi_filename": ,                         # list_of full_midi_filenames
    "full_audio_filename": ,                        # list_of full_audio_filename
    "number_of_instruments": ,                      # [(n_instruments_lower_bound, n_instruments_upper_bound), ...,
                                                    #  (n_instruments_lower_bound, n_instruments_upper_bound)]
}]  






##### <u> <i> Example 1 </i> </u>

Create two subsets: first one with rock and funk samples only and the second one with reggae only

Filter = [{"style_primary": ["rock", "funk"]}, {"style_primary": ["reggae"]}, ]

##### <u> <i> Example 2 </i> </u>

Create two subsets like above but only get the beats in the first one and fills in the second

Filter = [{"style_primary": ["rock", "funk"], "beat_type": ["beat"]}, {"style_primary": ["reggae"], "beat_type": ["fill"]}, ]






### <u> B. </u>  Create an instance of the GrooveMidiSubsetter and call the create_subsets() method

