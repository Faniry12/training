# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date
from dateutil import relativedelta


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    display_name = fields.Char(compute='_compute_display_name', store=True, index=True)
    second_name = fields.Char(string="Second name")
    registration_number = fields.Char(string='Registration number')
    cnaps_registration = fields.Char(string="CNaPS Registration")
    classification = fields.Many2one('hr.classification', string='Classification')
    bank_is = fields.Char(string='Bank', related='bank_account_id.bank_id.name')
    index = fields.Char(string='Index')
    title_id = fields.Many2one('res.partner.title', string='Title')
    other_email = fields.Char(string='Other professional email')
    # seniority = fields.Char(string='Seniority', compute='_compute_seniority', store=True)

    def name_get(self):
        res = []
        for rec in self:
            if rec.second_name:
                res.append((rec.id, "%s %s" % (rec.name, rec.second_name)))
            else:
                res.append((rec.id, "%s" % rec.name))
        return res

    def _compute_display_name(self):
        for rec in self:
            if rec.second_name:
                rec.display_name = "%s %s" % (rec.name, rec.second_name)
            else:
                rec.display_name = "%s" % rec.name

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('display_name', operator, name), ('registration_number', '=', name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    @api.depends('first_contract_date')
    def _compute_seniority(self):
        for rec in self:
            if rec.first_contract_date:
                today = date.today()
                diff = relativedelta.relativedelta(today, rec.first_contract_date)
                years = diff.years
                months = diff.months
                days = diff.days
                rec.seniority = '%s %s %s' % (str(years) + ' years' if years else '',
                                              str(months) + ' months' if months else '',
                                              str(days) + ' days' if days else '')
