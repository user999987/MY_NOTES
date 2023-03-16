'''
{
  "competitions": [
    ["HTML", "C#"],
    ["C#", "Python"],
    ["Python", "HTML"]
  ],
  "results": [0, 0, 1]
}

"Python"
// C# beats HTML
// Python beats C#
// Python beats HTML
'''
def tournamentWinner(competitions, results):
	# Write your code here.
	n = len(results)
	i = 0
	r={'winner':0}
	winner=''
	
	while i <n:
		home,guest = competitions[i] 
		winning = home if results[i]==1 else guest
		r[winning] = r.get(winning,0)+3
		if r[winning]>r['winner']:
			winner = winning
			r['winner'] = r[winning]
		
		i+=1
	return winner