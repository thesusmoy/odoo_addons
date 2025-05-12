from odoo import models, fields

class QizQuestion(models.Model):
    _name = 'qiz.question'
    _description = 'Qiz Template Question'
    _order = 'sequence, id'

    template_id = fields.Many2one('qiz.template', string='Template', required=True, ondelete='cascade')
    qiz_question_id = fields.Char(string='Qiz Question ID', readonly=True)
    sequence = fields.Integer(string='Sequence', default=10) 

    text = fields.Text(string='Question Text', readonly=True)
    type = fields.Char(string='Question Type (Qiz)', readonly=True) 

    total_responses_for_question = fields.Integer(string='Responses to this Question', readonly=True)

    avg_numeric_value = fields.Float(string='Average Value', readonly=True, digits=(16, 2))
    min_numeric_value = fields.Float(string='Min Value', readonly=True, digits=(16, 2))
    max_numeric_value = fields.Float(string='Max Value', readonly=True, digits=(16, 2))

    popular_answers_summary = fields.Text(string='Popular Answers Summary', readonly=True)


    true_count = fields.Integer(string='True Count', readonly=True)
    false_count = fields.Integer(string='False Count', readonly=True)
