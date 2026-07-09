from odoo import api, fields, models


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    interview_evaluation_count = fields.Integer(
        compute="_compute_interview_evaluation_count"
    )

    def _compute_interview_evaluation_count(self):
        evaluation = self.env["hr.interview.evaluation"]

        for applicant in self:
            applicant.interview_evaluation_count = evaluation.search_count(
                [("applicant_id", "=", applicant.id)]
            )

    def action_view_interview_evaluations(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Interview Evaluations",
            "res_model": "hr.interview.evaluation",
            "view_mode": "list,form",
            "domain": [("applicant_id", "=", self.id)],
            "context": {
                "default_applicant_id": self.id,
            },
        }
