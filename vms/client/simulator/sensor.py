import math
import random
from abc import ABC, abstractmethod

BIRTH_DAY = 11  # 11.11 - день и месяц рождения


class Sensor(ABC):
    def __init__(self, name: str, formula: str = "random"):
        self.name = name
        self.formula = formula
        self._step = 0

    @abstractmethod
    def _base(self) -> float:
        pass

    @abstractmethod
    def _amplitude(self) -> float:
        pass

    def read(self) -> float:
        self._step += 1
        base = self._base()
        amp = self._amplitude()

        if self.formula == "sin":
            noise = math.sin(self._step * BIRTH_DAY / 100.0) * amp
        elif self.formula == "linear":
            noise = ((self._step % BIRTH_DAY) / BIRTH_DAY * 2 - 1) * amp
        else:
            noise = random.uniform(-amp, amp)

        return round(base + noise, 2)


class TemperatureSensor(Sensor):
    """Датчик температуры, диапазон 18-32 C"""
    def _base(self): return 25.0
    def _amplitude(self): return 5.0


class PressureSensor(Sensor):
    """Датчик давления, диапазон 0.9-1.1 бар"""
    def _base(self): return 1.013
    def _amplitude(self): return 0.05


class CurrentSensor(Sensor):
    """Датчик тока, диапазон 0.5-4.5 А"""
    def _base(self): return 2.5
    def _amplitude(self): return 1.1  # 11/10 - используем день рождения


class HumiditySensor(Sensor):
    """Датчик влажности, диапазон 40-80%"""
    def _base(self): return 60.0
    def _amplitude(self): return 11.0  # amplitude = BIRTH_DAY


SENSOR_TYPES = {
    "temperature": TemperatureSensor,
    "pressure": PressureSensor,
    "current": CurrentSensor,
    "humidity": HumiditySensor,
}
