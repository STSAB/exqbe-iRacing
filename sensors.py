ADDRESS_MAP = {
    48: 'WaterTemp'
}


def address_to_name(address):
    """
     Hard coded translation from an Exhub address to an iRacing sensor key.
    """
    return ADDRESS_MAP.get(address)
