from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError


#23 11:56

#wizard and generic models
#abstract, Transient, Regular

# class AbstractOffer(models.AbstractModel):
#     _name = 'abstract.model.offer'
#     _description = 'Abstract offers'

#     partner_email = fields.Char(string="Email")
#     partner_phone = fields.Char(string="Phone Number")

#class TransientOffer(models.TransientModel):
    # _name = 'transient.model.offer'
    # _description = 'transient offers'
    # #_transient_max_hours = 2.0

    # @api.autovacuum
    # def _transient_vacuum(self):
    #     pass

    # partner_email = fields.Char(string="Email")
    # partner_phone = fields.Char(string="Phone Number")

#modelus
 
class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    #_inherit = ['abstract.model.offer'] 
    _description = 'Estate Properties Offers'

    price = fields.Float(string="Price")
    status = fields.Selection(
        [('accepted', 'Accepted'), ('denied', 'Denied')],
        string="Status")
    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer(string="Validity")
    deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadline')
    creation_date = fields.Date(string="Create Date")

    #operatus_modulus


    #print test des variables
        #@api.depends_context('uid')
        #print(self._context)
        #print(self.env.context)

    #sql constraints
    _sql_constraints = [
        ('check_validity', 'check(validity > 0)', 'Deadline cannot be before creation date')
    ]

    # @api.model
    # def _set_create_date(self):
    #     return fields.Date.today()
    
    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False
    
    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if not rec.get('creation_date'):
                rec['creation_date'] = fields.Date.today()
            return super(PropertyOffer, self).create(vals)

    def action_accept_offer(self):
        if self.property_id:
            self._validate_accepted_offer()
            self.property_id.write({
                'selling_price': self.price,
                'state': 'accepted'
            })
        self.status = 'accepted'

#use sql instead
    # @api.constrains('validity')
    # def _check_validity(self):
    #     for rec in self:
    #         if rec.deadline and rec.creation_date:
    #             if rec.deadline <= rec.creation_date:
    #                 raise ValidationError("Deadline cannot be before creation date")
    #         elif rec.deadline is None or rec.creation_date is None:
    #             pass

    #it would print in the console if it was possible to see it
    # def write(self, vals):
    #     print(vals)
    #     res_partner_ids = self.env['res.partner'].search([
    #         # ('is_company', '=', True),
    #         ('name', '=', vals.get('name'))
    #     ])
    #     #.mapped('phone')
    #     print(res_partner_ids.name)
    #     return super(PropertyOffer, self).write(vals)


    # def write(self, vals):    see 24
    #     res_partner_ids = self.envp['res.partner'].search([
    #         ('is_company', '=', True),
    #     ]).unlink()
    #     print(res_partner_ids)
    #     return super(PropertyOffer, self).write(vals)