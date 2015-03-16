def expected_value(ra, rb):
	return 1/(1 + pow(10, (rb - ra)/400))

def calculate_elo(winner, loser):
	winner_expected = expected_value(winner, loser)
	loser_expected = expected_value(loser, winner)

	winner_new = winner + 40*(1 - winner_expected)
	loser_new = loser - (40*loser_expected)

	return [winner_new, loser_new]
