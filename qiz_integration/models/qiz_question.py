from odoo import models, fields

class QizQuestion(models.Model):
    _name = 'qiz.question'
    _description = 'Qiz Template Question'
    _order = 'sequence, id'

    template_id = fields.Many2one('qiz.template', string='Template', required=True, ondelete='cascade')
    qiz_question_id = fields.Char(string='Qiz Question ID', readonly=True)
    sequence = fields.Integer(string='Sequence', default=10) # For ordering

    text = fields.Text(string='Question Text', readonly=True)
    type = fields.Char(string='Question Type (Qiz)', readonly=True) # Store original Qiz type

    # Aggregated Results
    total_responses_for_question = fields.Integer(string='Responses to this Question', readonly=True)

    # For Numeric types
    avg_numeric_value = fields.Float(string='Average Value', readonly=True, digits=(16, 2))
    min_numeric_value = fields.Float(string='Min Value', readonly=True, digits=(16, 2))
    max_numeric_value = fields.Float(string='Max Value', readonly=True, digits=(16, 2))

    # For Text/Choice types (store as JSON string or use more structured approach if needed)
    popular_answers_summary = fields.Text(string='Popular Answers Summary', readonly=True)

    # For Boolean type
    true_count = fields.Integer(string='True Count', readonly=True)
    false_count = fields.Integer(string='False Count', readonly=True)

    # You might add a computed field to display aggregated results nicely
    # display_aggregated_result = fields.Text(string="Aggregated Result", compute='_compute_display_aggregated_result')
    # def _compute_display_aggregated_result(self):
    #     for rec in self:
    #         parts = []
    #         if rec.type in ['RATING', 'NUMBER_INPUT'] and rec.avg_numeric_value is not None:
    #             parts.append(f"Avg: {rec.avg_numeric_value}, Min: {rec.min_numeric_value}, Max: {rec.max_numeric_value}")
    #         if rec.popular_answers_summary:
    #             parts.append(f"Popular: {rec.popular_answers_summary}")
    #         if rec.type == 'BOOLEAN':
    #             parts.append(f"True: {rec.true_count}, False: {rec.false_count}")
    #         rec.display_aggregated_result = "; ".join(parts) if parts else "No aggregated data"

