# -*- coding: utf-8 -*-


class ModbusException(Exception):
    """Base exception for Modbus errors."""

    pass


class ModbusTimeoutError(ModbusException):
    """Raised when a Modbus operation times out."""

    pass


class ModbusConnectionError(ModbusException):
    """Raised when a Modbus connection fails."""

    pass


class ModbusProtocolError(ModbusException):
    """Raised when a Modbus protocol error occurs."""

    pass


class ModbusInvalidAddressError(ModbusException):
    """Raised when an invalid address is specified."""

    pass


class ModbusInvalidValueError(ModbusException):
    """Raised when an invalid value is specified."""

    pass


class ModbusSlaveError(ModbusException):
    """Raised when a Modbus slave returns an error response."""

    def __init__(self, function_code: int, exception_code: int):
        self.function_code = function_code
        self.exception_code = exception_code
        super().__init__(
            f"Modbus error: FC=0x{function_code:02X}, "
            f"Exception=0x{exception_code:02X} ({self.exception_name})"
        )

    @property
    def exception_name(self) -> str:
        names = {
            0x01: "ILLEGAL_FUNCTION",
            0x02: "ILLEGAL_DATA_ADDRESS",
            0x03: "ILLEGAL_DATA_VALUE",
            0x04: "SLAVE_DEVICE_FAILURE",
            0x05: "ACKNOWLEDGE",
            0x06: "SLAVE_DEVICE_BUSY",
            0x08: "MEMORY_PARITY_ERROR",
            0x0A: "GATEWAY_PATH_UNAVAILABLE",
            0x0B: "GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND",
        }
        return names.get(self.exception_code, "UNKNOWN")
