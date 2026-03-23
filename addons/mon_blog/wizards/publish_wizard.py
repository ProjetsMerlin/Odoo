from odoo import models, fields

class PublishWizard(models.TransientModel):
    _name        = 'mon.blog.publish.wizard'
    _description = 'Assistant de publication'

    state = fields.Selection([
        ('published', 'Publié'),
        ('draft',     'Brouillon'),
        ('archived',  'Archivé'),
    ], string='Nouveau statut', required=True, default='published')

    nb_articles = fields.Integer(
        string='Articles sélectionnés',
        readonly=True
    )

    def action_confirm(self):
        articles = self.env['mon.blog.article'].browse(
            self.env.context.get('active_ids', [])
        )
        articles.write({'state': self.state})
        return {'type': 'ir.actions.act_window_close'}