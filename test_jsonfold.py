from jsonfold import dumps


def test_dumps_none():
    assert dumps(None) == "null"


def test_dumps_int():
    assert dumps(123) == "123"
    assert dumps(-123) == "-123"


def test_dumps_float():
    assert dumps(123.5) == "123.5"


def test_dumps_bool():
    assert dumps(True) == "true"
    assert dumps(False) == "false"


def test_dumps_string():
    assert dumps("hello world") == '"hello world"'


def test_dumps_empty_list():
    assert dumps([]) == "[]"
    assert dumps(()) == "[]"


def test_dumps_empty_dict():
    assert dumps({}) == "{}"


def test_dumps_flat_list():
    assert dumps([1, 2, 3, 4, 5]) == "[1, 2, 3, 4, 5 ]"
    assert dumps([1, 2, 3, 4, 5], max_width=10) == "[\n  1,\n  2,\n  3,\n  4,\n  5\n]"


def test_dumps_flat_dict():
    assert (
        dumps({"name": "alice", "color": "green"})
        == '{"name": "alice", "color": "green" }'
    )
    assert (
        dumps({"name": "alice", "color": "green"}, max_width=10)
        == '{\n  "name": "alice",\n  "color": "green"\n}'
    )
