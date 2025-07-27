# `lazily-sliced`

A memory-efficient Python sequence wrapper that applies slicing operations lazily, deferring data access until elements are actually needed.

## Features

- **Zero-copy slicing**: Avoids immediate data duplication when slicing sequences
- **Full Sequence interface**: Implements all `collections.abc.Sequence` operations
- **Portable**: Python 2 & 3 compatible, no dependencies
- **Memory efficient**: Uses `__slots__` and lazy evaluation
- **Composable**: Handles nested slicing operations efficiently

## Installation

```bash
pip install lazily-sliced
```

## Usage

```python
from lazily_sliced import LazilySliced

# Create from any sequence
data = list(range(1000))
lazy = LazilySliced(data, slice(100, 200))

# Standard sequence operations work
print(len(lazy))  # 100
print(lazy[10])   # 110
print(105 in lazy) # True

# Supports nested slicing
subset = lazy[10:20:2]
print(subset) # LazilySliced([110, 112, 114, 116, 118])
for item in lazy:
    print(item)
```

## When to Use

Ideal for:

- Working with large sequences where you need small slices
- Memory-constrained environments
- Chaining multiple slicing operations
- Cases where immediate data copying is expensive

## Performance Characteristics

| Operation    | Time Complexity | Notes                         |
|--------------|-----------------|-------------------------------|
| `len()`      | O(1)            |                               |
| Index access | O(1)            |                               |
| Iteration    | O(n)            | Proportional to slice size    |
| `in` check   | O(n)            | Worst case scans entire slice |
| Memory usage | O(1)            | Constant overhead             |

## Limitations

- Read-only (doesn't support item assignment)
- Underlying sequence must support integer indexing
- Slices must be within bounds of original sequence

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).