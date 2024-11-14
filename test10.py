# class VehicleFactory:
#     @classmethod
#     def create_vehicle(cls, vehicle_type, model):
#         if vehicle_type == "car":
#             return Car(model)
#         elif vehicle_type == "truck":
#             return Truck(model)
#         else:
#             raise ValueError("Unknown vehicle type")
#
#         # 使用类方法
#
#
# car = VehicleFactory.create_vehicle("car", "Honda")
# truck = VehicleFactory.create_vehicle("truck", "Chevy")
#
# print(car.drive())  # 输出: Driving the Honda
# print(truck.drive())  # 输出: Driving the Chevy Truck


class Car:
    def __init__(self, model):
        self.model = model

    def drive(self):
        return f"Driving the {self.model}"


class Truck:
    def __init__(self, model):
        self.model = model

    def drive(self):
        return f"Driving the {self.model} Truck"


def vehicle_factory(vehicle_type, model):
    if vehicle_type == "car":
        return Car(model)
    elif vehicle_type == "truck":
        return Truck(model)
    else:
        raise ValueError("Unknown vehicle type")

    # 使用工厂函数


car = vehicle_factory("car", "Toyota")
truck = vehicle_factory("truck", "Ford")

print(car.drive())  # 输出: Driving the Toyota
print(truck.drive())  # 输出: Driving the Ford Truck