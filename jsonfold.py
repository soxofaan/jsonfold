import json
from typing import List, Iterable, Iterator

_DEFAULT_MAX_WIDTH = 80


def fold_iter(
    lines: Iterable[str], max_width: int = _DEFAULT_MAX_WIDTH
) -> Iterator[str]:
    # Stack of buffers
    stack: List[None | List[str]] = []

    for line in lines:
        stripped = line.strip()

        if stripped.endswith("{") or stripped.endswith("["):
            # Start a new level on the stack
            stack.append([])

        # Yield immediately if current level has collapsed already
        if not stack or stack[-1] is None:
            yield line
        # otherwise: append to buffer and look deeper
        else:
            stack[-1].append(line)

            if stripped in {"}", "},", "]", "],"}:
                # Close current level: time to see if we can fold or not (collapse to multi-line)
                closed = stack.pop()
                # TODO: remove space after trailing element
                folded = closed[0] + " ".join(s.strip() for s in closed[1:])

                if len(folded) > max_width:
                    # Collapse all levels (if not already):
                    for level in range(len(stack)):
                        if stack[level]:
                            yield from stack[level]
                            # Mark level as collapsed
                            # TODO: just remove level from stack instead of setting it None?
                            stack[level] = None
                    yield from closed
                else:
                    # Move folded result up one level (unless it's collapsed already)
                    if stack and stack[-1]:
                        stack[-1].append(folded)
                    else:
                        yield folded


def fold(encoded: str, max_width: int = _DEFAULT_MAX_WIDTH) -> str:
    return "\n".join(fold_iter(encoded.split("\n"), max_width=max_width))


def dumps(obj, max_width: int = _DEFAULT_MAX_WIDTH) -> str:
    return fold(json.dumps(obj=obj, indent=2), max_width=max_width)
