define(['jquery', 'underscore', 'backbone', 'text!tpl/about.html'], function ($, _, Backbone, tpl) {

    "use strict"; 


    var template = _.template(tpl);

    return Backbone.View.extend({

        render: function () {
            this.$el.html(template());
            return this;
        }

    });


});