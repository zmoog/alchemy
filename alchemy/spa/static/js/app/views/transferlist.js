define(['jquery', 'underscore', 'backbone', 'app/models/transfer', 'text!tpl/transferlist.html'], function ($, _, Backbone, models,tpl) {

    "use strict";


    var template = _.template(tpl);

    return Backbone.View.extend({

    	initialize: function () {

            console.log('TransferListView::initialize')
    		this.collection = new models.TransferCollection();

			// this.listenTo( this.collection, 'add', this.renderTransfer );
            this.listenTo(this.collection, 'reset', this.render);
			this.listenTo(this.collection, 'sync', this.render);

            console.log('TransferListView::initialize fetching models from server')
            this.collection.fetch();
    	},

        render: function () {
        	console.log('TransferListView::render')
            this.$el.html(template({transferList: this.collection}));
            // this.collection.each(function (item) {
            // 	this.renderTransfer(item);
            // });
            return this;
        } // ,

        // renderTransfer: function (item) {
        // 	// console.log('TransferListView::renderTransfer')
        // 	var transferItemView = new TransferItemView({model: item});
        // 	this.$el.append(transferItemView.render().el)
        // }

    });

});