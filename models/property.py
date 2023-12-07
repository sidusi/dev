from odoo import fields, models, api

class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'


    name = fields.Char(string="Name", required=True)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offerReceived', 'Offer Received'),
            ('offerAccepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancel', 'Cancelled')
        ],
        string="State",
        default='new'
    )
    tag_ids = fields.Many2many('estate.property.tag',string="Property Tag")
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Price")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation",
        default='north'
    )
    total_area = fields.Integer(string="Total Area(sqm)", compute="_compute_total_area")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    sales_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", domain=[('is_company', '=', True)])
    phone = fields.Char(string="Phone", related='buyer_id.phone')
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")


    def action_cancel(self):
        self.state = 'cancel'

    def action_sold(self):
        self.state = 'sold'

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_property_view(self):
        return{
            'type' : 'ir.actions.act_window',
            'name' : f"{self.name} - Offers",
            'domain' : [('property_id', '=', self.id)],
            'view_mode' : 'tree',
            'res_model' : 'estate.property.offer'
        }

    def action_url_action(self):
        return{
            'type' : 'ir.actions.act_url',
            'url' : 'https://www.odoo.com/documentation/17.0/developer.html',
            'target' : 'new',
        }

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for record in self:
            if self.offer_ids:
                record.best_offer = max(self.offer_ids.mapped('price'))
            else:
                record.best_offer = 0

    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Estate Property - %s' % self.name

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char(string='Name', required=True)

class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string="Color")


