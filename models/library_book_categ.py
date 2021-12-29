from odoo import fields, models, api
from odoo.exceptions import ValidationError

class BookCategory(models.Model):
    _name = 'library.book.categ'
    _description = "Book Categories"
    _parent_store = True
    _parent_name = "parent_id"

    parent_path = fields.Char(index=True)

    name = fields.Char(string="Category")
    parent_id = fields.Many2one(
        string="Parent Category",
        comodel_name="library.book.categ",
        ondelete="restrict",
        index=True)

    child_ids = fields.One2many(
        string="Child Category",
        comodel_name="library.book.categ",
        inverse_name="parent_id")

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError(
                'Error! You cannot create recursive categories.')
