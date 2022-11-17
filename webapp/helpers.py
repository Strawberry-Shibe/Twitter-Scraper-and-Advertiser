from numpy import mean


def load_ps_cache(PS):
	"""
	loads all rows from the PersistentStorage database table as key, value pairs

	:returns: dictionary
	"""

	dic = {}
	for item in PS.query.all():
		dic[item.id] = item.content
	return dic


def string_rounding(num):
	magnitude = 0
	while abs(num) >= 1000:
		magnitude += 1
		num /= 1000.0
	return ['%d' % num, '%.1fK' % num, '%.1fM' % num, '%.1fB' % num, '%.1fT' % num][magnitude]


def avg(nums):
	zeros = nums.count(0)
	zeros_mod = int(zeros * 0)

	non_zeros = [i for i in nums if i != 0]
	nz_len = len(non_zeros)
	nz_average = mean(non_zeros)

	average = (nz_average*nz_len) / (nz_len+zeros_mod)

	return average
