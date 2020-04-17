import pytest 

from app.robo_advisor import to_usd 

def test_to_usd(): 
    # it should apply USD formatting
    assert to_usd(2.40) == "$2.40"

    # it should display two decimal places
    assert to_usd(2.4) == "$2.40"

    # it should round to two places
    assert to_usd(2.4000003) == "$2.40"

    # it should display thousands separators
    assert to_usd(1234567890.5555555) == "$1,234,567,890.56"