# -*- coding: utf-8 -*-

from odoo import models, fields, api


class gestion_equipements(models.Model):
    _name = 'product.attribution'
    _inherit = 'mail.thread'
    _description = 'Rédaction spécification fonctionnelle'

    reference = fields.Char("Reference")
    employee_id = fields.Many2one("hr.employee", "Employee", track_visibility='always')
    materiel_id = fields.Many2one("product.template", "material", track_visibility='always')
    date_delivrance = fields.Date("date de délirance")
    numero_de_serie = fields.Char("numero de serie")
    valeur_materielle = fields.Float("Valeur du materielle")
    categorie_materiel_id = fields.Many2one("product.category", "categorie du materiel")
    note = fields.Text("note")
    attribue_par = fields.Many2one("res.users", "attribuer par")
    state = fields.Selection([
            ('nouveau','Nouveau'),
            ('attribue','Attribue'),
            ('retourner','Retourner'),
            ('perdu','Perdu'),
            ('casse','Casse'),
            ('rembourser','Rembourser'),
            ('annuler','Annuler')
    ], default='nouveau')
    
    def attribuer(self):
        if self.state == 'nouveau':
            return self.write({'state': 'attribue'})
        
    def retourner(self):
        if self.state == 'attribue':
            return self.write({'state': 'retourner'})
    
    def annuler(self):
        if self.state == 'attribue':
            return self.write({'state': 'annuler'})
    
        


