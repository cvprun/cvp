# -*- coding: utf-8 -*-

from cvp.variables import CVP_EXTENSION, CVP_ROOT_INFO_FILENAME


class CvpFile:
    EXTENSION = CVP_EXTENSION
    ROOT_INFO_FILENAME = CVP_ROOT_INFO_FILENAME

    def __init__(self):
        pass

    def __bool__(self):
        return True
