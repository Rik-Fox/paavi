from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = "web_interface"
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    name = models.StringField()
    age = models.IntegerField()


# PAGES
class MyPage(Page):

    form_model = "player"
    form_fields = ["name"]

    @staticmethod
    def get_timeout_seconds(player: Player):
        participant = player.participant

        if participant.is_dropout:
            return 1  # instant timeout, 1 second
        else:
            return 5 * 60

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        participant = player.participant

        participant.is_dropout = True


### needed for multiplayer games
class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        return super().after_all_players_arrive(group)

    after_all_players_arrive


class Results(Page):
    pass


# page_sequence = [MyPage, ResultsWaitPage, Results]
page_sequence = [MyPage, Results]
