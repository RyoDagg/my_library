from odoo import fields, models, api
from odoo.exceptions import ValidationError

class BookCategory(models.Model):
    _name = 'library.book.categ'
    _description = "Book Categories"
    _parent_store = True
    _parent_name = "parent_id"

    parent_path = fields.Char(index=True)

    name = fields.Char(string="Category")
    description = fields.Text(string="Description")

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

    def create_categories(self):
        categ1 = {
            'name' : 'Child Category 1',
            'description' : 'jsqdhfjh jshf @1'
        }
        categ2 = {
            'name' : 'Child Category 2',
            'description' : 'jsqdhfjh jshf @2'
        }

        parent_categ_val = {
            'name' : 'Parent Category',
            'description' : 'PPPPPPPPPPPPPPPPPPPP',
            'child_ids' : [
                (0, 0, categ1),
                (0, 0, categ2)
            ]
        }
        record = self.env['library.book.categ'].create(parent_categ_val)
