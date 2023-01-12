class Team:
    def __init__(self, color: tuple[int, int, int]) -> None:
        self.color = color

    def get_color(self) -> tuple[int, int, int]:
        return self.color


class Player:
    def __init__(self, team: Team) -> None:
        self.team = team
        self.money = 0

    def get_team(self) -> Team:
        return self.team

    def get_player_team_color(self) -> tuple[int, int, int]:
        return self.team.color
