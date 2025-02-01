# -*- coding: utf-8 -*-

from typing import Dict, Generic, Optional, Sequence, Type, TypeVar, Union

_T = TypeVar("_T")


class Constraint(Generic[_T]):
    DEFAULT: _T

    def __init__(self, value: Optional[_T] = None):
        self.value = value if value is not None else self.DEFAULT


class ConstraintStep(Constraint[Union[int, float]]):
    DEFAULT = 1


class ConstraintStepFast(Constraint[Union[int, float]]):
    DEFAULT = 100


class ConstraintFloatFormat(Constraint[str]):
    DEFAULT = "%.3f"


class ConstraintFlags(Constraint[int]):
    DEFAULT = 0


class Constraints(Dict[Type[Constraint], Constraint]):
    def __init__(self, constraints: Optional[Sequence[Constraint]] = None):
        super().__init__({type(c): c for c in list(constraints if constraints else ())})

    def get_constraint_value(self, cls: Type[Constraint]):
        if constraint := self.get(cls):
            assert isinstance(constraint, cls)
            return constraint.value
        else:
            return cls.DEFAULT

    @property
    def step(self) -> Union[int, float]:
        return self.get_constraint_value(ConstraintStep)

    @property
    def step_fast(self) -> Union[int, float]:
        return self.get_constraint_value(ConstraintStepFast)

    @property
    def float_format(self) -> str:
        return self.get_constraint_value(ConstraintFloatFormat)

    @property
    def flags(self) -> int:
        return self.get_constraint_value(ConstraintFlags)
