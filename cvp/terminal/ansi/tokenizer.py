# -*- coding: utf-8 -*-

from typing import Final, List, Optional

from cvp.encoding.ascii import LF
from cvp.terminal.ansi.codes import CSI, ESC
from cvp.terminal.ansi.csi import CsiCommand, parse_csi_command
from cvp.terminal.ansi.fe import is_fe_escape_sequence
from cvp.variables import NOT_FOUND_INDEX

ESCAPE_SEQUENCE_BEGIN: Final[int] = 0x20
ESCAPE_SEQUENCE_END: Final[int] = 0x7F


def valid_escape_sequence(char: int) -> bool:
    return ESCAPE_SEQUENCE_BEGIN <= char <= ESCAPE_SEQUENCE_END


FE_ESCAPE_SEQUENCE_BEGIN: Final[int] = 0x40
FE_ESCAPE_SEQUENCE_END: Final[int] = 0x5F


def valid_fe_escape_sequence(char: int) -> bool:
    return FE_ESCAPE_SEQUENCE_BEGIN <= char <= FE_ESCAPE_SEQUENCE_END


class AnsiToken:
    def __init__(self, token: str):
        self.token = token


class AnsiLineFeed(AnsiToken):
    def __init__(self):
        super().__init__(chr(LF))


class AnsiError(AnsiToken, ValueError):
    def __init__(self, token: str, *args):
        AnsiToken.__init__(self, token)
        ValueError.__init__(self, *args)

    @property
    def error_message(self) -> str:
        return ValueError.__str__(self)


class AnsiNoCharError(AnsiError):
    def __init__(self):
        super().__init__(ESC, "No more characters after ESC (end of line)")


class AnsiInvalidControlCodeError(AnsiError):
    def __init__(self, control_code: str):
        assert 1 == len(control_code)
        super().__init__(
            ESC + control_code,
            f"Control code '{control_code}' (0x{ord(control_code):02X})",
            "is outside the valid escape sequence range.",
            f"(0x{ESCAPE_SEQUENCE_BEGIN:02X} ~ 0x{ESCAPE_SEQUENCE_END:02X})",
        )

    @property
    def control_code(self) -> str:
        return self.token[1]


class AnsiCsiParseError(AnsiError):
    def __init__(self, *args):
        super().__init__(ESC + CSI, *args)


class AnsiEscape(AnsiToken):
    def __init__(self, control_code: str, after: Optional[str] = None):
        assert 1 == len(control_code)
        if after is None:
            after = str()
        assert isinstance(after, str)
        super().__init__(ESC + control_code + after)

    @property
    def control_code(self) -> str:
        return self.token[1]


class AnsiFeEscape(AnsiEscape):
    def __init__(self, control_code: str, after: Optional[str] = None):
        super().__init__(control_code, after)


class AnsiCsiEscape(AnsiFeEscape):
    def __init__(self, command: CsiCommand):
        token = command.full
        assert token[0] == ESC
        assert token[1] == CSI
        after_text = command.full[2:]
        super().__init__(CSI, after_text)
        self.command = command


def _tokenize_ansi_escape_line(remain_text: str, result: List[AnsiToken]) -> None:
    assert remain_text.find(chr(LF)) == NOT_FOUND_INDEX

    while remain_text:
        esc_index = remain_text.find(ESC)
        if esc_index == NOT_FOUND_INDEX:
            result.append(AnsiToken(remain_text))
            break

        if 1 <= esc_index:
            result.append(AnsiToken(remain_text[:esc_index]))

        assert remain_text[esc_index] == ESC
        remain_index = esc_index + 1
        remain_text = remain_text[remain_index:]

        if not remain_text:  # EOL
            result.append(AnsiNoCharError())
            break

        control_code = remain_text[0]
        remain_text = remain_text[1:]

        if not valid_escape_sequence(ord(control_code)):
            result.append(AnsiInvalidControlCodeError(control_code))
            continue

        if not is_fe_escape_sequence(control_code):
            result.append(AnsiEscape(control_code))
            continue

        # If the ESC is followed by a byte in the range 0x40 to 0x5F, the escape
        # sequence is of type Fe. Its interpretation is delegated to the applicable
        # C1 control code standard.

        if control_code != CSI:
            result.append(AnsiFeEscape(control_code))
            continue

        assert control_code == CSI  # Control Sequence Introducer

        try:
            command = parse_csi_command(ESC + CSI + remain_text)
            result.append(AnsiCsiEscape(command))

            remain_index = command.length - 2  # 'ESC + CSI' is 2 length
            assert 1 <= remain_index
            remain_text = remain_text[remain_index:]
        except ValueError as e:
            result.append(AnsiCsiParseError(str(e)))


def _tokenize_ansi_escape_text(remain_text: str, result: List[AnsiToken]) -> None:
    while remain_text:
        lf_index = remain_text.find(chr(LF))
        if lf_index == NOT_FOUND_INDEX:
            _tokenize_ansi_escape_line(remain_text, result)
            break

        if 1 <= lf_index:
            _tokenize_ansi_escape_line(remain_text[:lf_index], result)

        assert remain_text[lf_index] == LF
        result.append(AnsiLineFeed())

        remain_index = lf_index + 1
        remain_text = remain_text[remain_index:]


def tokenize_ansi_escape_text(text: str) -> List[AnsiToken]:
    result: List[AnsiToken] = list()
    try:
        _tokenize_ansi_escape_text(text, result)
    finally:
        return result
