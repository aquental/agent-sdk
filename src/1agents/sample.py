"""Numerical data processing and analysis module.

This module provides utilities for processing and analyzing sequences of numerical
data. It includes functions for calculating statistical measures such as the
arithmetic mean with comprehensive input validation and error handling.

Key Functions:
    calculate_average: Computes the arithmetic mean of a sequence of numbers
                      with full validation of input data and edge case handling.
    process_data: Wrapper function that provides additional input validation
                 before delegating to calculate_average() for processing.

Usage Notes:
    - All functions expect sequences (list, tuple) of numeric values (int, float)
    - Empty sequences are not allowed and will raise ValueError
    - Special float values (NaN, infinity) are rejected to prevent invalid results
    - All exceptions include informative error messages with context details
    - Type hints are provided for IDE support and code clarity

Example:
    >>> from sample import calculate_average, process_data
    >>> calculate_average([1, 2, 3, 4, 5])
    3.0
    >>> process_data([10, 20, 30])
    20.0
"""

from typing import Sequence, Union
import math


def calculate_average(numbers: Sequence[Union[int, float]]) -> float:
    """Calculate the arithmetic mean of a sequence of numbers.

    This function computes the average by summing all numbers in the sequence
    and dividing by the count of numbers. It handles edge cases including
    empty sequences, NaN values, and non-numeric values.

    Args:
        numbers: A sequence (list, tuple, etc.) containing numeric values.
                 Must not be empty and should contain only int or float values.

    Returns:
        float: The arithmetic mean of the input numbers.

    Raises:
        ValueError: If the sequence is empty or contains NaN/infinite values.
                    Includes the index of the problematic value for debugging.
        TypeError: If the sequence contains non-numeric values. Includes the
                   actual type found and its index for easy correction.
        ZeroDivisionError: If attempting to divide by zero. This is a defensive
                          measure as empty sequences are checked upfront.

    Examples:
        >>> calculate_average([1, 2, 3, 4, 5])
        3.0
        >>> calculate_average((10, 20, 30))
        20.0
        >>> calculate_average([100])
        100.0
        >>> calculate_average([-5, 5, 10])
        3.3333333333333335
    """
    # Input validation: check for empty sequence
    # This check prevents ZeroDivisionError and ensures the sequence has data to process
    if not numbers or len(numbers) == 0:
        raise ValueError("Cannot calculate average of an empty sequence")

    # Validate that all items are numeric and handle special float values
    validated_numbers = []
    for i, num in enumerate(numbers):
        # Check if the value is numeric (int or float type)
        # This is necessary because the type hint alone doesn't enforce runtime validation
        if not isinstance(num, (int, float)):
            raise TypeError(
                f"All elements must be numeric (int or float). "
                f"Found {type(num).__name__} at index {i}"
            )

        # Check for NaN values which would make the average calculation meaningless
        # NaN is the only float value that is not equal to itself, hence we use math.isnan()
        if isinstance(num, float) and math.isnan(num):
            raise ValueError(
                f"Cannot calculate average with NaN values. "
                f"Found NaN at index {i}"
            )

        # Check for infinity values (positive or negative) which would skew results
        # Infinity in a calculation produces invalid or uninformative results
        if isinstance(num, float) and math.isinf(num):
            raise ValueError(
                f"Cannot calculate average with infinite values. "
                f"Found {'inf' if num > 0 else '-inf'} at index {i}"
            )

        validated_numbers.append(num)

    # Use built-in sum() function for efficiency and accuracy
    # It's optimized and handles integer and float accumulation properly
    total = sum(validated_numbers)

    try:
        # Calculate and return the average
        # We've already validated that the sequence is non-empty, so this should never fail
        average = total / len(validated_numbers)
        return average
    except ZeroDivisionError as e:
        # This exception handler is defensive and should not be reached in normal operation
        # due to the empty check above. If it does occur, it indicates a logic error elsewhere
        raise ZeroDivisionError(
            "Cannot divide by zero: sequence length is zero"
        ) from e


def process_data(data: Union[Sequence[Union[int, float]], None]) -> float:
    """Process and calculate the average of numerical data with validation.

    This function serves as a wrapper around calculate_average() with additional
    input validation to ensure the data is in the correct format before processing.
    It provides a higher-level interface for external callers who may pass data
    from less controlled sources (e.g., user input, API responses).

    Args:
        data: A sequence (list or tuple) containing numeric values (int or float).
              Passing None will trigger a validation error with a clear message.
              Other sequence types (set, generator, etc.) are not accepted to
              ensure consistent behavior and prevent unexpected iteration issues.

    Returns:
        float: The arithmetic mean of the data, computed after full validation.

    Raises:
        ValueError: If data is None (required parameter), or if the sequence is
                   empty, or if it contains invalid numeric values (NaN, infinity).
                   Error messages indicate the specific validation failure.
        TypeError: If data is not a list or tuple type, or if it contains
                   non-numeric values. Includes information about the actual type
                   for easier debugging.
        ZeroDivisionError: If the underlying calculation encounters division by zero.
                          This is a defensive error that should not occur in practice.

    Examples:
        >>> process_data([1, 2, 3, 4, 5])
        3.0
        >>> process_data((10, 20, 30))
        20.0
        >>> process_data([42])
        42.0
        >>> process_data(None)
        Traceback (most recent call last):
            ...
        ValueError: data is required
        >>> process_data("invalid")
        Traceback (most recent call last):
            ...
        TypeError: expected list or tuple, got str
    """
    # Validate that data is not None
    # None is used to represent "no data provided", which is an error condition
    if data is None:
        raise ValueError("data is required")

    # Validate that data is a sequence type (list or tuple)
    # We restrict to these types to ensure:
    # 1. The data is iterable and indexable
    # 2. The behavior is predictable and consistent
    # 3. We avoid issues with lazy iterators or generators that may not support re-iteration
    if not isinstance(data, (list, tuple)):
        raise TypeError(
            f"expected list or tuple, got {type(data).__name__}"
        )

    try:
        # Attempt to calculate the average using the core calculation function
        # This delegates the numeric validation and edge case handling
        return calculate_average(data)
    except ValueError as e:
        # Re-raise ValueError with context about what validation failed
        # The 'from e' preserves the original exception chain for debugging
        raise ValueError(f"Invalid data for average calculation: {str(e)}") from e
    except TypeError as e:
        # Re-raise TypeError with context about type validation issues
        # This helps callers understand what went wrong and how to fix it
        raise TypeError(f"data must contain only numbers: {str(e)}") from e
    except ZeroDivisionError as e:
        # Handle zero division error explicitly with context
        # Though the empty sequence check should prevent this, we handle it for robustness
        raise ZeroDivisionError(
            f"Cannot calculate average: {str(e)}"
        ) from e
