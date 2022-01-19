from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.tools.translate import _

class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['base.archive']
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
            ('borrowed', 'Borrowed'),
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

    ref_doc_id = fields.Reference(
        selection = '_referencable_models',
        string = 'Reference Document'
    )

    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([
            ('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]

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

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [
            ('draft', 'available'),
            ('available', 'borrowed'),
            ('borrowed', 'available'),
            ('available', 'lost'),
            ('borrowed', 'lost'),
            ('lost', 'available')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for record in self:
            if record.is_allowed_transition(record.state, new_state):
                record.state = new_state
            else:
                msg = "Moving from %s to %s is not allowed" %(record.state, new_state)
                raise UserError(msg)

    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.change_state('lost')

    def log_all_library_members(self):
        library_member_model = self.env['library.member']
        all_members = library_member_model.search([])
        print('ALL MEMBERS : ', all_members)
        return True

    def change_update_date(self):
        self.ensure_one()
        self.date_update = fields.Date.today()

    def find_book(self):
        domain = [
            '|',
                '&',('name', 'ilike', 'Book Name'),
                    ('category_id.name', 'ilike', 'Category Name'),
                '&',('name', 'ilike', 'Book Name 2'),
                    ('category_id.name', 'ilike', 'Category Name 2')
        ]
        books = self.search(domain)
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        logger.info('Books found : %s', books)
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        return True
