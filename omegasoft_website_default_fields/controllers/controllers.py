# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import re

identification_id_regex = re.compile(r'^[JGVEP][0-9]{8}$')


class WebsiteSaleInherit(WebsiteSale):
    def _checkout_form_save(self, mode, checkout, all_values):
        # Campos obligatorios que no están en el formulario del website
        if mode[0] == 'new':
            checkout['person_type_id'] = request.env['person.type'].search([('code','=','PNRE')]).id
            checkout['identification'] = checkout.get('vat')
            checkout['partner_type'] = 'customer'
        
        # Llama al método original para mantener la funcionalidad base
        res = super(WebsiteSaleInherit, self)._checkout_form_save(mode, checkout, all_values)
        return res

    def checkout_form_validate(self, mode, all_form_values, data):
        if request.env.user._is_public():
            all_form_values['field_required'] += ',vat'
        error, error_message = super().checkout_form_validate(mode, all_form_values, data)
        if all_form_values.get('vat') and\
        not identification_id_regex.match(all_form_values.get('vat')):
            error['vat'] = 'missing'
            error_message.append('El formato de Documento de identidad no es valido. Favor introducir V|E|J + valor numérico. Ejemplos: V123456789 / J123456789')
        return error, error_message