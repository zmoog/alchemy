requirejs.config({
    baseUrl: appStaticPath + 'js/lib',
    paths: {
        // the left side is the module ID,
        // the right side is the path to
        // the jQuery file, relative to baseUrl.
        // Also, the path should NOT include
        // the '.js' file extension. This example
        // is using jQuery 1.9.0 located at
        // js/lib/jquery-1.9.0.js, relative to
        // the HTML page.
        'backbone': 'backbone',
        'bootstrap': 'bootstrap.min',
        'jquery': 'jquery-1.10.2.min',
        'moment': 'moment.min',
        'underscore': 'underscore-min',

        'app': '../app',
        'tpl': '../tpl'
    },
    map: {
        '*': {
            'app/models/account': 'app/models/json/account',
            'app/models/transfer': 'app/models/json/transfer'
        }
    },
    shim: {
        'bootstrap': {
            deps: ['jquery']
        },
        'backbone': {
            //These script dependencies should be loaded before loading
            //backbone.js
            deps: ['underscore', 'jquery'],
            //Once loaded, use the global 'Backbone' as the
            //module value.
            exports: 'Backbone'
        },
        'underscore': {
            exports: '_'
        }
    }
});

require(['bootstrap', 'backbone', 'app/router'], function(bootstrap, Backbone, Router) {
    //This function is called when scripts/helper/util.js is loaded.
    //If util.js calls define(), then this function is not fired until
    //util's dependencies have loaded, and the util argument will hold
    //the module value for "helper/util".

    var router = new Router();
    Backbone.history.start();

    console.log('ready!')
});