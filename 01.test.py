def calculate_average(numbers):
    """
    주어진 숫자 리스트의 평균을 계산합니다.
    
    Args:
        numbers (list): 평균을 계산할 숫자들의 리스트
        
    Returns:
        float: 입력된 숫자들의 평균값. 빈 리스트인 경우 0을 반환합니다.
        
    Examples:
        >>> calculate_average([10, 20, 30])
        20.0
        >>> calculate_average([])
        0
        >>> calculate_average([5])
        5.0
    """
    total = sum(numbers)
    count = len(numbers)
    if count == 0:
        return 0
    return total / count