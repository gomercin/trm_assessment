class AssetInformation:
    """
    DTO to store asset information
    """
    def __init__(self, asset_name, spot_value, historical_data):
        self.asset_name = asset_name
        self.spot_value = spot_value
        self.historical_data = historical_data
