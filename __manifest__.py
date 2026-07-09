{
    "name": "HR Interview Evaluation",
    "version": "19.0.1.0.0",
    "summary": "Interview Evaluation for Recruitment",
    
    "description": """
    HR Interview Evaluation
    ========================

    Structured interview evaluation for the recruitment process, with weighted
    scoring criteria and automatic hiring recommendations.

    Key Features
    -------------
    * Configure reusable evaluation criteria with a percentage weight each (active criteria weights must always total exactly 100%).
    * Create an Interview Evaluation per applicant/interviewer, with evaluation lines auto-generated from all active criteria.
    * Interviewers score each criterion (1-5), and the weighted score per line and the overall total score are computed automatically.
    * Automatic hiring recommendation (Strong Hire / Hire / No Hire / Strong No Hire) based on the total score.
    * Interview workflow: Draft → In Progress → Done, with Cancel and Reset to Draft actions.
    * Completed (Done) evaluations are locked: key fields cannot be edited and the record cannot be deleted.
    * Auto-numbered reference (e.g. INT00001) via a dedicated sequence.
    * Smart button on the Applicant form to quickly access related interview evaluations.
    """,
    
    "author": "Fauza Lutfia",
    "website": "https://github.com/fzltf/hr_interview_evaluation",
    "category": "Human Resources",
    "license": "LGPL-3",
    "images": [
        "static/description/icon.png"
    ],
    "depends": [
        "hr",
        "hr_recruitment"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/interview_sequence.xml",

        "views/hr_evaluation_criteria_views.xml",
        "views/hr_interview_evaluation_views.xml",
        "views/hr_applicant_views.xml",

        "views/menu_views.xml",
        
    ],
    "installable": True,
    "application": True,

}