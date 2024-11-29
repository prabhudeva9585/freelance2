/** @odoo-module */

import { AccountReport } from "@account_reports/components/account_report/account_report";
import { AccountReportFilters } from "@account_reports/components/account_report/filters/filters";

export class search_template_custom extends AccountReportFilters {
    static template = "l10n_ve_account_reports_dual.search_template_custom";

    handleCurrencySelection(currency) {
        let currencies = this.controller.options['currencies']
        const currencyIds = this.controller.options['currencies'].map(currency => currency.id);
        let switch_currency = 0
        for (let i = 0; i < currencyIds.length; i++) {
            if (this.controller.options['selected_currency'] !=currencyIds[i] ){

                switch_currency =currencyIds[i]
            }
        }
        this.controller.options['selected_currency'] = switch_currency
        this.toggleFilter('currencies.' + currencies[1].id + '.selected');
    }
}

AccountReport.registerCustomComponent(search_template_custom);
