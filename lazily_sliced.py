# Copyright (c) 2025 Jifeng Wu
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
import sys

if sys.version_info < (3,):
    XRange = xrange
else:
    XRange = range

if sys.version_info < (3, 3):
    from collections import Sequence
else:
    from collections.abc import Sequence


class LazilySliced(Sequence):
    """A lazy sequence wrapper that applies slicing without immediate data copying.

    This class implements the Sequence interface while deferring the actual slicing
    operation until individual elements are accessed. This is useful for memory
    efficiency when working with large sequences where you only need to access
    a small portion of the data.
    """
    __slots__ = ('underlying_sequence', 'index_range')

    def __new__(cls, sequence, slice_obj=None):
        """Create a new LazySlice instance.

        Args:
            sequence: The underlying sequence to be sliced
            slice_obj: Either a slice object to slice the sequence or None.
                      If None, the entire sequence will be used (equivalent to providing slice(None)).

        Returns:
            A new LazySlice instance wrapping the sequence with the specified range object.
        """
        if not isinstance(slice_obj, slice):
            slice_obj = slice(None)

        instance = super(LazilySliced, cls).__new__(cls)
        # Fast path for subclasses
        if isinstance(sequence, LazilySliced):
            instance.underlying_sequence = sequence.underlying_sequence
            instance.index_range = sequence.index_range[slice_obj]
        else:
            instance.underlying_sequence = sequence
            instance.index_range = range(len(sequence))[slice_obj]
        return instance

    def __contains__(self, value):
        for actual_index in self.index_range:
            if self.underlying_sequence[actual_index] == value:
                return True
        return False

    def __getitem__(self, index_or_slice_obj):
        if isinstance(index_or_slice_obj, int):
            # Calculate the actual index in the original sequence
            actual_index = self.index_range[index_or_slice_obj]
            return self.underlying_sequence[actual_index]
        else:
            # Create a new LazySlice
            return LazilySliced(self, index_or_slice_obj)

    def __iter__(self):
        for actual_index in self.index_range:
            yield self.underlying_sequence[actual_index]

    def __len__(self):
        return len(self.index_range)

    def __reversed__(self):
        return self[::-1]

    def __repr__(self):
        return '%s([%s])' % (
            self.__class__.__name__,
            ', '.join(repr(element) for element in self)
        )
