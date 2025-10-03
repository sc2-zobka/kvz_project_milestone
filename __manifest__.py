# -*- coding: utf-8 -*-
{
    'name': "kvz_project_milestone",
    'version': '17.0.1.0.0',
    'category': 'Project',
    'summary': 'Extended milestone management for project managers',
    'description': """
        Project Milestones Manager
        ==========================
        - Custom milestone view filtered by project manager
        - Efficient access control with record rules
        - Full CRUD operations for project managers
    """,
    'author': "Kuvasz Solutions",
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'project',
    ],
    'data': [
        # Security
        # 'security/ir.model.access.csv',
        
        # Views
        'views/project_milestone_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
