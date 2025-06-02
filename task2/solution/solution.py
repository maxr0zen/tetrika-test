import wikipediaapi
import csv
from collections import Counter
import os

def get_animals_with_library():
    """Получение данных о животных с Википедии"""
    wiki = wikipediaapi.Wikipedia(
        language='ru',
        user_agent='AnimalCounter/1.0 (https://github.com/yourusername/animalcounter; your@email.com) Python/3.x'
    )
    category = wiki.page("Категория:Животные по алфавиту")
    
    letter_counter = Counter()
    
    for page in category.categorymembers.values():
        if page.ns == 0:  
            title = page.title
            if title:
                letter_counter[title[0].upper()] += 1
    
    return letter_counter

def save_to_csv(counter, filepath):
    """Сохранение данных в CSV файл"""
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for letter, count in sorted(counter.items()):
            writer.writerow([letter, count])

def main():
    """Основная функция программы"""
    try:
        letter_counts = get_animals_with_library()
    
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(parent_dir, 'beasts.csv')
        save_to_csv(letter_counts, csv_path)
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main()
