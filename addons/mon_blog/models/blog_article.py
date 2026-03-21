from odoo import models, fields, api

class BlogArticle(models.Model):
    _name = 'mon.blog.article'
    _description = 'Article de blog'
    _order = 'date_publication desc'

    name = fields.Char(string='Titre', required=True)
    slug = fields.Char(string='URL slug', required=True)
    auteur_id = fields.Many2one('res.users', string='Auteur', default=lambda self: self.env.user)
    date_publication = fields.Date(string='Date de publication', default=fields.Date.today)
    image = fields.Image(string='Image de couverture')
    resume = fields.Text(string='Résumé')
    contenu = fields.Html(string='Contenu')
    tag_ids = fields.Many2many('mon.blog.tag', string='Tags')
    is_published = fields.Boolean(string='Publié', default=False)
    nb_vues = fields.Integer(string='Vues', default=0, readonly=True)

    state = fields.Selection([
        ('draft',     'Brouillon'),
        ('published', 'Publié'),
        ('archived',  'Archivé'),
    ], string='Statut', default='draft', required=True)

    comment_ids = fields.One2many(
        comodel_name='mon.blog.comment',
        inverse_name='article_id',
        string='Commentaires'
    )

    comment_count = fields.Integer(
        string='Nb commentaires',
        compute='_compute_comment_count',
        store=True
    )

    @api.depends('comment_ids')
    def _compute_comment_count(self):
        for article in self:
            article.comment_count = len(article.comment_ids)

    @api.constrains('slug')
    def _check_slug_unique(self):
        for rec in self:
            existing = self.search([
                ('slug', '=', rec.slug),
                ('id', '!=', rec.id)
            ])
            if existing:
                raise models.ValidationError("Ce slug est déjà utilisé !")

class BlogTag(models.Model):
    _name = 'mon.blog.tag'
    _description = 'Tag de blog'

    name = fields.Char(string='Nom', required=True)
    color = fields.Char(string='Couleur')