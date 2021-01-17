from .CartesianProductPolyDomain import * 

class Zeta3Domain1(CartesianProductPolyDomain):
	'''
	This domain iters polynomials from this kind:
	a(n) = (x0*n + x1)(x2*n*(n + 1) + x3)
	b(n) = x4*n^6

	where x0, x1, x2, x3, x4 are 5 freedom degrees

	to reduce search space and be similar to other results- 
	keep x0 and x1 low
	keep x4 negative

	this is a decedent of CartesianProductPolyDomain since an and bn has no
	particular relation
	'''

	def __init__(self, a_coefs_ranges, b_coef_range, *args, **kwargs):
		'''
		a_coefs_ranges - the range allowed for each coef from x0,x1,x2,x3
		in this format-
			[(x0_min, x0_max), ... ]
		'''
		super().__init__(
			a_deg = 4, # deg refers to degree of freedom, not poly_deg
			b_deg = 1,
			a_coef_range = [0,0], # junk values, will override soon
			b_coef_range = [0,0]
			,*args, **kwargs)

		self.a_coef_range = a_coefs_ranges
		self.b_coef_range = [b_coef_range]

		self.an_length = self.get_an_length()
		self.bn_length = self.get_bn_length()
		self.num_iterations = self.an_length * self.bn_length

		self.an_domain_range, self.bn_domain_range = self.dump_domain_ranges()

	def get_calculation_method(self):
		def an_iterator(free_vars, max_runs, start_n=1):
			for i in range(start_n, max_runs):
				yield (free_vars[0]*i + free_vars[1])*(free_vars[2]*i*(i+1) + free_vars[3])

		def bn_iterator(free_vars, max_runs, start_n=1):
			for i in range(start_n, max_runs):
				yield free_vars[0]*(i**6)

		return an_iterator, bn_iterator

	# allows user to get actual data regarding the polynomals he got
	@classmethod
	def get_poly_an_degree(an_coefs):
		deg = 3
		if an_coefs[0] == 0:
			deg -= 1
		if an_coefs[2] ==0:
			deg -= 2
		return deg

	@classmethod
	def get_poly_bn_degree(bn_coefs):
		return 6

	@classmethod
	def get_poly_an_lead_coef(an_coefs):
		return an_coefs[0] * an_coefs[2]

	@classmethod
	def get_poly_bn_lead_coef(bn_coefs):
		return bn_coefs[0]
	
	def check_for_convegence(self, an_coefs, bn_coefs):
		# see Ramanujan paper for convergence condition on balanced 
		# an & bn degrees
		a_leading_coef = an_coefs[0] * an_coefs[2]

		# checking for >= as well as >, might be overkill
		return bn_coefs[0] * 4 >= -1 * (a_leading_coef**2)

	def iter_polys(self, primary_looped_domain):
		# TODO - use parent 
		an_domain, bn_domain = self.dump_domain_ranges()

		if primary_looped_domain == 'a':
			a_coef_iter = product(*an_domain)
			for a_coef in a_coef_iter:
				b_coef_iter = product(*bn_domain)
				for b_coef in b_coef_iter:
					if self.check_for_convegence(a_coef, b_coef):
						yield a_coef, b_coef
		else:
			b_coef_iter = product(*bn_domain)
			for b_coef in b_coef_iter:
				a_coef_iter = product(*an_domain)
				for a_coef in a_coef_iter:
					if self.check_for_convegence(a_coef, b_coef):
						yield a_coef, b_coef
