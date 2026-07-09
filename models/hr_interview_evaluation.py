from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrInterviewEvaluation(models.Model):
    _name = "hr.interview.evaluation"
    _rec_name = "name"
    _description = "Interview Evaluation"
    _order = "interview_date desc"

    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        default="New",
        readonly=True,
    )

    applicant_id = fields.Many2one(
        "hr.applicant",
        string="Candidate",
        index=True,
        required=True,
        ondelete="restrict",
        help="Candidate being evaluated.",
    )

    interviewer_id = fields.Many2one(
        "hr.employee",
        string="Interviewer",
        index=True,
        required=True,
        ondelete="restrict",
        help="Employee conducting the interview.",
    )

    interview_date = fields.Datetime(
        string="Interview Date",
        index=True,
        required=True,
        default=fields.Datetime.now,
        help="Scheduled interview date.",
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        readonly=True,
        copy=False,
        help="Current interview evaluation status.",
    )

    recommendation = fields.Selection(
        [
            ("strong_hire", "Strong Hire"),
            ("hire", "Hire"),
            ("no_hire", "No Hire"),
            ("strong_no_hire", "Strong No Hire"),
        ],
        string="Recommendation",
        compute="_compute_recommendation",
        store=True,
        readonly=True,
        copy=False,
        help="Automatically calculated based on total score.",
    )

    total_score = fields.Float(
        string="Total Score",
        compute="_compute_total_score",
        store=True,
        readonly=True,
        copy=False,
        digits=(16, 2),
        help="Overall weighted interview score.",
    )

    evaluation_line_ids = fields.One2many(
        "hr.interview.evaluation.line",
        "evaluation_id",
        string="Evaluation Lines",
        help="Evaluation criteria and interviewer scores.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        """
        Create interview evaluation and generate evaluation lines
        from active evaluation criteria.
        """
        self.env["hr.evaluation.criteria"]._check_total_active_weight()
        for vals in vals_list:
            if not vals.get("name") or vals.get("name") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("hr.interview.evaluation")
                    or "New"
                )

        records = super().create(vals_list)

        criteria = self.env["hr.evaluation.criteria"].search(
            [("active", "=", True)],
            order="sequence",
        )

        for record in records:
            lines = [(0, 0, {"criteria_id": criterion.id}) for criterion in criteria]
            if lines:
                record.evaluation_line_ids = lines
        return records

    @api.constrains("interview_date")
    def _check_interview_date(self):
        """
        Prevent interview date from being earlier than today.
        """
        today = fields.Date.context_today(self)

        for rec in self:
            if rec.interview_date and rec.interview_date.date() < today:
                raise ValidationError("Interview date cannot be earlier than today.")

    @api.depends(
        "evaluation_line_ids.weighted_score",
        "evaluation_line_ids.score",
    )
    def _compute_total_score(self):
        for rec in self:
            rec.total_score = sum(rec.evaluation_line_ids.mapped("weighted_score"))

    @api.depends("total_score")
    def _compute_recommendation(self):
        for rec in self:
            if rec.total_score >= 90:
                rec.recommendation = "strong_hire"
            elif rec.total_score >= 75:
                rec.recommendation = "hire"
            elif rec.total_score >= 60:
                rec.recommendation = "no_hire"
            else:
                rec.recommendation = "strong_no_hire"

    def action_start(self):
        for rec in self:
            if rec.state != "draft":
                raise ValidationError("Only draft interviews can be started.")

            rec.state = "in_progress"

    def action_done(self):
        """
        Complete the interview after validating all evaluation scores.
        """
        for rec in self:

            if not rec.evaluation_line_ids:
                raise ValidationError("Please add at least one evaluation criteria.")

            for line in rec.evaluation_line_ids:
                if not line.score:
                    raise ValidationError(
                        f"Please select a score for '{line.criteria_id.name}'."
                    )

            rec.state = "done"

    def action_cancel(self):
        for rec in self:
            if rec.state in ("done", "cancelled"):
                raise ValidationError("This interview cannot be cancelled.")

            rec.state = "cancelled"

    def action_draft(self):
        for rec in self:
            if rec.state != "cancelled":
                raise ValidationError(
                    "Only cancelled interviews can be reset to draft."
                )

            rec.state = "draft"

    def write(self, vals):
        """
        Prevent modification of completed interview evaluations.
        """
        protected_fields = {
            "applicant_id",
            "interviewer_id",
            "interview_date",
            "evaluation_line_ids",
        }

        for rec in self:
            if rec.state == "done":
                if protected_fields.intersection(vals.keys()):
                    raise ValidationError(
                        "Completed interview evaluations cannot be modified."
                    )

        return super().write(vals)

    def unlink(self):
        """
        Prevent deletion of completed interview evaluations.
        """
        for rec in self:
            if rec.state == "done":
                raise ValidationError("Completed interviews cannot be deleted.")
        return super().unlink()
