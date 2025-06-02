import unittest
from unittest.mock import Mock, patch
from collections import Counter
import os
import tempfile
import shutil
from solution.solution import get_animals_with_library, save_to_csv, main


class MockWikiPage:
    def __init__(self, title):
        self.title = title
        self.ns = 0

class MockCategory:
    def __init__(self, pages):
        self.categorymembers = {i: MockWikiPage(title) for i, title in enumerate(pages)}


class TestWikiAnimals(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения перед каждым тестом"""
        # Настройка мока для Wikipedia API
        self.mock_wiki_patcher = patch('wikipediaapi.Wikipedia')
        self.mock_wiki = self.mock_wiki_patcher.start()
        self.wiki_instance = Mock()
        self.mock_wiki.return_value = self.wiki_instance
        
        # Создаем временную директорию для тестов
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Очистка после каждого теста"""
        self.mock_wiki_patcher.stop()
        # Удаляем временную директорию
        shutil.rmtree(self.test_dir)

    def test_get_animals_with_library(self):
        """Тест получения данных с Википедии"""
        test_data = {
            "Акула": "А",
            "Бегемот": "Б",
            "Волк": "В",
            "Гепард": "Г",
            "Дельфин": "Д"
        }
        
        mock_pages = {}
        for title in test_data.keys():
            page = Mock()
            page.title = title
            page.ns = 0
            mock_pages[title] = page
        
        mock_category = Mock()
        mock_category.categorymembers = mock_pages
        self.wiki_instance.page.return_value = mock_category
        
        result = get_animals_with_library()
        
        self.assertIsInstance(result, Counter)
        self.assertEqual(len(result), len(test_data))
        
        # Проверяем подсчет букв
        for title, letter in test_data.items():
            self.assertGreater(result[letter], 0)

    def test_empty_category(self):
        """Тест пустой категории"""
        self.wiki_instance.page.return_value = MockCategory([])
        result = get_animals_with_library()
        self.assertIsInstance(result, Counter)
        self.assertEqual(len(result), 0)

    def test_save_to_csv(self):
        """Тест сохранения в CSV"""
        # Подготавливаем тестовые данные
        test_data = Counter({
            'А': 5,
            'Б': 3,
            'В': 1
        })
        
        # Используем временную директорию
        test_file = os.path.join(self.test_dir, "test.csv")
        
        # Сохраняем данные
        save_to_csv(test_data, test_file)
        
        # Проверяем, что файл создан
        self.assertTrue(os.path.exists(test_file))
        
        # Проверяем содержимое файла
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            lines = content.split('\n')
            
            # Проверяем количество строк
            self.assertEqual(len(lines), len(test_data))
            
            # Проверяем каждую строку
            for line in lines:
                letter, count = line.split(',')
                self.assertIn(letter, test_data)
                self.assertEqual(int(count), test_data[letter])

    def test_main_function(self):
        """Тест основной функции программы"""
        # Подготавливаем тестовые данные
        test_data = Counter({
            'А': 5,
            'Б': 3,
            'В': 1
        })
        
        output_file = os.path.join(self.test_dir, "beasts.csv")
        
        # Мокаем только get_animals_with_library
        with patch('solution.solution.get_animals_with_library') as mock_get_animals:
            mock_get_animals.return_value = test_data
            
            # Мокаем os.path.dirname чтобы он возвращал нашу тестовую директорию
            with patch('solution.solution.os.path.dirname', return_value=self.test_dir):
                # Запускаем main
                main()
                
                self.assertTrue(os.path.exists(output_file))
                
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    lines = content.split('\n')
                    self.assertEqual(len(lines), len(test_data))
                    
                    for line in lines:
                        letter, count = line.split(',')
                        self.assertIn(letter, test_data)
                        self.assertEqual(int(count), test_data[letter])

    def test_error_handling(self):
        """Тест обработки ошибок"""
        self.wiki_instance.page.side_effect = Exception("Test error")
        
        with self.assertRaises(Exception) as context:
            get_animals_with_library()
        self.assertIn("Test error", str(context.exception))


if __name__ == '__main__':
    unittest.main(verbosity=2)
