class Team:
    def __init__(self, color: str) -> None:
        self.color = color

    def get_color(self):
        return self.color


class Player:
    def __init__(self, team: Team) -> None:
        self.team = team
        self.money = 0

    def get_player_team_color(self):
        return self.team.color
