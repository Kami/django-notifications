VALID_FILTERS = ('exact', 'startswith', 'endswith', \
				 'contains')


class MatchFilter(object):
	def __init__(self, match_filter = None, model = None):
		self.match_filter = match_filter
		self.model = None
		
		self.valid_fields = self.__get_model_fields(model)
		self.filters = self.__parse_filters(self.match_filter)
		
	def is_valid(self):
		"""
		Returns True if a given match filter is valid, False
		otherwise.
		"""
		if not self.filters:
			return False
					
		return True
	
	def matches(self, field_values):
		"""
		Returns True if the model instance matches the match filter,
		False otherwise.
		"""
		for (field, (value, type)) in self.filters.iteritems():
			if type == 'contains':
				matches = field_values[field].find(value) != -1
			elif type == 'startswith':
				matches = field_values[field].startswith(value)
			elif type == 'endswith':
				matches = field_values[field].endswith(value)
			elif type == 'exact':
				matches = field_values[field] == value
				
			if not matches:
				return False
		
		return True
	
	def __parse_filters(self, string):
		"""
		Parses filters from a string and returns a dictionary of filters on
		success, False if the filters are not valid.
		"""
		splitted = self.match_filter.split(',')
		filters = [filter.split('=') for filter in splitted]
		
		filters_cleaned = {}
		for filter in filters:
			field = filter[0]
			
			if field in filters_cleaned.keys():
				# Filter for this field already exists,
				# skip it.
				continue
			
			try:
				value = filter[1]
			except IndexError:
				# Missing filter value
				return False
			
			if field not in self.valid_fields:
				# Model does not contain this field
				return False
			
			type, value = self.__get_filter_type_and_value(value)
			
			if value.isdigit():
				value = int(value)
			elif value.lower() == 'true':
				value = True
			elif value.lower() == 'false':
				value = False
			
			filters_cleaned[field] = (value, type)

		return filters_cleaned
	
	def __get_filter_type_and_value(self, value):
		"""
		Returns a filter type and a value.
		"""
		if value.startswith('*') and value.endswith('*'):
			value = value[1:-1]
			type = 'contains'
		elif value.startswith('*'):
			value = value[1:]
			type = 'endswith'
		elif value.endswith('*'):
			value = value[:-1]
			type = 'startswith'
		else:
			value = value
			type = 'exact'

		return type, value
	
	def __get_model_fields(self, model):
		"""
		Returns a list of valid fields for a given model.
		"""
		meta = model._meta.fields
		fields = [field.attname for field in meta]
		
		return fields