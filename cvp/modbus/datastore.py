# -*- coding: utf-8 -*-

import threading
from typing import List

from cvp.modbus.exceptions import ModbusInvalidAddressError


class ModbusDataStore:
    """Thread-safe Modbus data store for coils, discrete inputs, and registers."""

    def __init__(
        self,
        coils_size: int = 65536,
        discrete_inputs_size: int = 65536,
        holding_registers_size: int = 65536,
        input_registers_size: int = 65536,
    ):
        """Initialize the data store.

        Args:
            coils_size: Size of coils array (default: 65536).
            discrete_inputs_size: Size of discrete inputs array (default: 65536).
            holding_registers_size: Size of holding registers array (default: 65536).
            input_registers_size: Size of input registers array (default: 65536).
        """
        self._coils_size = coils_size
        self._discrete_inputs_size = discrete_inputs_size
        self._holding_registers_size = holding_registers_size
        self._input_registers_size = input_registers_size

        self._coils: List[bool] = [False] * coils_size
        self._discrete_inputs: List[bool] = [False] * discrete_inputs_size
        self._holding_registers: List[int] = [0] * holding_registers_size
        self._input_registers: List[int] = [0] * input_registers_size

        self._lock = threading.RLock()

    def _validate_address_range(
        self,
        address: int,
        count: int,
        max_size: int,
        name: str,
    ) -> None:
        """Validate address range.

        Args:
            address: Starting address.
            count: Number of items.
            max_size: Maximum size of the store.
            name: Name of the store for error messages.

        Raises:
            ModbusInvalidAddressError: If address range is invalid.
        """
        if address < 0:
            raise ModbusInvalidAddressError(f"Invalid {name} address: {address}")
        if count <= 0:
            raise ModbusInvalidAddressError(f"Invalid {name} count: {count}")
        if address + count > max_size:
            raise ModbusInvalidAddressError(
                f"{name} address range {address}:{address + count} "
                f"exceeds maximum size {max_size}"
            )

    def get_coils(self, address: int, count: int) -> List[bool]:
        """Read coils.

        Args:
            address: Starting address.
            count: Number of coils to read.

        Returns:
            List of coil values.

        Raises:
            ModbusInvalidAddressError: If address range is invalid.
        """
        self._validate_address_range(address, count, self._coils_size, "coils")
        with self._lock:
            return self._coils[address : address + count].copy()

    def set_coils(self, address: int, values: List[bool]) -> None:
        """Write coils.

        Args:
            address: Starting address.
            values: List of coil values to write.

        Raises:
            ModbusInvalidAddressError: If address range is invalid.
        """
        count = len(values)
        self._validate_address_range(address, count, self._coils_size, "coils")
        with self._lock:
            for i, value in enumerate(values):
                self._coils[address + i] = value

    def set_coil(self, address: int, value: bool) -> None:
        """Write a single coil.

        Args:
            address: Coil address.
            value: Coil value.

        Raises:
            ModbusInvalidAddressError: If address is invalid.
        """
        self._validate_address_range(address, 1, self._coils_size, "coil")
        with self._lock:
            self._coils[address] = value

    def get_discrete_inputs(self, address: int, count: int) -> List[bool]:
        """Read discrete inputs.

        Args:
            address: Starting address.
            count: Number of discrete inputs to read.

        Returns:
            List of discrete input values.

        Raises:
            ModbusInvalidAddressError: If address range is invalid.
        """
        self._validate_address_range(
            address, count, self._discrete_inputs_size, "discrete inputs"
        )
        with self._lock:
            return self._discrete_inputs[address : address + count].copy()

    def set_discrete_inputs(self, address: int, values: List[bool]) -> None:
        """Write discrete inputs (typically set by the server/simulation).

        Args:
            address: Starting address.
            values: List of discrete input values to write.

        Raises:
            ModbusInvalidAddressError: If address range is invalid.
        """
        count = len(values)
        self._validate_address_range(
            address, count, self._discrete_inputs_size, "discrete inputs"
        )
        with self._lock:
            for i, value in enumerate(values):
                self._discrete_inputs[address + i] = value

    def get_holding_registers(self, address: int, count: int) -> List[int]:
        """Read holding registers.

        Args:
            address: Starting address.
            count: Number of registers to read.

        Returns:
            List of register values.

        Raises:
            ModbusInvalidAddressError: If address range is invalid.
        """
        self._validate_address_range(
            address, count, self._holding_registers_size, "holding registers"
        )
        with self._lock:
            return self._holding_registers[address : address + count].copy()

    def set_holding_registers(self, address: int, values: List[int]) -> None:
        """Write holding registers.

        Args:
            address: Starting address.
            values: List of register values to write.

        Raises:
            ModbusInvalidAddressError: If address range is invalid.
        """
        count = len(values)
        self._validate_address_range(
            address, count, self._holding_registers_size, "holding registers"
        )
        with self._lock:
            for i, value in enumerate(values):
                self._holding_registers[address + i] = value & 0xFFFF

    def set_holding_register(self, address: int, value: int) -> None:
        """Write a single holding register.

        Args:
            address: Register address.
            value: Register value.

        Raises:
            ModbusInvalidAddressError: If address is invalid.
        """
        self._validate_address_range(
            address, 1, self._holding_registers_size, "holding register"
        )
        with self._lock:
            self._holding_registers[address] = value & 0xFFFF

    def get_input_registers(self, address: int, count: int) -> List[int]:
        """Read input registers.

        Args:
            address: Starting address.
            count: Number of registers to read.

        Returns:
            List of register values.

        Raises:
            ModbusInvalidAddressError: If address range is invalid.
        """
        self._validate_address_range(
            address, count, self._input_registers_size, "input registers"
        )
        with self._lock:
            return self._input_registers[address : address + count].copy()

    def set_input_registers(self, address: int, values: List[int]) -> None:
        """Write input registers (typically set by the server/simulation).

        Args:
            address: Starting address.
            values: List of register values to write.

        Raises:
            ModbusInvalidAddressError: If address range is invalid.
        """
        count = len(values)
        self._validate_address_range(
            address, count, self._input_registers_size, "input registers"
        )
        with self._lock:
            for i, value in enumerate(values):
                self._input_registers[address + i] = value & 0xFFFF

    @property
    def coils_size(self) -> int:
        return self._coils_size

    @property
    def discrete_inputs_size(self) -> int:
        return self._discrete_inputs_size

    @property
    def holding_registers_size(self) -> int:
        return self._holding_registers_size

    @property
    def input_registers_size(self) -> int:
        return self._input_registers_size

    def reset(self) -> None:
        """Reset all data to initial values."""
        with self._lock:
            self._coils = [False] * self._coils_size
            self._discrete_inputs = [False] * self._discrete_inputs_size
            self._holding_registers = [0] * self._holding_registers_size
            self._input_registers = [0] * self._input_registers_size
