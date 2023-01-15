class Team:
    def __init__(self, color: tuple[int, int, int]) -> None:
        self.color = color

    def get_color(self) -> tuple[int, int, int]:
        return self.color


class Player:
    def __init__(self, team: Team) -> None:
        self.team = team
        self.money = 70
        self.player_profit = 0
        self.base_is_alive = True

    def get_team(self) -> Team:
        return self.team

    def get_player_team_color(self) -> tuple[int, int, int]:
        return self.team.color
