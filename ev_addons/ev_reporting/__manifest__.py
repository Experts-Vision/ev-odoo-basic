{
    "name": "EV Reporting",
    "version": "18.0.1.0.0",
    "category": "Theme",
    "summary": "EV Reporting",
    "description": """
        This Provide A custom Reporting For EV
    """,
    "author": "Experts Vision Company",
    "website": "https://expertsvision.org",
    "depends": ["base", "purchase"],
    "data": [
        "reports/test.xml",
        "reports/report_action.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "ev_reporting/static/src/scss/report.scss",
        ],
          "web.report_assets_pdf": [
        "ev_reporting/static/src/scss/report.scss"
    ],
    },
    "demo": [],
    "application": False,
    "license": "AGPL-3",
    "images": [],
    "support": "support@expertsvision.org",
    'installable': True,
}
