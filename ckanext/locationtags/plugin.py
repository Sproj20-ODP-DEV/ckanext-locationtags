import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class LocationtagsPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'location-tags')


    # IDatasetForm

    """overriding create_package_schema to include the location field on resources when a dataset is created"""

    def create_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(LocationTagsPlugin, self).create_package_schema()
        # our custom field
        schema.update({
            'location': [toolkit.get_validator('ignore_missing'),
                         toolkit.get_converter('convert_to_extras')]
        })
        return schema

    """overriding update_package_schema to include the location field on resources when a dataset is updated"""

    def update_package_schema(self):
        schema = super(LocationTagsPlugin,
                       self).update_package_schema()
        # our custom field
        schema.update({
            'location': [toolkit.get_validator('ignore_missing'),
                         toolkit.get_converter('convert_to_extras')]
        })
        return schema

    """overriding update_package_schema to include the location field on resources when a dataset is updated"""

    def show_package_schema(self):
        schema = super(LocationTagsPlugin,
                       self).show_package_schema()
        schema.update({
            'custom_text': [toolkit.get_converter('ignore_missing'),
                            toolkit.get_validator('convert_to_extras')]
        })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return False

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []