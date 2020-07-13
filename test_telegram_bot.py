import unittest
from telegram_bot import TelegramBot, Scoreboard

class TelegramBotTestCase(unittest.TestCase):
    def setUp(self):
        self.score_items = {}
        self.bot = TelegramBot()
        self.score = Scoreboard()
        self.chat_id = '-419901661'
        self.score_items[self.chat_id] = self.score        
        self.first_name = 'John'


    def configure_bot_action_data(self, incoming_message_text):
        self.bot.chat_id = self.chat_id
        self.bot.incoming_message_text = incoming_message_text
        self.bot.first_name = self.first_name


    def test_parse_webhook_data(self):
        # self.configure_bot_action_data()
        pass


    def mock_send_message(*args, **kwargs):
        return True

    def test_action(self):
        self.bot.send_message = self.mock_send_message

        # Number command with a number
        self.configure_bot_action_data('/123')
        response = self.bot.action(self.score_items)
        self.assertEqual(response, True)

        # Number command with a negative number
        self.configure_bot_action_data('/-123')
        response = self.bot.action(self.score_items)
        self.assertEqual(response, True)

        # Number without slash
        self.configure_bot_action_data(' -123')
        self.assertIsNone(self.bot.action(self.score_items))

        # Rad command
        self.configure_bot_action_data('/rad')
        self.assertTrue(self.bot.action(self.score_items))

        # String without slash
        self.configure_bot_action_data('test')
        self.assertIsNone(self.bot.action(self.score_items))

        # String with slash
        self.configure_bot_action_data('/test')
        self.assertIsNone(self.bot.action(self.score_items))

    def test_class_check(self):
        self.score_items = {}
        self.configure_bot_action_data("/123")
        self.assertEqual(self.bot.class_check(self.score_items), self.score_items[self.chat_id])


    def test_high_score(self):            
        self.bot.send_message = self.mock_send_message

        self.score.incoming('John', 123)
        success = None
        self.assertEqual(self.bot.high_score(success, self.score, limit=2), True)
    
    def test_reset(self):
        self.bot.send_message = self.mock_send_message
        self.score.incoming('John', 123)
        success = None
        self.assertEqual(self.bot.reset(success, self.score), True)        

    def test_end(self):
        self.bot.send_message = self.mock_send_message
        self.score.incoming('John', 123)
        success = None
        self.assertEqual(self.bot.reset(success, self.score), True)   


    def test_commands(self):
        self.bot.send_message = self.mock_send_message
        success = None
        self.assertEqual(self.bot.commands(success), True)   

class ScoreboardTestCase(unittest.TestCase):
    def setUp(self):
        self.score = Scoreboard()


    def test_init(self):
        self.assertEqual(self.score.table, {})

    def test_incoming(self):
        # New User
        self.score.incoming('John', 123)
        self.assertEqual(self.score.table, {'John':123})

        # Existing User
        self.score.incoming('John', 123)
        self.assertEqual(self.score.table, {'John':246})

        # Different User
        self.score.incoming('Mark', 321)
        self.assertEqual(self.score.table, {'John':246, 'Mark':321})

        # Negative Number
        self.score.incoming('Mark', -21)
        self.assertEqual(self.score.table, {'John':246, 'Mark':300})

    def test_print(self):
        self.score.incoming('John', 123)
        self.assertEqual(self.score.print_str('John'), 'John: 123')

    def test_clear(self):
        self.score.incoming('John',123)
        self.score.clear()
        self.assertEqual(self.score.table, {})

if __name__ == '__main__':
    unittest.main()
