import unittest
from parse_organization import clear_value, Organization


class TestClear(unittest.TestCase):
    def test_clear_value(self):
        text = '''
            \n\n       
            Проверочный текст:   \n
                \n\n\n  \n
        '''
        self.assertEqual(
            clear_value(text),
            'Проверочный текст:',
            'очистка текста срабатывает неправильно'
        )


if __name__ == "__main__":
    unittest.main()