import requests

from config import TELEGRAM_SEND_MESSAGE_URL

class TelegramBot:
            
    def __init__(self):
        """"
        Initializes an instance of the TelegramBot class.

        Attributes:
            chat_id:str: Chat ID of Telegram chat, used to identify which conversation outgoing messages should be send to.
            text:str: Text of Telegram chat
            first_name:str: First name of the user who sent the message
        """

        self.chat_id = None
        self.text = None
        self.first_name = None

    def parse_webhook_data(self, data):
        """
        Parses Telegram JSON request from webhook and sets fields for conditional actions

        Args:
            data:str: JSON string of data
        """

        message = data['message']

        self.chat_id = message['chat']['id']
        self.incoming_message_text = message['text'].lower()
        self.first_name = message['from']['first_name']


    def action(self, score_items):
        """
        Conditional actions based on set webhook data.

        Returns:
            bool: True if the action was completed successfully else false
        """

        success = None
        score = self.class_check(score_items)

        if self.incoming_message_text[0] == '/':

            if self.is_number():
                score.incoming(self.first_name, self.incoming_message_text)
                self.outgoing_message_text = score.print_str(self.first_name)
                success = self.send_message()
    
            elif self.incoming_message_text == '/rad':
                self.outgoing_message_text = '🤙'
                success = self.send_message()

            elif self.incoming_message_text == "/high_score":
                success = self.high_score(success,score, limit=10) 
                      
            elif self.incoming_message_text == "/end":
                success = self.end(success,score)

            elif self.incoming_message_text == "/reset":
                success = self.reset(success,score)                  

            elif self.incoming_message_text == "/commands":
                success = self.commands(success)
 
        return success

    def send_message(self):
        """
        Sends message to Telegram servers.
        """

        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.outgoing_message_text))

        return True if res.status_code == 200 else False
    
    def is_number(self):
        """
        Check if the value after the '/' is a int
        """
        try:
            self.incoming_message_text = int (self.incoming_message_text[1:len(self.incoming_message_text)])
            return True
        except ValueError:
                return False        

    def class_check(self, score_items):
        if not self.chat_id in score_items.keys():
            score_items[self.chat_id] = Scoreboard()
        return score_items[self.chat_id]

    def high_score(self, success, score, limit):
        ordered_scores = sorted(score.table.items(), key = lambda x: x[1], reverse=True)
        top = len(ordered_scores)
        if top > limit:
            top = limit
        for i in range(top):
            string = ordered_scores[i][0] + ': ' + str(ordered_scores[i][1])
            self.outgoing_message_text = string
            success = self.send_message()
        return success


    def end(self, success, score):
        max_score = max(score.table.values())
        max_scorers = dict(filter(lambda elem: elem[1]==max_score, score.table.items()))
        for key,values in max_scorers.items():
            string = "High score for " + key + ' with ' + str(values) + " points!"
            self.outgoing_message_text = string
            success = self.send_message()            

        self.reset(success, score)
        return success

    def reset(self, success, score):
        score.clear()
        self.outgoing_message_text = "The Scoreboard is clear"
        success = self.send_message()
        return success

    def commands(self, success):
        self.outgoing_message_text = "'/' and a number addition your score, ex. '/23'"
        success = self.send_message()
        self.outgoing_message_text = "'/high_score' prints the scoreboard in order"
        success = self.send_message()
        self.outgoing_message_text = "'/end' search for the players that have the highest points, prints and reset the scoreboard"
        success = self.send_message()
        self.outgoing_message_text = "'/reset' cleans the scoreboard"
        success = self.send_message()
        return success

    @staticmethod
    def init_webhook(url):
        """
        Initializes the webhook

        Args:
            url:str: Provides the telegram server with a endpoint for webhook data
        """

        requests.get(url)

class Scoreboard:
    def __init__(self):
        self.table = {}

    def incoming(self, name, points):
        if name in self.table.keys():
            self.table[name] = self.table[name] + points
        else:
            self.table[name] = points

    def print_str(self,name):
        return str(name + ': ' + str(self.table[name]))

    def clear(self):
        self.table = {}
