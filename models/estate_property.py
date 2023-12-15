from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    sales_id = fields.Many2one("res.users", required=True)

    @api.model_create_multi
    def create(self, values_list):
        for val in values_list:
        #     reference to model name
            sales_person_property_ids = self.env[self._name].search_count([("sales_id", "=", val.get("sales_id"))])
            if sales_person_property_ids >= 2:
                raise ValidationError("User already has enough 2 properties assigned to him ")
        return super(EstateProperty, self).create(values_list)
