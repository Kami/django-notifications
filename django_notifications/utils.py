from django.template import Template, VariableNode
from django.db.models.fields.related import ForeignKey

def get_template_variables_list(string = None):
	"""
	Returns a list of all the template variable which
	appear in a given string.
	"""
	template = Template(string)
	nodes = template.nodelist
	
	variables = []
	for node in nodes:
		if not isinstance(node, VariableNode):
			# We are only interested in variable nodes
			continue
		variable = node.filter_expression.var.var
		variables.append(variable)
		
	if not variables:
		return None
	
	return variables

def get_model_field_names(model, include_related = False):
	"""
	Returns a list of valid fields for a given model.
	
	If include_related = True, it also includes a list of
	fields for all the related objects (foreign keys).
	"""
	meta = model._meta
	model_name = meta.module_name
	meta_fields = meta._fields()
	
	fields = []
	# First we check all the model field
	for field in meta_fields:
		field_name = field.attname
		
		if include_related and isinstance(field, ForeignKey):
			# A foreign key, include all the fields for the related model
			field_name = field.name
			related_model = field.related.parent_model
			related_model_name = related_model._meta.module_name

			related_fields = get_model_field_names(related_model)
			related_fields = ['%s.%s' % (field_name, field) \
							 for field in related_fields]
			
			fields.extend(related_fields)
		fields.append(field_name)

	return fields