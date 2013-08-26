define(['jquery', 'backbone'], function ($, Backbone) {

    "use strict";

    var Transfer = Backbone.Model.extend({

            urlRoot: "/api/transfers/",

            initialize: function () {
            }

        }),

        TransferCollection = Backbone.Collection.extend({

            model: Transfer,

            url: "/api/transfers/",

            parse: function(response) {
                return response.results;
            }

        });

    return {
        Transfer: Transfer,
        TransferCollection: TransferCollection
    };

});