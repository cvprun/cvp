# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/ANSI_escape_code#Control_Sequence_Introducer_commands

from typing import Final, List, NamedTuple

from cvp.terminal.codes import CSI, ESC


class CsiCommand(NamedTuple):
    parameter: str
    intermediate: str
    final: str

    @property
    def full(self) -> str:
        return ESC + CSI + self.parameter + self.intermediate + self.final

    def __str__(self) -> str:
        return self.full

    def __len__(self) -> int:
        return len(self.__str__())

    def as_integer_parameters(self) -> List[int]:
        result = list()
        for part in self.parameter.split(";"):
            if not part:
                result.append(0)
            elif part.isdigit():
                result.append(int(part))
            else:
                raise ValueError("Invalid CSI parameter: not a digit or empty")
        return result


PARAMETER_BYTES_BEGIN: Final[int] = 0x30
PARAMETER_BYTES_END: Final[int] = 0x3F

INTERMEDIATE_BYTES_BEGIN: Final[int] = 0x20
INTERMEDIATE_BYTES_END: Final[int] = 0x2F

FINAL_BYTE_BEGIN: Final[int] = 0x40
FINAL_BYTE_END: Final[int] = 0x7E


def is_parameter_bytes(char: int) -> bool:
    return PARAMETER_BYTES_BEGIN <= char <= PARAMETER_BYTES_END


def is_intermediate_bytes(char: int) -> bool:
    return INTERMEDIATE_BYTES_BEGIN <= char <= INTERMEDIATE_BYTES_END


def is_final_byte(char: int) -> bool:
    return FINAL_BYTE_BEGIN <= char <= FINAL_BYTE_END


def parse_csi_command(text: str) -> CsiCommand:
    if len(text) < 3:
        raise ValueError("CSI sequence must be at least 3 chars (ESC + CSI + final)")
    if text[0] != ESC:
        raise ValueError("CSI sequence must start with ESC")
    if text[1] != CSI:
        raise ValueError("CSI sequence must have CSI as the second character")

    parameter_done = False
    parameter = str()
    intermediate = str()
    final = str()

    for i, c in enumerate(text[2:]):
        match ord(c):
            case x if is_parameter_bytes(x):
                if parameter_done:
                    raise ValueError(
                        "Parameter value cannot appear after "
                        "intermediate in CSI sequence."
                    )
                parameter += c
            case x if is_intermediate_bytes(x):
                intermediate += c
                parameter_done = True
            case x if is_final_byte(x):
                final += c
                break
            case x:
                raise ValueError(f"Invalid char '{c}'({x}) in CSI at {i+2}")

    return CsiCommand(parameter, intermediate, final)
