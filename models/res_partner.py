from odoo import models, fields, api

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

    count_books = fields.Integer(
        string="Number Of Authered Books",
        compute = '_compute_count_books')

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for record in self:
            record.count_books = len(record.authored_book_ids)
