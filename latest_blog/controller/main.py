# from odoo import http
# from odoo.http import request
# import json
#
#
# class LatestBlog(http.Controller):
#     @http.route(['/latest_blog'], type="json", auth="public")
#     def latest_blog(self):
#         blog_obj = request.env['blog.post'].sudo().search([], limit=4)
#         obl_list = []
#         for rec in blog_obj:
#             values = json.loads(rec["cover_properties"])
#             image = values["background-image"][6:-2]
#             values = {
#                 'title': rec.name,
#                 'subtitle': rec.subtitle,
#                 'blg_img': image,
#                 'url': rec.website_url
#             }
#             obl_list.append(values)
#         data = {
#                 'blog_data': obl_list,
#         }
#         print(data)
#         res = http.Response(template="latest_blog.latest_blog_snippet_templ", qcontext=data)
#         return res.render()

