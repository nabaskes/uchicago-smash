def expected_value(ra, rb):
	return 1/(1 + pow(10, (rb - ra)/400))

def calculate_elo(winner, loser):
	winner_expected = expected_value(winner, loser)
	loser_expected = expected_value(loser, winner)

	winner_new = winner + K*(1 - winner_expected)
	loser_new = loser - (K*loser_expected)

	return [winner_new, loser_new]
