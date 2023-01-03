odoo.define('documents.DocumentsInspector.inherit', function (require) {"use strict";
var model = require('documents.DocumentsInspector');
var core = require('web.core');
var _t = core._t;
var qweb = core.qweb;
var web = require('web.data');
var DocumentsInspector = model.include({
events: {
	'click .change_stage_action': '_onClick',
}
})
})