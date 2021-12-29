from odoo import models, fields, api
from datetime import timedelta

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = "Library Book"
    _order = 'date_release desc, name'
    _rec_name = 'short_name'
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)','Book title must be unique.'),
        ('positve_page', 'CHECK (pages>0)','Number of pages must be positive.')]

    short_name = fields.Char('Short Title',
        translate=True,
        index=True)

    name = fields.Char('Title', required=True)
    date_release = fields.Date(string="Rlease Date")

    author_ids = fields.Many2many('res.partner', string="Author")

    publisher_id = fields.Many2one(
        string="Publisher",
        comodel_name="res.partner",
        domain=[],
        context={},
        ondelete="set null")

    cost_price = fields.Float("Book Cost", digits='Book Price')

    currency_id = fields.Many2one(string="Currency",
        comodel_name="res.currency")

    retail_price = fields.Monetary(
        string = 'Retail Price'
        # optional: currency_field='currency_id',
        )

    notes = fields.Text("Internal Notes")
    state = fields.Selection(
        string="State",
        selection=[
            ('draft', 'Not Available'),
            ('available', 'Available'),
            ('lost', 'Lost')],
        default='draft')

    description = fields.Html('Description',
        sanitize=True,
        strip_style=False)

    cover = fields.Binary("Book cover")
    out_of_print = fields.Boolean("Out Of Print?")
    date_update = fields.Date("Last Updated")

    pages = fields.Integer("Number of Pages",
        groups='base.group_user',
        states={'lost': [('readonly',True)]},
        help='Total book page count',
        company_dependent=False)

    age_days = fields.Float(
        string="Days since release",
        compute='_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=False,        #optional
        compute_sudo=True)  #optional

    reader_rating = fields.Float("Reader average rating", digits=(14, 2))
    category_id = fields.Many2one('library.book.categ')

    publisher_city = fields.Char(
        'Publisher City',
        related = 'publisher_id.city',
        readonly = True)

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release>fields.date.today():
                raise models.ValidationError('Relase date must be in the past')
    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self:
            if book.date_release:
                delta = today - book.date_release
                book.age_days = delta.days
            else:
                book.age_days = 0

    def _inverse_age(self):
        today = fields.Date.today()
        for book in self.filtered('date_release'):
            d = today - timedelta(days=book.age_days)
        book.date_release = d

    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
        operator_map = {
            '>' : '<', '>=' : '<=',
            '<' : '>', '<=' : '>='
        }
        new_op = operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]

    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s. ($%s)" % (record.name, record.retail_price)
            result.append((record.id, rec_name))
        return result
