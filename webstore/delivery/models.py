from abc import ABC, abstractmethod

from django.db import models




class CourierManager(ABC):
    
    @abstractmethod
    def delivery_price(self,order):
        pass


class WeightedPricing(ABC):
    @abstractmethod
    def delivery_price(self, order):
        pass

class CubicPricing(ABC):
    @abstractmethod
    def delivery_price(self, order):
        pass

class FirstCourierManager(CourierManager):
    


class SecondCourierManager(CourierManager):
    pass


class FirstCourierWeighterPricing(WeightedPricing):
    pass

class FirstCourierCubicPricing(CubicPricing):
    pass


class SecondCourierWeighterPricing(WeightedPricing):
    pass

class SecondCourierCubicPricing(CubicPricing):
    pass