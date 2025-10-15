from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _apply_theme_colors_from_params(self):
        """Apply theme colors from system parameters"""
        theme_colors = [
            'color_appsmenu_text',
            'color_appbar_text', 
            'color_appbar_active',
            'color_appbar_background'
        ]
        
        variables = []
        for color in theme_colors:
            param_key = f'theme.{color}'
            value = self.env['ir.config_parameter'].sudo().get_param(param_key)
            if value:
                variables.append({'name': color, 'value': value})
        
        if variables:
            self.env['web_editor.assets'].replace_color_variables_values(
                '/muk_web_theme/static/src/scss/colors.scss',
                'web._assets_primary_variables',
                variables
            )
        
        return True

    @api.model
    def _post_init_apply_theme_colors(self):
        """Post-install hook to apply theme colors"""
        self = self.env['res.config.settings']
        self._apply_theme_colors_from_params()
