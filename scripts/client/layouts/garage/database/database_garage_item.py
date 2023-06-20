class DatabaseGarageItem:
    def __init__(self, garage_item):
        self.garage_item = garage_item
        self.item_id = 0
        self.upgrading_property_id = None
        self.upgrade_done_time = None
        self.upgradable_property_data_levels = {}
        self.property_levels_id = None
        self.count = 0
        self.temporary_item_expiration_time = None

    def get_property_value(self, property_name):
        property = self.garage_item.get_property(property_name)

        if property == None: return

        upgradable_property_data = self.garage_item.get_upgradable_property_data_by_id(property.upgradable_property_id)

        if upgradable_property_data == None:
            return property.initial_value

        property_level = self.upgradable_property_data_levels[upgradable_property_data.property_id]
        return property.initial_value + (property.final_value - property.initial_value) * (property_level / upgradable_property_data.max_level) # apply micro upgrades to property level

    def get_all_propertys_with_value(self):
        return {property_name:self.get_property_value(property_name) for property_name in self.garage_item.get_all_property_names()}
