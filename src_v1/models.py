# -*- coding: iso-8859-1 -*-


class Champion:
    def __init__(
        self, champion, tier, win_rate, pick_rate, ban_rate, weak_against, rank
    ):
        self.champion = champion
        self.tier = tier
        self.win_rate = win_rate
        self.pick_rate = pick_rate
        self.ban_rate = ban_rate
        self.weak_against = weak_against
        self.rank = rank
