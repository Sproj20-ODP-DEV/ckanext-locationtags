import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def check_empty(key, data, errors, context):
    """Custom validator to check if field is empty or not when form is submitted"""
    if not data.get(key, None):
        errors[key].append('Location field is empty')
    return


class LocationtagsPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)

    # IConfigurer

    def _modify_package_schema(self, schema):
        """Helper function to update schema"""
        schema.update({
            'location': [check_empty,
                            tk.get_converter('convert_to_extras')]
        })
        return schema

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'location-tags')

    # IDatasetForm

    def create_package_schema(self):
            """overriding create_package_schema to include the location field on resources when a dataset is created"""
        # let's grab the default schema in our plugin
        schema = super(LocationTagsPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    
    def update_package_schema(self):
        """overriding update_package_schema to include the location field on resources when a dataset is updated"""

        schema = super(LocationTagsPlugin,
                       self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    
    def show_package_schema(self):
        """overriding update_package_schema to include the location field on resources when a dataset is updated"""
        schema = super(LocationTagsPlugin,
                       self).show_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return False

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
