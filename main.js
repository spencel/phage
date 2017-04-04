// Version 0.3 - added images of proteins

var diToggled = {};

var objPhage = {
	cursorOnPhageWithId: "",
	showingPhageDataWithId: "",
	init: function() {
		var numLength = arPhages.length;
		strHtml = "<table id=\"table1\">";
		for (var i = 0; i < numLength; i++) {
			var strGenomeId = arPhages[i][0];
			var strBpRange = arPhages[i][1];
			var strSpecieName = arPhages[i][2];
			var strProteinId = arPhages[i][4];
			strHtml = strHtml +
				"<tr id=\"r-"+ i + "\">"+
					"<td id=\"c-"+ i +"\" class=\"p\">"+ strGenomeId + "<br>" + arPhages[i][4] + "<br>" + arPhages[i][5] + "<br>" + arPhages[i][6] + "<br>" + strSpecieName + "</td>"+
				"</tr>";
		}
		strHtml = strHtml + "</table>";
		console.log( strHtml );
		jQuery( "body" ).append(strHtml);
		cursorOnPhageWithId = "c-0";
		jQuery('#'+ cursorOnPhageWithId).after("<td id='button-showData' class='p'>...</td>");
	},
	toggle: function( eleId ) {
		if ( diToggled.hasOwnProperty( eleId ) ) {
		} else {
			if ( eleId.split('-')[0] == 'c' && eleId != cursorOnPhageWithId) {
				cursorOnPhageWithId = eleId;
				jQuery('#button-showData').remove();
				jQuery('#'+ cursorOnPhageWithId).after("<td id='button-showData' class='p'>...</td>")
			}
		}
	},
	showData: function() {
		jQuery('#button-showData').remove();
		showingPhageDataWithId = cursorOnPhageWithId;
		diToggled[ showingPhageDataWithId ] = '';
		var phageId = cursorOnPhageWithId.split('-')[1];
		console.log(phageId);
		var phageIndeces = arPhages[phageId][3];
		console.log(arPhages[phageId]);
		strHtml = "<table><tr><td>Rank</td><td>Template/Model</td><td>Confidence</td><td>Sequence ID</td><td>Qstart</td><td>Qend</td><td>Resolution</td><td>Template Info</td></tr>";
		for (iRow = 0; iRow < phageIndeces.length; iRow++) {
			strHtml = strHtml + "<tr>";
			var phageIndex = phageIndeces[iRow];
			var rank = extSumInf[phageIndex][1]; //skip first column because it's relational
			var templateModel = extSumInf[phageIndex][2];
			var confidence = Math.round( Number( extSumInf[ phageIndex ][ 3 ] ) * 10000 ) / 100 + "%";
			var sequenceId = extSumInf[phageIndex][4];
			var qStart = extSumInf[phageIndex][5];
			var qEnd = extSumInf[phageIndex][6];
			var resolution = extSumInf[phageIndex][7];
			var templateInfo1 = extSumInf[phageIndex][8];
			var templateInfo2 = extSumInf[phageIndex][9];
			var templateInfo3 = extSumInf[phageIndex][10];
			strHtml = strHtml
				+ "<td class='center'>" + rank + "</td><td><a  target='_blank' href='" + strArPhageDirPaths[phageId] + "/" + templateModel + "'>"
				+ templateModel + "</a></br><img id='button-showLargeProteinImage-" + phageId + "-" + rank + "' src='" + strArPhageDirPaths[phageId] + "/" + templateModel.replace( "pdb", "png" ) + "'></td><td class='center'>"
				+ confidence + "</td><td class='center'>"
				+ sequenceId + "</td><td class='center'>"
				+ qStart + "</td><td class='center'>"
				+ qEnd + "</td><td class='center'>"
				+ resolution + "</td><td>"
				+ templateInfo1 + "<br>"
				+ templateInfo2 + "<br>"
				+ templateInfo3 + "</td></tr>";
		}
		strHtml = strHtml + "</table>";
		jQuery('#'+ showingPhageDataWithId).after(strHtml);
	},
	showLargeProteinImage: function( event ) {
		var id = event.target.id;
		var arId = id.split("-");
		var element = jQuery( "#" + id );
		newId = "button-showSmallProteinImage-" + arId[2] + "-" + arId[3];
		element.attr({ "id": newId, "src": element.attr( "src" ).replace( ".png", ".big.png" ) });
	},
	showSmallProteinImage: function( event ) {
		var id = event.target.id;
		var arId = id.split("-");
		var element = jQuery( "#" + id );
		newId = "button-showLargeProteinImage-" + arId[2] + "-" + arId[3];
		element.attr({ "id": newId, "src": element.attr( "src" ).replace( ".big.png", ".png" ) });
	},
	sortByConfidence: function() {

		function swap(items, firstIndex, secondIndex){

		    var temp = items[firstIndex];
		    items[firstIndex] = items[secondIndex];
		    items[secondIndex] = temp;
		}

		function partition(items, left, right) {

		    var pivot   = items[Math.floor((right + left) / 2)][3],
		        i       = left,
		        j       = right;


		    while (i <= j) {

		        while (items[i][3] < pivot) {
		            i++;
		        }

		        while (items[j][3] > pivot) {
		            j--;
		        }

		        if (i <= j) {
		            swap(items, i, j);
		            i++;
		            j--;
		        }
		    }

		    return i;
		}

		function quickSort(items, left, right) {

		    var index;

		    if (items.length > 1) {

		        index = partition(items, left, right);

		        if (left < index - 1) {
		            quickSort(items, left, index - 1);
		        }

		        if (index < right) {
		            quickSort(items, index, right);
		        }

		    }

		    return items;
		}

		quickSort(extSumInf, 0, extSumInf.length - 1);

		strHtml = "<tr><td>Specie</td><td>Template/Model</td><td>Confidence</td><td>Sequence ID</td><td>Qstart</td><td>Qend</td><td>Resolution</td><td>Template Info</td></tr>";
		
		for (iRow = extSumInf.length - 1; iRow > 0; iRow--) {
			strHtml = strHtml + "<tr>";
			var phageId = extSumInf[iRow][0];
			var strGenomeId = arPhages[phageId][0];
			var strBpRange = arPhages[phageId][1];
			var strSpecieName = arPhages[phageId][2];
			var rank = extSumInf[iRow][1];
			var templateModel = extSumInf[iRow][2];
			var confidence = Math.round( Number( extSumInf[ iRow ][ 3 ] ) * 10000 ) / 100 + "%";
			var sequenceId = extSumInf[iRow][4];
			var qStart = extSumInf[iRow][5];
			var qEnd = extSumInf[iRow][6];
			var resolution = extSumInf[iRow][7];
			var templateInfo1 = extSumInf[iRow][8];
			var templateInfo2 = extSumInf[iRow][9];
			var templateInfo3 = extSumInf[iRow][10];
			strHtml = strHtml
				+ "<td id=\"d-"+ phageId +"\" class=\"p\">"+ strGenomeId +", " + strBpRange + "<br>" + strSpecieName + "</td>"
				+ "<td><a  target='_blank' href='" + strArPhageDirPaths[phageId] + "/" + templateModel + "'>"
				+ templateModel + "</a></td><td class='center'>"
				+ confidence + "</td><td class='center'>"
				+ sequenceId + "</td><td class='center'>"
				+ qStart + "</td><td class='center'>"
				+ qEnd + "</td><td class='center'>"
				+ resolution + "</td><td>"
				+ templateInfo1 + "<br>"
				+ templateInfo2 + "<br>"
				+ templateInfo3 + "</td></tr>";
		}

		jQuery( "#table1" ).html( strHtml );

	}
}




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
		case 'd':
		case 'c':
			openSummary( event_target_id[1] );
			break;

		case 'sortByConfidence':
			objPhage.sortByConfidence();
			break;

		case 'button':
			switch ( event_target_id[1] ) {
				case "showData":
					objPhage.showData();
				break;
				case "showLargeProteinImage":
					objPhage.showLargeProteinImage( event );
				break;
				case "showSmallProteinImage":
					objPhage.showSmallProteinImage( event );
				break;
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
		case "button":
		break;
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
	var strMatch = document.getElementById( "searchA" ).value.toLowerCase();
	console.log(strMatch);
	strHtml = "";
	var numLength = arPhages.length - 1;
	for (var i = 0; i < numLength; i++) {
		if (arPhages[i][0].toLowerCase().indexOf(strMatch) != -1) {
			strHtml = strHtml +"<tr id=\"r-"+ i + "\"><td id=\"c-"+ i +"\" class=\"p\">"+ arPhages[i][0] +"<br>" + arPhages[i][4] + "<br>" + arPhages[i][5] + "<br>" + arPhages[i][6] + "<br>" + arPhages[i][2] +"</td></tr>";
		} else if (arPhages[i][1].toLowerCase().indexOf(strMatch) != -1) {
			strHtml = strHtml +"<tr id=\"r-"+ i + "\"><td id=\"c-"+ i +"\" class=\"p\">"+ arPhages[i][0] +"<br>" + arPhages[i][4] + "<br>" + arPhages[i][5] + "<br>" + arPhages[i][6] + "<br>" + arPhages[i][2] +"</td></tr>";
		} else if (arPhages[i][2].toLowerCase().indexOf(strMatch) != -1) {
			strHtml = strHtml +"<tr id=\"r-"+ i + "\"><td id=\"c-"+ i +"\" class=\"p\">"+ arPhages[i][0] +"<br>" + arPhages[i][4] + "<br>" + arPhages[i][5] + "<br>" + arPhages[i][6] + "<br>" + arPhages[i][2] +"</td></tr>";
		}
	}
	document.getElementById( "table1" ).innerHTML= strHtml;
}
function openSummary( pId ) {
	window.open(strArPhageDirPaths[pId] + "/summary.html","_blank")
}




function main() {

	objPhage.init();
	

}