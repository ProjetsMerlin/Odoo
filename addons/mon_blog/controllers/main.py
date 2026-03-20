from odoo import http
from odoo.http import request

class BlogController(http.Controller):

    @http.route('/blog', type='http', auth='public', website=True)
    def blog_list(self, **kwargs):
        """Page liste — tous les articles publiés"""
        articles = request.env['mon.blog.article'].sudo().search([
            ('is_published', '=', True)
        ])
        tags = request.env['mon.blog.tag'].sudo().search([])

        return request.render('mon_blog.blog_list_template', {
            'articles': articles,
            'tags': tags,
        })

    @http.route('/blog/<string:slug>', type='http', auth='public', website=True)
    def blog_detail(self, slug, **kwargs):
        """Page détail — un article par son slug"""
        article = request.env['mon.blog.article'].sudo().search([
            ('slug', '=', slug),
            ('is_published', '=', True),
        ], limit=1)

        if not article:
            return request.not_found()

        article.sudo().write({'nb_vues': article.nb_vues + 1})

        return request.render('mon_blog.blog_detail_template', {
            'article': article,
        })

    @http.route('/blog/tag/<string:tag_name>', type='http', auth='public', website=True)
    def blog_by_tag(self, tag_name, **kwargs):
        """Filtrer par tag"""
        tag = request.env['mon.blog.tag'].sudo().search([
            ('name', 'ilike', tag_name)
        ], limit=1)

        articles = request.env['mon.blog.article'].sudo().search([
            ('is_published', '=', True),
            ('tag_ids', 'in', tag.ids),
        ]) if tag else []

        return request.render('mon_blog.blog_list_template', {
            'articles': articles,
            'tags': request.env['mon.blog.tag'].sudo().search([]),
            'tag_actif': tag,
        })