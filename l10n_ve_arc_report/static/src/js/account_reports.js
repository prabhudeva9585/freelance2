/** @odoo-module **/

import { WarningDialog } from "@web/core/errors/error_dialogs";
import { Many2OneField, many2OneField } from '@web/views/fields/many2one/many2one_field';
import { DateTimeField } from "@web/views/fields/datetime/datetime_field";
// import { _t, qweb as QWeb } from "web.core";
import { _t } from "@web/core/l10n/translation";

import { Component, onWillStart } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { AccountReport } from "@account_reports/components/account_report/account_report";


class M2OFilters extends Component {
    setup() {
        this.fields = this.props.fields;
        this.widgets = {};
        this.model = this.env.model; // Access model through `env` in Odoo 17
    }

    async willStart() {
        const defs = [];
        for (const [fieldName, fieldInfo] of Object.entries(this.fields)) { 
            defs.push(this._makeM2OWidget(fieldInfo, fieldName));
        }
        await Promise.all(defs);
    }

    async _makeM2OWidget(fieldInfo, fieldName) {
        const options = {
            [fieldName]: { options: { no_create: true, no_open: true } },
        };
        const record = await this.model.makeRecord(fieldInfo.modelName, [
            {
                name: fieldName,
                relation: fieldInfo.modelName,
                type: "many2one",
                value: fieldInfo.value.id,
                domain: fieldInfo.domain,
            },
        ]);
        this.widgets[fieldName] = new Many2OneField(null, {
            fieldName,
            record,
            mode: "edit",
        });
    }

    async start() {
        const content = QWeb.render("m2oWidgetTable", { fields: this.fields });
        this.el.append(content);
        for (const [fieldName, field] of Object.entries(this.fields)) {
            const fieldWidget = this.widgets[fieldName];
            fieldWidget.mount(this.el.querySelector(`#${fieldName}_field`));
        }
    }

    _confirmChange() {
        const data = {};
        for (const [fieldName, filter] of Object.entries(this.fields)) {
            const widgetValue = this.widgets[fieldName].value;
            if (widgetValue) {
                data[fieldName] = {
                    id: widgetValue.data.id,
                    name: widgetValue.data.display_name,
                };
            }
        }
        this.trigger("m2o_changed", { data });
    }
}

class YearPicker extends DateTimeField {
    setup() {
        this.options = {
            locale: moment.locale(),
            viewMode: "years",
            format: "YYYY",
            minDate: moment({ y: 1000 }),
            maxDate: moment({ y: 9999 }),
            widgetParent: "body",
        };
    }
}

// patch(AccountReport.prototype, "account_report_m2o_patch", {
//     async renderSearchViewButtons() {
//         await this._super.apply(this, arguments);

//         // Year Filter
//         const yearpickers = this.el.querySelectorAll(".js_account_reports_yearpicker");
//         yearpickers.forEach((el) => {
//             const name = el.querySelector("input").getAttribute("name");
//             const defaultValue = el.dataset.defaultValue;
//             const dt = new YearPicker();
//             dt.mount(el).then(() => {
//                 const input = dt.el.querySelector("input");
//                 input.setAttribute("name", name);
//                 if (defaultValue) {
//                     dt.setValue(moment({ y: defaultValue }));
//                 }
//             });
//         });

//         this.el.querySelector(".js_account_report_year_filter").addEventListener("click", (e) => {
//             const year = this.el.querySelector('.o_datepicker_input[name="year"]');
//             const error = year.value === "";
//             if (error) {
//                 new WarningDialog(this, {
//                     title: _t("Odoo Warning"),
//                 }, {
//                     message: _t("Date cannot be empty"),
//                 }).open();
//             } else {
//                 this.report_options.year = parseInt(year.value);
//                 this.reload();
//             }
//         });

//         // Many2One Filter
//         if ("partner_id" in this.report_options) {
//             if (!this.partner_m2o_filter) {
//                 this.partner_m2o_filter = new M2OFilters(this, {
//                     partner_id: {
//                         label: "Proveedor",
//                         modelName: "res.partner",
//                         value: this.report_options.partner_id,
//                         domain: [["partner_type", "in", ["supplier", "customer_supplier"]]],
//                     },
//                 });
//                 this.partner_m2o_filter.mount(this.el.querySelector(".js_m2o_filters"));
//             } else {
//                 this.el.querySelector(".js_m2o_filters").append(this.partner_m2o_filter.el);
//             }
//         }
//     },
// });
