odoo.define('pos_rating.receipt', function (require) {
"use strict";
var models = require('point_of_sale.models');
models.load_fields('product.product', 'prod_rating');
var _super_orderline = models.Orderline.prototype;

models.Orderline = models.Orderline.extend({
    export_for_printing: function() {
        var line = _super_orderline.export_for_printing.apply(this,arguments);
        line.prod_rating = this.get_product().prod_rating;
        return line;
    },
});
});