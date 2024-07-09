from typing import Dict, List


def concat_dicts(list_of_dicts: List[Dict]) -> Dict:
    """
    Concatenate a list of dictionaries into a single dictionary.

    This function takes a list of dictionaries and combines them into a single dictionary.
    For each unique key across all input dictionaries, it creates a list of values
    from all dictionaries that contain that key.

    Args:
        list_of_dicts (List[Dict]): A list of dictionaries to be concatenated.
            Each dictionary in the list can have any number of key-value pairs.

    Returns:
        Dict[str, List]: A dictionary where each key is a unique key from the input dictionaries,
            and each value is a list of values for that key from all input dictionaries
            that contained the key.

    Example:
        >>> d1 = {'a': 1, 'b': 2}
        >>> d2 = {'b': 3, 'c': 4}
        >>> d3 = {'a': 5, 'c': 6}
        >>> concat_dicts([d1, d2, d3])
        {'a': [1, 5], 'b': [2, 3], 'c': [4, 6]}

    Note:
        - If a key is not present in a dictionary, it will not contribute to the list for that key.
        - The order of values in the resulting lists corresponds to the order of dictionaries in the input list.
        - This function does not modify the input dictionaries.
    """
    return {key: [d[key] for d in list_of_dicts if key in d] for key in set().union(*list_of_dicts)}
