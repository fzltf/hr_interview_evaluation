{
    "name": "HR Interview Evaluation",
    "version": "19.0.1.0.0",
    "summary": "Interview Evaluation for Recruitment",
    
    "description": """
    HR Interview Evaluation
    ========================

    Structured interview evaluation for Odoo Recruitment with weighted scoring,
    automated hiring recommendations, workflow management, and Recruitment integration.

    Main Features:
    - Configurable weighted evaluation criteria
    - Automatic score calculation
    - Automatic hiring recommendations
    - Interview workflow
    - Smart Button on Recruitment Applicant
    - Auto-generated interview references
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