import json
from typing import List, Iterable


def json_fold(lines: Iterable[str], max_width: int = 40):
    # Stack of buffers
    stack: List[None | List[str]] = []

    for line in lines:
        stripped = line.strip()
        if stripped.endswith("{") or stripped.endswith("["):
            # Start a new level on the stack
            stack.append([line])
        elif stripped.startswith("}") or stripped.startswith("]"):
            # Close current level: time to see if we can fold or not (collapse to multi-line)
            if stack[-1]:
                stack[-1].append(line)

                closed = stack.pop()
                folded = closed[0] + "".join(s.strip() for s in closed[1:])
                if len(folded) > max_width:
                    # Collapse all levels:
                    for level in range(len(stack)):
                        if stack[level]:
                            yield from stack[level]
                            # Mark level as collapsed
                            stack[level] = None
                    yield from closed
                else:
                    # Move folded result up one level
                    if stack[-1]:
                        stack[-1].append(folded)
                    else:
                        yield folded
            else:
                yield line
        else:
            # Append to current buffer
            if stack[-1]:
                stack[-1].append(line)
            else:
                yield line


if __name__ == "__main__":
    data = {
        "foo": [1, 2, 3, 4, 5, 6],
        "bar": [x * 1111 for x in range(10)],
        "meh": {
            "a": {
                "bb": {
                    "ccc": {
                        "dddd": {
                            "eeeee": {
                                "ffffff": 0,
                            }
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
    }

    lines = json.dumps(data, indent=2).split("\n")
    print(f"{lines=}")

    for max_width in [20, 40, 80, 120]:
        print(f"{max_width=}")

        for res in json_fold(lines=lines, max_width=max_width):
            print(f"[{len(res):4d}] {res=} ")
