from typing import Callable, Iterable

def csort[_T, SupportsRichComparison](iterable: Iterable[_T], columns, key: Callable[[_T], SupportsRichComparison]=None) -> list[_T]:
    """Sortiert eine Iterable so, dass Spalten, die horizontal aufgefüllt werden, wie vertikal aufgefüllt aussehen.
    
    Wenn eine Liste normalerweise die Anordnung
    ```
    [
        1, 2, 3,
        4, 5, 6
    ]
    ```
    Dann wird sie durch diese Funktion zu
    ```
    [
        1, 3, 5,
        2, 4, 6
    ]
    ```
    sortiert.
    
    """
    items = list(iterable)

    if key is not None:
        items.sort(key=key)

    n = len(items)
    rows = (n + columns - 1) // columns  # aufrunden

    result = []
    for row in range(rows):
        for col in range(columns):
            index = col * rows + row
            if index < n:
                result.append(items[index])

    return result