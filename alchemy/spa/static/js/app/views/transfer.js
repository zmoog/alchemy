define(['jquery', 'underscore', 'backbone', 'moment', 'text!tpl/transfer.html'], function ($, _, Backbone, moment, tpl) {

    "use strict";


    var template = _.template(tpl);

    return Backbone.View.extend({

        render: function () {
            this.$el.html(template({
            	transfer: this.model,
                moment: moment
            }));
            return this;
        }

    });

});