import textwrap
import pytest

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
    assert dumps([1, 2, 3, 4, 5], max_width=1) == "[\n  1,\n  2,\n  3,\n  4,\n  5\n]"


def test_dumps_flat_dict():
    assert (
        dumps({"name": "alice", "color": "green"})
        == '{"name": "alice", "color": "green" }'
    )
    assert (
        dumps({"name": "alice", "color": "green"}, max_width=10)
        == '{\n  "name": "alice",\n  "color": "green"\n}'
    )
    assert (
        dumps({"name": "alice", "color": "green"}, max_width=1)
        == '{\n  "name": "alice",\n  "color": "green"\n}'
    )


@pytest.mark.parametrize(
    ["max_width", "obj", "expected"],
    [
        (
            80,
            {"five": list(range(5)), "ten": list(range(10))},
            '{"five": [0, 1, 2, 3, 4 ], "ten": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ] }',
        ),
        (
            40,
            {"five": list(range(5)), "ten": list(range(10))},
            """\
            {
              "five": [0, 1, 2, 3, 4 ],
              "ten": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
            }""",
        ),
        (
            30,
            {"five": list(range(5)), "ten": list(range(10))},
            """\
            {
              "five": [0, 1, 2, 3, 4 ],
              "ten": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9
              ]
            }""",
        ),
        (
            80,
            {str(x): chr(97 + x) * x for x in range(5)},
            '{"0": "", "1": "b", "2": "cc", "3": "ddd", "4": "eeee" }',
        ),
        (
            40,
            {str(x): chr(97 + x) * x for x in range(5)},
            """\
            {
              "0": "",
              "1": "b",
              "2": "cc",
              "3": "ddd",
              "4": "eeee"
            }""",
        ),
    ],
)
def test_dumps_listings(max_width, obj, expected):
    expected = textwrap.dedent(expected)
    assert dumps(obj, max_width=max_width) == expected


@pytest.mark.parametrize(
    ["max_width", "obj", "expected"],
    [
        (
            80,
            {
                "query": "get stuff",
                "results": {
                    "count": 5,
                    "data": [
                        {"id": 1, "name": "Alice", "payments": None},
                        {"id": 23, "name": "Bob", "payments": [100, 200]},
                        {
                            "id": 3000,
                            "name": "Carol",
                            "status": "premium",
                            "payments": [1000, 3000, 2000, 2, -5],
                        },
                        {"id": 44, "name": "Dave", "payments": [1, 5]},
                        {
                            "id": 555,
                            "name": "Eric",
                            "payments": [44, {"price": 666, "currency": "tulip bulbs"}],
                        },
                    ],
                },
                "_id": "123kthxbye",
            },
            """\
            {
              "query": "get stuff",
              "results": {
                "count": 5,
                "data": [
                  {"id": 1, "name": "Alice", "payments": null },
                  {"id": 23, "name": "Bob", "payments": [100, 200 ] },
                  {
                    "id": 3000,
                    "name": "Carol",
                    "status": "premium",
                    "payments": [1000, 3000, 2000, 2, -5 ]
                  },
                  {"id": 44, "name": "Dave", "payments": [1, 5 ] },
                  {
                    "id": 555,
                    "name": "Eric",
                    "payments": [44, {"price": 666, "currency": "tulip bulbs" } ]
                  }
                ]
              },
              "_id": "123kthxbye"
            }""",
        ),
        (
            120,
            {
                "query": "get stuff",
                "results": {
                    "count": 5,
                    "data": [
                        {"id": 1, "name": "Alice", "payments": None},
                        {"id": 23, "name": "Bob", "payments": [100, 200]},
                        {
                            "id": 3000,
                            "name": "Carol",
                            "status": "premium",
                            "payments": [1000, 3000, 2000, 2, -5],
                        },
                        {"id": 44, "name": "Dave", "payments": [1, 5]},
                        {
                            "id": 555,
                            "name": "Eric",
                            "payments": [44, {"price": 666, "currency": "tulip bulbs"}],
                        },
                    ],
                },
                "_id": "123kthxbye",
            },
            """\
            {
              "query": "get stuff",
              "results": {
                "count": 5,
                "data": [
                  {"id": 1, "name": "Alice", "payments": null },
                  {"id": 23, "name": "Bob", "payments": [100, 200 ] },
                  {"id": 3000, "name": "Carol", "status": "premium", "payments": [1000, 3000, 2000, 2, -5 ] },
                  {"id": 44, "name": "Dave", "payments": [1, 5 ] },
                  {"id": 555, "name": "Eric", "payments": [44, {"price": 666, "currency": "tulip bulbs" } ] }
                ]
              },
              "_id": "123kthxbye"
            }""",
        ),
        (
            80,
            {
                "a": {
                    "bb": {
                        "ccc": {
                            "dddd": {
                                "eeeee": {
                                    "ffffff": "foo",
                                },
                            }
                        },
                        "CCC": {
                            "D": 13,
                            "DD": 133,
                            "DDD": 1333,
                        },
                    }
                }
            },
            """\
            {
              "a": {
                "bb": {
                  "ccc": {"dddd": {"eeeee": {"ffffff": "foo" } } },
                  "CCC": {"D": 13, "DD": 133, "DDD": 1333 }
                }
              }
            }""",
        ),
        (
            120,
            {
                "a": {
                    "bb": {
                        "ccc": {
                            "dddd": {
                                "eeeee": {
                                    "ffffff": "foo",
                                },
                            }
                        },
                        "CCC": {
                            "D": 13,
                            "DD": 133,
                            "DDD": 1333,
                        },
                    }
                }
            },
            '{"a": {"bb": {"ccc": {"dddd": {"eeeee": {"ffffff": "foo" } } }, "CCC": {"D": 13, "DD": 133, "DDD": 1333 } } } }',
        ),
        (
            40,
            {
                "a": {
                    "bb": {
                        "ccc": {
                            "dddd": {
                                "eeeee": {
                                    "ffffff": "foo",
                                },
                            }
                        },
                        "CCC": {
                            "D": 13,
                            "DD": 133,
                            "DDD": 1333,
                        },
                    }
                }
            },
            """\
            {
              "a": {
                "bb": {
                  "ccc": {
                    "dddd": {
                      "eeeee": {"ffffff": "foo" }
                    }
                  },
                  "CCC": {
                    "D": 13,
                    "DD": 133,
                    "DDD": 1333
                  }
                }
              }
            }""",
        ),
    ],
)
def test_dumps_deep_nesting(obj, max_width, expected):
    expected = textwrap.dedent(expected)
    assert dumps(obj, max_width=max_width) == expected
