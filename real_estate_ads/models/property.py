from odoo import fields, models, api
 
class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate Properties'

    name = fields.Char(string="Name", required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
        ('cancel', 'Cancelled')
    ], default='new', string='Status')
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")
    description = fields.Text(string="description")
    postcode = fields.Char(string="postcode")
    date_availability = fields.Date(string="Available from", readonly=True)
    expected_price = fields.Float(string="Expected Price")
    best_offer = fields.Float(string="Best Offer")
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms")
    Living_Area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    Garage = fields.Boolean(string="Garage", default=False)
    Garden = fields.Boolean(string="Garden", default=False)
    Garden_area = fields.Integer(string="Garden Area (sqm)")
    Garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation", default='north')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    sales_id = fields.Many2one('res.users', string="Salesman")
    buyer_id = fields.Many2one('res.partner', string="Buyer", domain=[('is_company', '=', True)])
    phone = fields.Char(string="Phone", related='buyer_id.phone')

    @api.depends('Living_Area', 'Garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.Living_Area + rec.Garden_area


    total_area = fields.Integer(string="Total Area", compute=_compute_total_area)
    

#id, create_date, create_uid, write_date, write_uid 

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'

    name = fields.Char(string="Name", required=True)

    def action_accept(self):
        self.state = 'sold'

    def action_refuse(self):
        self.state = 'cancel'

class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Tag'

    name = fields.Char(string="Name", required=True)