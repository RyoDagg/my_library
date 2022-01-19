from odoo import fields, models

class BaseArchive(models.AbstractModel):
    _name  = 'base.archive'
    active = fields.Boolean()

    def do_archive(self):
        for record in self:
            record.active = not record.active
