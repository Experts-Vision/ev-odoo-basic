import { Component } from '@odoo/owl'
import { registry } from '@web/core/registry'
import { xml } from '@odoo/owl'
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";


class FinancialReport extends Component {
    static template = "base_accounting_kit.financial_report_template"
    static components = {
        Layout
    }

    setup() {
        this.context = this.props.action.context;
        this.action = useService("action")
        this.orm = useService("orm")

        
    }

    async print() {
        const data = this.context.data.data;
        if (!data) {
            console.error("No data available for printing");
            return;
        }
        
        try {
            const reportAction = await this.orm.call(
                "financial.report",
                "get_report_action",
                [data]
            );
            
            if (reportAction) {
                this.action.doAction(reportAction);
            }
        } catch (error) {
            console.error("Error printing report:", error);
        }
    }

    async xlsx() {
        const data = this.context.data.data;
        if (!data) {
            console.error("No data available for export");
            return;
        }
        
        data.form.debit_credit = false;
        try {
            const reportAction = await this.orm.call(
                "financial.report",
                "get_xlsx_action",
                [data]
            );
            
            if (reportAction) {
                this.action.doAction(reportAction);
            }
        } catch (error) {
            console.error("Error exporting to XLSX:", error);
        }
    }
}



registry.category("actions").add("base_accounting_kit.financial_report_action", FinancialReport);