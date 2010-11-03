#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim:syntax=python:sw=4:ts=4:expandtab
import vogelerunner
#from vogelerunner.mainmodule import get_reverse_phone


class TestAstInfoCli(object):
    def setup(self):
        pass

    def teardown(self):
        pass

    def test_annuaire_inverse(self):
        result = '1234' # get_reverse_phone('0169964797')
        assert result == 'FR France  Savigny sur Orge Stepniewski Edwige'
