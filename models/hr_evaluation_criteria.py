from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrEvaluationCriteria(models.Model):
    _name = "hr.evaluation.criteria"
    _description = "Interview Evaluation Criteria"
    _rec_name = "name"
    _order = "sequence, id"

    _sql_constraints = [
        (
            "unique_criteria_name",
            "unique(name)",
            "Criteria name must be unique.",
        ),
        (
            "check_weight_positive",
            "CHECK(weight > 0)",
            "Weight must be greater than zero.",
        ),
    ]

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )

    name = fields.Char(
        string="Criteria",
        required=True,
    )

    weight = fields.Float(
        string="Weight (%)",
        digits=(16, 2),
        default=10.0,
        help="Percentage weight of this evaluation criteria.",
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )

    @api.constrains("weight")
    def _check_weight(self):
        for rec in self:
            if rec.weight <= 0:
                raise ValidationError("Weight must be greater than zero.")

    def _check_total_active_weight(self):
        """

        Ensure the total weight of all active evaluation criteria equals 100%.

        """
        active_criteria = self.search(
            [
                ("active", "=", True),
            ]
        )

        total_weight = sum(active_criteria.mapped("weight"))

        if round(total_weight, 2) != 100.0:
            raise ValidationError(
                "The total weight of all active evaluation criteria must be exactly 100%.\n\n"
                f"Current total weight: {total_weight:.2f}%."
            )
