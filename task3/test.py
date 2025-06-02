from solution.solution import *
import unittest

class TestSolution(unittest.TestCase):
    def test_clip_to_lesson(self):
        # Тест на пустой список
        self.assertEqual(clip_to_lesson([], 0, 100), [])
        
        # Тест на интервалы вне урока
        self.assertEqual(clip_to_lesson([(0, 50), (150, 200)], 100, 120), [])
        
        # Тест на интервалы частично внутри урока
        self.assertEqual(
            clip_to_lesson([(50, 150), (110, 130)], 100, 120),
            [(100, 120), (110, 120)]
        )
        
        # Тест на интервал полностью внутри урока
        self.assertEqual(clip_to_lesson([(110, 115)], 100, 120), [(110, 115)])

    def test_merge_intervals(self):
        # Тест на пустой список
        self.assertEqual(merge_intervals([]), [])
        
        # Тест на неперекрывающиеся интервалы
        self.assertEqual(
            merge_intervals([(1, 2), (3, 4), (5, 6)]),
            [(1, 2), (3, 4), (5, 6)]
        )
        
        # Тест на перекрывающиеся интервалы
        self.assertEqual(
            merge_intervals([(1, 3), (2, 4), (5, 7), (6, 8)]),
            [(1, 4), (5, 8)]
        )
        
        # Тест на полностью перекрывающиеся интервалы
        self.assertEqual(
            merge_intervals([(1, 5), (2, 3), (4, 6)]),
            [(1, 6)]
        )
        
        # Тест на несортированные интервалы
        self.assertEqual(
            merge_intervals([(3, 4), (1, 2), (5, 6)]),
            [(1, 2), (3, 4), (5, 6)]
        )

    def test_intersect_intervals(self):
        # Тест на пустые списки
        self.assertEqual(intersect_intervals([], []), [])
        self.assertEqual(intersect_intervals([(1, 2)], []), [])
        self.assertEqual(intersect_intervals([], [(1, 2)]), [])
        
        # Тест на непересекающиеся интервалы
        self.assertEqual(intersect_intervals([(1, 2)], [(3, 4)]), [])
        
        # Тест на частично пересекающиеся интервалы
        self.assertEqual(
            intersect_intervals([(1, 3), (4, 6)], [(2, 5)]),
            [(2, 3), (4, 5)]
        )
        
        # Тест на полностью пересекающиеся интервалы
        self.assertEqual(
            intersect_intervals([(1, 5)], [(2, 3)]),
            [(2, 3)]
        )
        
        # Тест на множественные пересечения
        self.assertEqual(
            intersect_intervals([(1, 3), (4, 6)], [(2, 5)]),
            [(2, 3), (4, 5)]
        )

    def test_appearance(self):
        # Тест на пустые интервалы
        self.assertEqual(
            appearance({
                'lesson': [0, 100],
                'pupil': [],
                'tutor': []
            }),
            0
        )
        
        # Тест на отсутствие пересечений
        self.assertEqual(
            appearance({
                'lesson': [0, 100],
                'pupil': [10, 20],
                'tutor': [30, 40]
            }),
            0
        )
        
        # Тест на полное пересечение
        self.assertEqual(
            appearance({
                'lesson': [0, 100],
                'pupil': [10, 30],
                'tutor': [10, 30]
            }),
            20
        )
        
        # Тест на частичное пересечение
        # pupil: [(10,30), (40,50)]
        # tutor: [(20,45)]
        # Пересечения: (20,30) = 10 сек и (40,45) = 5 сек
        # Итого: 15 секунд
        self.assertEqual(
            appearance({
                'lesson': [0, 100],
                'pupil': [10, 30, 40, 50],
                'tutor': [20, 45]
            }),
            15
        )
        
        # Тест на интервалы вне урока
        self.assertEqual(
            appearance({
                'lesson': [0, 100],
                'pupil': [-10, -5, 110, 120],
                'tutor': [-20, -15, 105, 115]
            }),
            0
        )

    def test_appearance_with_real_data(self):
        test_cases = [
            {'intervals': {'lesson': [1594663200, 1594666800],
                          'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 
                                   1594663396, 1594666472],
                          'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
             'answer': 3117},
            {'intervals': {'lesson': [1594702800, 1594706400],
                          'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 
                                   1594704512, 1594704513, 1594704564, 1594705150, 
                                   1594704581, 1594704582, 1594704734, 1594705009, 
                                   1594705095, 1594705096, 1594705106, 1594706480, 
                                   1594705158, 1594705773, 1594705849, 1594706480, 
                                   1594706500, 1594706875, 1594706502, 1594706503, 
                                   1594706524, 1594706524, 1594706579, 1594706641],
                          'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 
                                   1594705149, 1594706463]},
             'answer': 3577},
            {'intervals': {'lesson': [1594692000, 1594695600],
                          'pupil': [1594692033, 1594696347],
                          'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
             'answer': 3565}
        ]
        
        for i, test in enumerate(test_cases, 1):
            with self.subTest(test_number=i):
                self.assertEqual(
                    appearance(test['intervals']),
                    test['answer'],
                    f'Ошибка в тесте {i}'
                )

if __name__ == '__main__':
    unittest.main(verbosity=2)
