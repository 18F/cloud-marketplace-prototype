import pytest

from .factories import *


def test_team_str():
    team = TeamFactory.build()
    assert team.name == str(team)
