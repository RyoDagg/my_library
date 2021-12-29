from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book_ids = fields.One2many(
        string="Published Books",
        comodel_name="library.book",
        inverse_name="publisher_id")

    authored_book_ids = fields.Many2many('library.book',
        string='Authered Books',
        #relation = '$relation_name'
        )
