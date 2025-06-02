def clip_to_lesson(intervals: list[tuple[int, int]], lesson_start: int, lesson_end: int) -> list[tuple[int, int]]:
    clipped = []
    for start, end in intervals:
        if end > lesson_start and start < lesson_end:
            clipped.append((max(start, lesson_start), min(end, lesson_end)))
    return clipped

def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []
    
    intervals.sort()
    result = [intervals[0]]
    
    for start, end in intervals[1:]:
        last_start, last_end = result[-1]
        if start <= last_end:
            result[-1] = (last_start, max(last_end, end))
        else:
            result.append((start, end))
    return result

def intersect_intervals(pupil: list[tuple[int, int]], tutor: list[tuple[int, int]]) -> list[tuple[int, int]]:
    result = []
    i = j = 0
    
    while i < len(pupil) and j < len(tutor):
        start = max(pupil[i][0], tutor[j][0])
        end = min(pupil[i][1], tutor[j][1])
        
        if start < end:
            result.append((start, end))
        
        if pupil[i][1] < tutor[j][1]:
            i += 1
        else:
            j += 1
    
    return result

def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals['lesson']
    
    pupil = [(intervals['pupil'][i], intervals['pupil'][i + 1]) 
             for i in range(0, len(intervals['pupil']), 2)]
    pupil = clip_to_lesson(pupil, lesson_start, lesson_end)
    pupil = merge_intervals(pupil)
    
    tutor = [(intervals['tutor'][i], intervals['tutor'][i + 1]) 
             for i in range(0, len(intervals['tutor']), 2)]
    tutor = clip_to_lesson(tutor, lesson_start, lesson_end)
    tutor = merge_intervals(tutor)
    
    common = intersect_intervals(pupil, tutor)
    return sum(end - start for start, end in common)


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
    for i, test in enumerate(tests, 1):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Ошибка в тесте {i}: получено {test_answer}, ожидалось {test["answer"]}'
