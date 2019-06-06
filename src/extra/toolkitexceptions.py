# -*- coding: utf-8 -*-


class ToolkitException(Exception):
    def __init__(self, msg=''):
        Exception.__init__(self, f'{msg}')


class PeerWasBruted(ToolkitException):
    def __init__(self):
        super().__init__(msg='Peer has been successfully bruted.')
