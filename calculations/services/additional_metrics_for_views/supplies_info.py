from calculations.models import Supplies_info

def addition_metrics_for_supplies_info():
    sup = Supplies_info.objects.all()
    warehouses = []

    for item in sup:
        warehouses.append(item.warehouse)

    def unique_generator(list_):
        seen = []
        for item in list_:
            if item not in seen:
                seen.append(item)
        return seen

    def non_unique_element_count(list_):
        count_non_unique = 1
        for i in range(len(list_)):
            if list_[i] == list_[i + 1]:
                count_non_unique += 1
            else:
                return count_non_unique

    return unique_generator(warehouses), non_unique_element_count(warehouses)