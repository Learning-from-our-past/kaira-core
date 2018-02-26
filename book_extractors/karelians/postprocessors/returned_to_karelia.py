
def check_if_person_returned_karelia_in_between_wars(location_list, metadata_collector=None):
    """
    Reads through the migration history and tries to resolve if the person returned to karelia in between
    Winter War and Continuation War. Returns true if:
    1) Person lived in karelia before first war
    2) Person moved in karelia in between wars

    Otherwise returns false.

    Returns None if there was not enough year data to resolve returning information. For example in if previous conditions were not
    met AND there is a karelian record with no year information.

    :param location_list:
    :param metadata_collector:
    :return boolean:
    """
    lived_in_karelia_before_wars = False
    moved_to_karelia_in_between_wars = False
    year_data_not_available_for_karelian_place = False
    continuation_war_start_year = 41
    continuation_war_end_year = 44

    for living_record in location_list:
        if living_record['region'] == 'karelia':

            if not year_data_not_available_for_karelian_place:
                year_data_not_available_for_karelian_place = living_record['movedIn'] is None and living_record['movedOut'] is None

            if living_record['movedOut'] is not None and living_record['movedOut'] < continuation_war_start_year:
                lived_in_karelia_before_wars = True

            if living_record['movedIn'] is not None and living_record['movedIn'] < continuation_war_start_year:
                lived_in_karelia_before_wars = True

            if living_record['movedIn'] is not None and continuation_war_start_year <= living_record['movedIn'] <= continuation_war_end_year:
                moved_to_karelia_in_between_wars = True

            if living_record['movedOut'] is not None and continuation_war_start_year <= living_record['movedOut'] <= continuation_war_end_year:
                moved_to_karelia_in_between_wars = True

    if not moved_to_karelia_in_between_wars and year_data_not_available_for_karelian_place:
        """ 
        Sometimes it is not possible to figure out from provided year data if the person returned to karelia in between wars or not.
        For example if there is a living record in karelia without both movedIn and movedOut data and person is said to not returned
        to karelia, then we can't know if they lived in karelia in between the wars or if the record belongs to some other time range.
        In this case return None.
        """
        return None

    return lived_in_karelia_before_wars and moved_to_karelia_in_between_wars
