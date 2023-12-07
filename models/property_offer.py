from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    name = fields.Char(string="Name", compute="_compute_offer_name")
    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
            ('define', 'Define status for this offer..')
        ],
        string="Status",
        default='define'
    )
    partner_id = fields.Many2one('res.partner', string="Costumer")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer(string="Validity(Days)", default=7)
    deadline = fields.Date(string="Deadline", compute='_compute_offer_deadline', inverse='_inverse_offer_deadline')
    offer_date = fields.Date(string="Offer Date", default=fields.Date.today())

    # api.depends make compute fields with ORM, api.onchange make compute with Form view and it doesn't need to loop the record

    @api.depends('offer_date','validity')
    def _compute_offer_deadline(self):
        for rec in self:
            if rec.offer_date and rec.validity:
                rec.deadline = rec.offer_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    def _inverse_offer_deadline(self):
        for rec in self:
            if rec.deadline and rec.offer_date:
                rec.validity = (rec.deadline - rec.offer_date).days
            else:
                rec.validity = False

    def action_accepted_offer(self):
        if self.property_id:
            self._validate_accepted_offer()
            self.property_id.write({
                'selling_price' : self.price,
                'state' : 'offerAccepted'
            })
            self.status = 'accepted'

    def action_refused_offer(self):
        if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.write({
                'selling_price' : 0,
                'state' : 'offerReceived'
            })
            self.status = 'refused'


    def _validate_accepted_offer(self):
        offer_ids = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted')
        ])
        if offer_ids:
            raise ValidationError("You have an accepted offer already")

    @api.model_create_multi
    def create(self, values):
        for record in values:
            if not record.get('offer_date'):
                record['offer_date'] = fields.Date.today()
        return super(PropertyOffer, self).create(values)

    @api.constrains('validity')
    def _check_validity(self):
        for record in self:
            if record.deadline <= record.offer_date:
                raise ValidationError(("Deadline cannot be less than Offer Date"))

    @api.depends('property_id','partner_id')
    def _compute_offer_name(self):
        for record in self:
            if record.property_id and record.partner_id:
                record.name = f"{record.property_id.name} - {record.partner_id.name}"
            else:
                record.name = False



    def extend_offer_deadline(self):
        active_ids = self._context.get('active_ids',[])
        if active_ids:
            # record set
            offer_ids = self.env['estate.property.offer'].browse(active_ids)
            # loop
            for offer in offer_ids:
                offer.validity = 10


    def _extend_offer_deadline(self):
        offer_ids = self.env['estate.property.offer'].search([])
        for offer in offer_ids:
            offer.validity += 1