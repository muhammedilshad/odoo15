odoo.define('custom_pos.user_interface', function(require) {
	"User strict";
	var models = require('point_of_sale.models');
	models.load_fields("product.product", ['prod_rating']);
});