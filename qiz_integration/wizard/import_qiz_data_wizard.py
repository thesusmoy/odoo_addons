
import requests 
import json
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class ImportQizDataWizard(models.TransientModel):
    _name = 'import.qiz.data.wizard'
    _description = 'Import Qiz Data Wizard'

    api_token = fields.Char(string='Qiz API Token', required=True)
    
    QIZ_API_BASE_URL = 'https://qiz-beta.com/api/v1'

    def _get_headers(self):
        if not self.api_token:
            raise UserError(_("API Token is required."))
        return {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
        }

    def action_import_data(self):
        self.ensure_one()
        headers = self._get_headers()

        templates_url = f"{self.QIZ_API_BASE_URL}/me/templates"
        try:
            response = requests.get(templates_url, headers=headers, timeout=30)
            response.raise_for_status()
            qiz_templates_data = response.json()
        except requests.exceptions.RequestException as e:
            raise UserError(_("Failed to fetch templates from Qiz API: %s") % str(e))
        except json.JSONDecodeError:
            raise UserError(_("Received invalid JSON response when fetching templates."))

        if not qiz_templates_data:
            
            return {'type': 'ir.actions.client', 'tag': 'display_notification', 'params': {
                'title': _('No Templates Found'),
                'message': _('No templates were found for the provided API token.'),
                'sticky': False,
                'type': 'info',
            }}

        template_model = self.env['qiz.template']
        question_model = self.env['qiz.question']
        imported_count = 0
        updated_count = 0

        for qiz_template_info in qiz_templates_data:
            qiz_template_id = qiz_template_info.get('id')
            if not qiz_template_id:
                
                continue

            results_url = f"{self.QIZ_API_BASE_URL}/templates/{qiz_template_id}/aggregated-results"
            try:
                res_response = requests.get(results_url, headers=headers, timeout=60)
                res_response.raise_for_status()
                qiz_results_data = res_response.json()
            except requests.exceptions.RequestException as e:
                
                self.env.cr.commit()
                _logger.error(f"Failed to fetch results for template {qiz_template_id}: {e}")
                continue 
            except json.JSONDecodeError:
                _logger.error(f"Invalid JSON for template results {qiz_template_id}")
                continue


            template_vals = {
                'name': qiz_results_data.get('templateTitle'),
                'qiz_template_id': qiz_template_id,
                'author_name': qiz_results_data.get('author', {}).get('name'),
                'author_email': qiz_results_data.get('author', {}).get('email'),
                'description': qiz_template_info.get('description'), 
                'last_imported_date': datetime.now(),
                'total_responses_qiz': qiz_results_data.get('totalResponses', 0),
            }

            existing_template = template_model.search([('qiz_template_id', '=', qiz_template_id)], limit=1)

            current_template = None
            if existing_template:
                existing_template.write(template_vals)
                current_template = existing_template
                updated_count += 1
                
                current_template.question_ids.unlink() 
            else:
                current_template = template_model.create(template_vals)
                imported_count += 1

            
            q_sequence = 10
            for q_data in qiz_results_data.get('questions', []):
                question_vals = {
                    'template_id': current_template.id,
                    'qiz_question_id': q_data.get('questionId'),
                    'text': q_data.get('text'),
                    'type': q_data.get('type'),
                    'sequence': q_sequence,
                    'total_responses_for_question': q_data.get('totalResponsesForQuestion', 0),
                    'avg_numeric_value': q_data.get('average'),
                    'min_numeric_value': q_data.get('min'),
                    'max_numeric_value': q_data.get('max'),
                    'true_count': q_data.get('trueCount'),
                    'false_count': q_data.get('falseCount'),
                }

                pop_answers = q_data.get('popularAnswers')
                if pop_answers:
                    
                    summary_parts = [f"{pa['answer']} ({pa['count']})" for pa in pop_answers]
                    question_vals['popular_answers_summary'] = "; ".join(summary_parts)

                question_model.create(question_vals)
                q_sequence += 10


        message = _("%s templates imported, %s templates updated.") % (imported_count, updated_count)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Import Successful'),
                'message': message,
                'sticky': False, 
                'type': 'success', 
                'next': {'type': 'ir.actions.act_window_close'}, 
            }
        }

