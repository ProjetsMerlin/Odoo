from odoo import models, fields

class BlogComment(models.Model):
    _name        = 'mon.blog.comment'
    _description = 'Commentaire de blog'
    _order       = 'date_publication desc'

    author_name      = fields.Char(string='Auteur', required=True)
    content          = fields.Text(string='Commentaire', required=True)
    date_publication = fields.Datetime(string='Date', default=fields.Datetime.now)

    article_id = fields.Many2one(
        comodel_name='mon.blog.article',
        string='Article',
        required=True,
        ondelete='cascade'
    )