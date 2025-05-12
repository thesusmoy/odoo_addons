from odoo import models, fields, api

class QizTemplate(models.Model):
    _name = 'qiz.template'
    _description = 'Qiz Form Template'
    _order = 'name'

    name = fields.Char(string='Title', required=True)
    qiz_template_id = fields.Char(string='Qiz Template ID', required=True, index=True, readonly=True)
    author_name = fields.Char(string='Author Name', readonly=True)
    author_email = fields.Char(string='Author Email', readonly=True)
    description = fields.Text(string='Description', readonly=True)

    question_ids = fields.One2many('qiz.question', 'template_id', string='Questions', readonly=True)

    last_imported_date = fields.Datetime(string='Last Imported', readonly=True)
    total_responses_qiz = fields.Integer(string='Total Responses (from Qiz)', readonly=True)

    _sql_constraints = [
        ('qiz_template_id_unique', 'unique(qiz_template_id)', 'Qiz Template ID must be unique!')
    ]

    def view_qiz_template_details(self):
        
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current', 
        }
