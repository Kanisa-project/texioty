import random
import datetime
import pythonbible as bible
from src.texioty.helpers.tex_helper import TexiotyHelper

"""
normalized_list = bible.get_references(
    "The parable of the cheese in Matthew 5:16-18 and Luke 1:23-25"
    )
verse_ids = bible.convert_references_to_verse_ids(normalized_list)
random_book = bible.Book(random.randint(1, 72))
random_chapter = random.randint(1, bible.get_number_of_chapters(random_book))
random_verse = random.randint(1, bible.get_number_of_verses(random_book, random_chapter))
random_verse_len = random.choice(range(1, 10))
verse_list = []
for i in range(3):
    verse_list.append(f"{random_book.value:03d}{random_chapter:03d}{random_verse+i:03d}")
print(random_book, verse_list, "\n-----\nKING JAMES")
for random_verse_id in verse_list:
    print(bible.get_verse_text(int(random_verse_id), version=bible.Version.KING_JAMES))
print("\n-----\nGENEVA")
for random_verse_id in verse_list:
    print(bible.get_verse_text(int(random_verse_id), version=bible.Version.GENEVA))
print("\n-----\nDEFAULT")
for random_verse_id in verse_list:
    print(bible.get_verse_text(int(random_verse_id)))
"""

class BibleAPI(TexiotyHelper):
    def __init__(self, txo, txi):
        super().__init__(txo, txi)
        self.selected_version = bible.Version.KING_JAMES
        self.current_book = bible.Book(random.randint(1, 72))

    def get_verse_of_the_day(self) -> str:
        return bible.get_verse_text(self.get_random_verse_id(), version=self.selected_version)

    def get_random_verse_id(self) -> int:
        random_chapter = random.randint(1, bible.get_number_of_chapters(self.current_book))
        random_verse = random.randint(1, bible.get_number_of_verses(self.current_book, random_chapter))
        verse_list = []
        for i in range(3):
            verse_list.append(f"{self.current_book.value:03d}{random_chapter:03d}{random_verse+i:03d}")
        return random.choice(verse_list)

WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# book_num = 72 % random.randint(1,7)
book_num = random.randint(1,72) % 7
print(WEEK[datetime.datetime.now().weekday()], book_num, datetime.datetime.now(datetime.timezone.utc))