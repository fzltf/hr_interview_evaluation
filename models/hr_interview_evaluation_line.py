from odoo import api, fields, models


class HrInterviewEvaluationLine(models.Model):

    _name = "hr.interview.evaluation.line"
    # _rec_name = "criteria_id"
    _description = "Interview Evaluation Line"
    _order = "sequence, id"

    _sql_constraints = [
        (
            "unique_evaluation_criteria",
            "unique(evaluation_id, criteria_id)",
            "Each evaluation criteria can only be added once.",
        ),
    ]

    sequence = fields.Integer(
        related="criteria_id.sequence",
        store=True,
        readonly=True,
    )

    evaluation_id = fields.Many2one(
        "hr.interview.evaluation",
        string="Interview Evaluation",
        required=True,
        ondelete="cascade",
    )

    criteria_id = fields.Many2one(
        "hr.evaluation.criteria",
        string="Criteria",
        required=True,
        help="Select the evaluation criterion.",
    )

    weight = fields.Float(
        string="Weight (%)",
        related="criteria_id.weight",
        store=True,
        readonly=True,
        digits=(16, 2),
        help="Weight percentage inherited from the evaluation criterion.",
    )

    score = fields.Selection(
        [
            ("1", "1 - Poor"),
            ("2", "2 - Fair"),
            ("3", "3 - Good"),
            ("4", "4 - Very Good"),
            ("5", "5 - Excellent"),
        ],
        string="Score",
        help="Score given by interviewer.",
    )

    weighted_score = fields.Float(
        string="Weighted Score",
        compute="_compute_weighted_score",
        store=True,
        readonly=True,
        digits=(16, 2),
        help="Automatically calculated weighted score.",
    )

    notes = fields.Text(
        string="Notes",
        help="Interviewer comments for this evaluation criterion.",
    )

    @api.depends("score", "weight")
    def _compute_weighted_score(self):
        for line in self:
            if line.score:
                line.weighted_score = (float(line.score) / 5.0) * line.weight
            else:
                line.weighted_score = 0.0
