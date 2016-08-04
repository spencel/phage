jQuery( document ).ready( function() { // Runs program when webpage has fully loaded all elements and resources

var eleBody = jQuery( "body" );

var objPhage = {
	cursorOnPhageWithId: "",
	showingPhageDataWithId: "",
	init: function() {
		var numLength = arPhages.length;
		strHtml = "<table id=\"table1\">";
		for (var i = 0; i < numLength; i++) {
			var strDescription = arPhages[i][0];
			strHtml = strHtml +
				"<tr id=\"r-"+ i + "\">"+
					"<td id=\"c-"+ i +"\" class=\"p\">"+ strDescription +"</td>"+
				"</tr>";
			//eleBody.append("<div>"+ strDescription +"</div>");
		}
		strHtml = strHtml + "</table>";
		eleBody.append(strHtml);
		cursorOnPhageWithId = "c-0";
		jQuery('#'+ cursorOnPhageWithId).after("<td id=\"b-showData\" class=\"p\">...</td>");
	},
	toggle: function( eleId ) {
		if ( eleId.split('-')[0] == 'c' && eleId != cursorOnPhageWithId) {
			cursorOnPhageWithId = eleId;
			jQuery('#b-showData').remove();
			jQuery('#'+ cursorOnPhageWithId).after("<td id=\"b-showData\" class=\"p\">...</td>")
		}
	},
	showData: function () {
		jQuery('#b-showData').remove();
		showingPhageDataWithId = cursorOnPhageWithId;
		var phageId = cursorOnPhageWithId.split('-')[1];
		var phageIndeces = arPhages[phageId][2];
		console.log(arPhages[phageId]);
		strHtml = "<table>";
		for (iRow = 0; iRow < phageIndeces.length; iRow++) {
			strHtml = strHtml + "<tr>";
			for (iCol = 1; iCol < extSumInf[phageIndeces[iRow]].length; iCol++) { //skip first column because it's relational
				strHtml = strHtml + "<td>" + extSumInf[phageIndeces[iRow]][iCol] + "</td>";
			}
			strHtml = strHtml + "</tr>";
		}
		strHtml = strHtml + "</table>";
		jQuery('#'+ showingPhageDataWithId).after(strHtml);
	}
}

objPhage.init();


// Input: Keyboard
jQuery( document ).on("keydown", function( event ) { // Possibly consider using "window" instead of "document".
	event.stopPropagation(); // stops the event from triggering subsequent parent elements

	var event_keyCode = event.keyCode;
	switch ( event_keyCode ) {
		// Key: Enter
		case 13:
		break;
		default:
			var event_target_id = event.target.id;
			switch ( event_target_id ) {
				default:
			}

	}
});
jQuery( document ).on("keyup", function( event ) { // Possibly consider using "window" instead of "document".
	event.stopPropagation(); // stops the event from triggering subsequent parent elements
	var event_keyCode = event.keyCode;
	switch ( event_keyCode ) {
		// Key: Enter
		case 13:
		break;
		default:
			var event_target_id = event.target.id;
			switch ( event_target_id ) {
				// Context: Phage name/id query
				case "searchA":
					searchA();
				break;
				default:
			}
	}
});

// Input: Mouse
jQuery( document ).on("click", function( event ) {
	event.stopPropagation(); // stops the event from triggering subsequent parent elements
	var event_target_id = event.target.id.split('-');
	switch ( event_target_id[0] ) {
		case 'c':
			openSummary( event_target_id[1] );
		case 'b':
			switch ( event_target_id[1] ) {
				case "showData":
					objPhage.showData();
				default:
			}
		default:
	}
});
jQuery( document ).on("mousedown", function( event ) { // Possibly consider using "window" instead of "document".
	event.stopPropagation(); // stops the event from triggering subsequent parent elements
	var event_target_id = event.target.id.split('-');
	switch ( event_target_id ) {
		default:
	}
});
jQuery( document ).on("mouseup", function( event ) { // Possibly consider using "window" instead of "document".
	event.stopPropagation(); // stops the event from triggering subsequent parent elements
	var event_target_id = event.target.id.split('-');
	switch ( event_target_id ) {
		default:
	}
});
jQuery( document ).on("mousemove", function( event ) { // Possibly consider using "window" instead of "document".
	event.stopPropagation(); // stops the event from triggering subsequent parent elements
	var event_target_id = event.target.id.split('-');
	switch ( event_target_id[0] ) {
		case 'c':
			objPhage.toggle(event.target.id);
		break;
		default:
	}
});
jQuery( document ).on("mouseover", function( event ) { // Possibly consider using "window" instead of "document".
	event.stopPropagation(); // stops the event from triggering subsequent parent elements
	var event_target_id = event.target.id.split('-');
	switch ( event_target_id[0] ) {
		default:
	}
});
jQuery( document ).on("mouseout", function( event ) { // Possibly consider using "window" instead of "document".
	event.stopPropagation(); // stops the event from triggering subsequent parent elements
	var event_target_id = event.target.id.split('-');
	switch ( event_target_id[0] ) {
		default:
	}
});

// Input: Touchscreen
jQuery( document ).on("touchmove", function( event ) {
	event.stopPropagation(); // stops the event from triggering subsequent parent elements
	var event_target_id = event.target.id.split('-');
	alert("touchmove!");
	switch ( event_target_id[0] ) {
		case 'c':
			objPhage.toggle(event.target.id);
		break;
		default:
	}
});


function searchA() {
	document.getElementById( "table1" ).innerHTML= "" ;
	//console.log(document.getElementById( "searchA" ).value);
	var strMatch = document.getElementById( "searchA" ).value;
	console.log(strMatch);
	strHtml = "";
	var numLength = arPhages.length - 1;
	for (var i = 0; i < numLength; i++) {
		if (arPhages[i][0].toLowerCase().indexOf(strMatch) != -1) {
			strHtml = strHtml +"<tr id=\"r-"+ i + "\"><td id=\"c-"+ i +"\" class=\"p\">"+ arPhages[i][0] +"</td></tr>";
		}
	}
	document.getElementById( "table1" ).innerHTML= strHtml;
}
function openSummary( pId ) {
	window.open(strArPhageDirPaths[pId] + "/summary.html","_blank")
}
}); // End jQuery( document ).ready( function() {

