
var walk = function(row, column_index, depth) {
		
		var cell = row.childNodes[column_index];
		
		for (i = 0; i < depth; i++) {
			cell = cell.childNodes[0];
		}
		
		return cell.nodeValue;
};

var simple_element = function(tag, attributes) {

	var start = '<' + tag;
	
	var attrs = '';
	
	$(attributes).each(function(i,attr) {
		attrs += ' ' + attr;
	});
	
	start + '>';
	
	var end = '</' + tag + '>'
	
	return start + attrs + end;
}

var multiseries_chart = function(rows, context) { 

	//var header = "<graph caption='Daily Visits' subcaption='(from 8/6/2006 to 8/12/2006)' hovercapbg='FFECAA' hovercapborder='F47E00' formatNumberScale='0' decimalPrecision='0' showvalues='0' numdivlines='3' numVdivlines='0' yaxisminvalue='1000' yaxismaxvalue='1800'  rotateNames='1'>";
	var header = "<graph caption='Daily Visits' subcaption='(from 8/6/2006 to 8/12/2006)' hovercapbg='FFECAA' hovercapborder='F47E00' formatNumberScale='0' decimalPrecision='0' showvalues='0' numdivlines='3' rotateNames='0'>";
	//var header = "<graph caption='Daily Visits' subcaption='(from 8/6/2006 to 8/12/2006)' hovercapbg='FFECAA' hovercapborder='F47E00' rotateNames='1'>";
	var footer = "</graph>";
	
	var categories = [];
	var datasets = [];
	
	$(context.series).each( function(j, serie) {

		var set_values = []
	
		rows.each( function(i, row) {
		
			var name = walk(row, serie.name.column, serie.name.depth);
			var value = walk(row, serie.value.column, serie.value.depth);
			
			set_values[i] = value;
			categories[i] = { 'name': name };

		});		

		datasets[j] = { 'seriesName': j, 'values': set_values };			
	});
	
	var xml = '';
	
	xml += header;
	xml += '<categories>';
	
	$(categories).each(function(i, category) {
		xml += "<category name='" + category.name + "' />";
	});
	
	xml += '</categories>';
	
	$(datasets).each( function(i, dataset) {
		xml += "<dataset seriesname='" + context.series[i]['label'] + "' color='" + context.series[i]['color'] + "'>";
		$(dataset.values).each( function(i, value) {
			xml += "<set value='" + value + "' />";
		});
		xml += "</dataset>";
	});

	xml += footer;

	return xml	;
}

var build_graph = function (rows, context) {

	var header = "<graph caption='Monthly Unit Sales' xAxisName='Month' yAxisName='Units' showNames='1' decimalPrecision='0' formatNumberScale='0'>";
    var build_row = function(name, value, color) { return "<set name='" + name + "' value='" + value + "' color='" + color + "'></set>" };
    var footer = "</graph>";
  
    var xml = header;

    rows.each( function(i, row) { 

	 	$(context['series']).each( function(i, serie) {

			var name = walk(row, serie['name']['column'], serie['name']['depth']);
			var value = walk(row, serie['value']['column'], serie['value']['depth']);
			
 	    	xml += build_row( 
    			escape(name), 
    			escape(value), 
    			'B3AACC'
    		);
	    	
	 	})

    });
    
    xml += footer;
    
    return xml;
    
};