# -*- coding: utf-8 -*-

from odoo import models


class PurchaseOrderReport(models.AbstractModel):
    _name = 'report.ev_reporting.custom_po_report'
    _description = 'Custom Purchase Order Report'

    # def _get_report_values(self, docids, data=None):
    #     """Generate report values"""
    #     docs = self.env['purchase.order'].browse(docids)
        
    #     # Helper function for translations in template
    #     def translate(text):
    #         return self.env._(text)
        
    #     return {
    #         'doc_ids': docids,
    #         'doc_model': 'purchase.order',
    #         'docs': docs,
    #         '_': translate,
    #     }

