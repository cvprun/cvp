# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .fft2_node import Fft2Node
from .fft_node import FftNode
from .fftfreq_node import FftfreqNode
from .fftn_node import FftnNode
from .fftshift_node import FftshiftNode
from .ifft2_node import Ifft2Node
from .ifft_node import IfftNode
from .ifftn_node import IfftnNode
from .ifftshift_node import IfftshiftNode
from .irfft2_node import Irfft2Node
from .irfft_node import IrfftNode
from .irfftn_node import IrfftnNode
from .rfft2_node import Rfft2Node
from .rfft_node import RfftNode
from .rfftfreq_node import RfftfreqNode
from .rfftn_node import RfftnNode


def get_fft_nodes() -> List[Node]:
    """Get all fft nodes."""
    return [
        FftNode(),
        IfftNode(),
        Fft2Node(),
        Ifft2Node(),
        FftnNode(),
        IfftnNode(),
        RfftNode(),
        IrfftNode(),
        Rfft2Node(),
        Irfft2Node(),
        RfftnNode(),
        IrfftnNode(),
        FftfreqNode(),
        RfftfreqNode(),
        FftshiftNode(),
        IfftshiftNode(),
    ]
